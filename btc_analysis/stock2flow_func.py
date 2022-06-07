import math
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy import stats

from btc_analysis.config import (GOLD_FLOW_TONS, GOLD_STOCK_TONS, HALVING_DATE,
                                 MINING_REWARD, SILVER_STOCK_TONS,
                                 SIVER_FLOW_TONS, MKT_CAP_LOG_VAL)
from btc_analysis.market_data import yesterday_str
from btc_analysis.mongo_func import mongo_upload, query_mongo

# -----------------------
# TIME FUNCTIONS
# -----------------------

# function that generate an array of date starting from
# start_date to end_date given in mm-dd-yyyy format;


def date_gen(start_date, end_date, clss="array"):

    date_index = pd.date_range(start_date, end_date)

    date_ll = [datetime.strftime(date, "%d-%m-%Y") for date in date_index]

    if clss == "array":

        date_ll = np.array(date_ll)

    return date_ll


# For each data point the following data will be needed:
# Stock: The current * circulating supply.
# Flow: The extrapolated yearly emission based on the current * block reward.
# Price: The current * daily close of BTC’s USD price on Bitstamp exchange.
# Market capitalization: The product of the obtained stock and price(s.a.).

# --------------------
# MODEL DEFINITION
# --------------------


# the function takes as input a df of three columns: Date, USD_price, Supply
# and return a df with market cap, Stock to Flow ratio, ln(mkt_cap) and ln(SF)

def data_setup(initial_df):

    final_df = initial_df.copy()

    final_df["Market Cap"] = final_df["Supply"] * final_df["Price USD"]
    final_df["S2F ratio"] = stock2flow_ratio(final_df["Supply"])
    final_df["ln(S2F ratio)"] = np.log(final_df["S2F ratio"])
    final_df["ln(mkt_cap)"] = np.log(final_df["Market Cap"])

    final_df = final_df.replace([np.inf, -np.inf], np.nan)
    final_df.fillna(0, inplace=True)

    return final_df


# the function computes the Stock to Flow ratio values for
# the passed array containing the supply
# S2F = 1/Yearly Supply growth Rate
# Supply grpwth rate with monthly observation:
# GR = (Supply_t - Supply_t-1)/Supply_t-1
# That on year basis becomes:
# SF = Supply_t-1 / ((Supply_t - Supply_t-1) * 12)

def stock2flow_ratio(supply_df):

    x_1_to_n = np.array(supply_df.tail(len(supply_df.index) - 1))

    x_0_to_n_minus_1 = np.array(supply_df.head(len(supply_df.index) - 1))
    x_0 = np.array(supply_df.head(1))[0]

    num = x_1_to_n - x_0
    den = (x_1_to_n - x_0_to_n_minus_1) * 12

    stock2flow_array = np.array(num / den)

    stock2flow_array = np.concatenate([[0], stock2flow_array])

    return stock2flow_array


def stock2flow_regression(data_df):

    final_df = data_df.copy()
    (slope, intercept, r_value, p_value, std_err) = stats.linregress(
        final_df["ln(S2F ratio)"], final_df["ln(mkt_cap)"])

    # final_df["S2F model"] = math.exp(
    #     intercept) * final_df["S2F ratio"] ** slope
    # final_df["S2F price"] = final_df["S2F model"] / final_df["Supply"]

    return final_df, slope, intercept, r_value


def S2F_definition(source_data):

    data_df = data_setup(source_data)

    _, slope, intercept, r_value = stock2flow_regression(data_df)

    np_regression = np.column_stack((slope, intercept, r_value))

    regression_df = pd.DataFrame(np_regression, columns=[
                                 "Slope", "Intercept", "R Value"])

    mongo_upload(data_df, "collection_S2F_source_data")
    mongo_upload(regression_df, "collection_S2F_regression")

    return slope, intercept

# Note: The corrected supply is higher than the theoretical supply because
# the hash rate of Bitcoin’s network has only grown since its beginning and
# difficulty is adjusting with a delay. Therefore, the real flow of Bitcoi
# n is higher than the theoretical flow extrapolated from the block reward.
# As a result of this, the flow is higher, the stock grows faster, and
# halvings occur sooner than in theory.
# (Theoretical Flow=Block Reward * 6 * 24 * 365, corr. fact.: 1.04)


def S2F_complete_model(slope, intercept):

    date_arr = date_gen("01-03-2009", "01-01-2030")

    date_df = pd.DataFrame(columns=["Date"])
    date_df["Date"] = date_arr

    final_df = reward_to_time(date_df)

    final_df["Daily Reward"] = final_df["Reward"] * 6 * 24

    final_df["Stock"] = final_df["Daily Reward"].cumsum()

    final_df["Flow"] = final_df["Daily Reward"] * 365

    final_df["S2F ratio"] = final_df["Stock"] / final_df["Flow"]

    final_df["S2F mkt cap"] = math.exp(
        intercept)*final_df["S2F ratio"] ** slope

    final_df["S2F price"] = final_df["S2F mkt cap"] / final_df["Stock"]

    final_df["S2F price 365d average"] = final_df["S2F price"].rolling(
        window=365).mean()

    return final_df


def reward_to_time(initial_df):

    final_df = initial_df.copy()

    final_df["Datetime"] = [datetime.strptime(
        date, "%d-%m-%Y") for date in final_df["Date"]]

    final_df["Reward"] = 50

    i = 1

    for h_date in HALVING_DATE:

        final_df.loc[final_df.Datetime > datetime.strptime(
            h_date, "%d-%m-%Y"), "Reward"] = MINING_REWARD[i]

        i = i + 1

    final_df = final_df.drop(columns=["Datetime"])

    return final_df


def days_to_halving(initial_df, halving_days_list):

    final_df = initial_df.copy()

    final_df["Datetime"] = [datetime.strptime(
        date, "%d-%m-%Y") for date in final_df["Date"]]

    i = 0
    days_to_halv = np.array([])

    for date in final_df["Datetime"]:

        next_halving = datetime.strptime(halving_days_list[i], "%d-%m-%Y")

        if next_halving == date:

            i = i + 1
            day_count = 0

        else:

            day_count = (next_halving - date).days

        days_to_halv = np.append(days_to_halv, day_count)

    final_df["Days to Halving"] = days_to_halv

    return final_df


# -----------------------------------
# POST HALVING PERFORMANCES COMPARISON
# ------------------------------------

def halving_performace(halving_df, date_df):

    price_only = halving_df["BTC Price"]
    return_only = np.array(price_only.pct_change())

    halving_df["BTC Return"] = return_only

    start_price = np.array(
        halving_df.loc[halving_df["Date"] == "11-05-2020", "BTC Price"])[0]

    return_df = halving_return_df(halving_df, date_df)
    perf_df = halving_normalize(return_df, start_price)

    return perf_df


def halving_return(halving_df, start_date, stop_date):

    start = datetime.strptime(start_date, "%d-%m-%Y")
    stop = datetime.strptime(stop_date, "%d-%m-%Y")

    period_ret_df = halving_df.loc[halving_df.Datetime.between(
        start, stop, inclusive='both'), "BTC Return"]

    return period_ret_df


def halving_return_df(halving_df, date_df):

    last_h_date = datetime.strptime("11-05-2020", "%d-%m-%Y")

    halving_2012_ret = halving_return(halving_df, "28-11-2012", "08-07-2016")
    halving_2016_ret = halving_return(halving_df, "09-07-2016", "10-05-2020")

    date_len = min(int(len(halving_2012_ret.index)),
                   int(len(halving_2016_ret.index)))
    date_df["Date"] = [datetime.strptime(
        date, "%d-%m-%Y") for date in date_df["Date"]]
    date_arr = date_df.loc[date_df.Date >= last_h_date, "Date"]

    halving_2012_ret = np.array(halving_2012_ret.head(date_len))
    halving_2016_ret = np.array(halving_2016_ret.head(date_len))
    date_arr = date_arr.head(date_len)

    header = ["Datetime", "halving 2012", "halving 2016"]
    final_df = pd.DataFrame(columns=header)
    final_df["Datetime"] = date_arr
    final_df["halving 2012"] = halving_2012_ret
    final_df["halving 2016"] = halving_2016_ret

    final_df.reset_index(drop=True, inplace=True)

    return final_df


def halving_normalize(return_df, start_price):

    return_df["Datetime"] = [datetime.strftime(
        date, "%d-%m-%Y") for date in return_df["Datetime"]]
    norm_matrix = np.array(return_df["Datetime"])

    halv_col_tot = list(return_df.columns)
    halv_col = halv_col_tot.copy()
    halv_col.remove("Datetime")

    for halving in halv_col:

        single_h_ret = np.array(return_df[halving])
        single_h_ret = single_h_ret[1:len(single_h_ret)]
        norm_arr = np.array([start_price])
        current_value = start_price

        for ret in single_h_ret:

            next_value = current_value * (1 + ret)
            norm_arr = np.append(norm_arr, next_value)

            current_value = next_value

        norm_matrix = np.column_stack((norm_matrix, norm_arr))

    header = halv_col_tot
    norm_df = pd.DataFrame(norm_matrix, columns=header)

    norm_df["Datetime"] = [datetime.strptime(
        date, "%d-%m-%Y") for date in norm_df["Datetime"]]

    return norm_df

# --------------------
# OTHER FUNCTIONS
# --------------------


def commodities_mkt_cap():

    yahoo_prices = query_mongo("btc_analysis", "all_prices_y")

    yahoo_last_day = yahoo_prices.tail(1)
    gold_price = np.array(yahoo_last_day["GOLD"])[0]
    silver_price = np.array(yahoo_last_day["SILVER"])[0]

    if math.isnan(gold_price) is False:
        pass

    else:

        yahoo_last_day = yahoo_prices.tail(2)
        yahoo_last = yahoo_last_day.head(1)
        gold_price = np.array(yahoo_last["GOLD"])[0]
        silver_price = np.array(yahoo_last["SILVER"])[0]

    gold_mkt_cap = GOLD_STOCK_TONS * 32000 * gold_price
    silver_mkt_cap = SILVER_STOCK_TONS * 32000 * silver_price

    return gold_mkt_cap, silver_mkt_cap


def commodities_df():

    gold_S2F = GOLD_STOCK_TONS / GOLD_FLOW_TONS
    silver_S2F = SILVER_STOCK_TONS / SIVER_FLOW_TONS
    gold_mkt_cap, silver_mkt_cap = commodities_mkt_cap()

    comm_arr = np.column_stack(
        (gold_S2F, gold_mkt_cap, silver_S2F, silver_mkt_cap))
    col_list = ["Gold S2F", "Gold mkt", "Silver S2F", "Silver mkt"]
    comm_df = pd.DataFrame(comm_arr, columns=col_list)

    return comm_df


def check_and_add():

    yesterday = yesterday_str("%d-%m-%Y")

    df_from_csv = pd.read_csv(
        Path("source_data", "BTC_price.csv"), sep="|")
    last_day = df_from_csv.tail(1)
    last_date = np.array(last_day["Date"])[0]

    if last_date == yesterday:

        pass

    else:

        crypto_price = query_mongo("index", "crypto_price")
        last_day_price = crypto_price.tail(1)
        btc_price = np.array(last_day_price["BTC"])[0]
        array_to_add = np.column_stack((yesterday, btc_price))
        df_to_add = pd.DataFrame(array_to_add, columns=["Date", "BTC Price"])

        df_to_add.to_csv(Path("source_data", "BTC_price.csv"),
                         mode='a', index=False, header=False, sep='|')


# function that camputes S2F values starting from mkt cap values
# and knowing slope and intercept of the regression function
# S2F = (mkt_cap / e ^ (intercept)) ^ (1/slope)

def S2F_reg_value(regression_df):

    slope = np.array(regression_df["Slope"])[0]
    intercept = np.array(regression_df["Intercept"])[0]

    regression_value_df = pd.DataFrame(
        np.array(MKT_CAP_LOG_VAL), columns=["Mkt Cap"])

    regression_value_df["S2F"] = [
        ((y/math.exp(intercept)) ** (1/slope)) for y in regression_value_df["Mkt Cap"]]

    return regression_value_df


# ----------------------
# STOCK TO FLOW CROSS MODEL
# -----------------------

def S2FX_complete_model(slope, intercept):

    date_arr = date_gen("01-03-2009", "01-01-2030")

    date_df = pd.DataFrame(columns=["Date"])
    date_df["Date"] = date_arr

    final_df = reward_to_time(date_df)

    final_df["Daily Reward"] = final_df["Reward"] * 6 * 24
    final_df["Stock"] = final_df["Daily Reward"].cumsum()
    final_df["Flow"] = final_df["Daily Reward"] * 365

    final_df["S2FX ratio"] = final_df["Stock"] / final_df["Flow"]

    final_df["S2FX mkt cap"] = math.exp(
        intercept)*final_df["S2FX ratio"] ** slope

    final_df["S2FX price"] = final_df["S2FX mkt cap"] / final_df["Stock"]

    final_df["S2FX price 365d average"] = final_df["S2FX price"].rolling(
        window=365).mean()

    return final_df


def add_commodity(cluster_df):

    commodity_df = commodities_df()

    gold_S2F = np.array(commodity_df["Gold S2F"])[0]
    gold_mkt = np.array(commodity_df["Gold mkt"])[0]
    ln_gold_S2F = np.log(gold_S2F)
    ln_gold_mkt = np.log(gold_mkt)
    gold_arr = np.column_stack((gold_S2F, gold_mkt, ln_gold_S2F, ln_gold_mkt))

    silver_S2F = np.array(commodity_df["Silver S2F"])[0]
    silver_mkt = np.array(commodity_df["Silver mkt"])[0]
    ln_silver_S2F = np.log(silver_S2F)
    ln_silver_mkt = np.log(silver_mkt)
    silver_arr = np.column_stack(
        (silver_S2F, silver_mkt, ln_silver_S2F, ln_silver_mkt))

    total_arr = np.row_stack((gold_arr, silver_arr))
    new_df = pd.DataFrame(total_arr, columns=list(cluster_df.columns))

    final_cluster_df = cluster_df.append(new_df)
    final_cluster_df.reset_index(drop=True, inplace=True)

    return final_cluster_df


def S2FX_definition(source_data, cluster_number):

    data_df = data_setup(source_data)

    cluster_df = cluster_finder(data_df, cluster_number)
    cluster_df = add_commodity(cluster_df)

    _, slope, intercept, r_value = stock2flow_regression(cluster_df)

    np_regression = np.column_stack((slope, intercept, r_value))

    regression_df = pd.DataFrame(np_regression, columns=[
                                 "Slope", "Intercept", "R Value"])

    mongo_upload(cluster_df, "collection_S2FX_cluster")
    mongo_upload(regression_df, "collection_S2FX_regression")

    return slope, intercept


def cluster_finder(initial_df, cluster_number):

    initial_df = initial_df[["S2F ratio", "Market Cap"]]
    initial_array = np.array(initial_df)
    kmeans = KMeans(n_clusters=cluster_number)
    kmeans.fit(initial_array)

    cluster_arr = kmeans.cluster_centers_

    cluster_df = pd.DataFrame(cluster_arr, columns=["S2F ratio", "Market Cap"])
    cluster_df["ln(S2F ratio)"] = np.log(cluster_df["S2F ratio"])
    cluster_df["ln(mkt_cap)"] = np.log(cluster_df["Market Cap"])

    return cluster_df
