import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import math

from btc_analysis.config import HALVING_DATE, MINING_REWARD


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

    final_df["S2F model"] = math.exp(
        intercept) * final_df["S2F ratio"] ** slope
    final_df["S2F price"] = final_df["S2F model"] / final_df["Supply"]

    return final_df, slope, intercept


def S2F_definition(source_data):

    data_df = data_setup(source_data)

    _, slope, intercept = stock2flow_regression(data_df)

    return slope, intercept

# Note: The corrected supply is higher than the theoretical supply because
# the hash rate of Bitcoin’s network has only grown since its beginning and
# difficulty is adjusting with a delay. Therefore, the real flow of Bitcoi
# n is higher than the theoretical flow extrapolated from the block reward.
# As a result of this, the flow is higher, the stock grows faster, and
# halvings occur sooner than in theory.
# (Theoretical Flow=Block Reward * 6 * 24 * 365, corr. fact.: 1.04)


def complete_model(slope, intercept):

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
