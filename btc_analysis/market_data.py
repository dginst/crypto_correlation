import json
from datetime import datetime, timezone
from pathlib import Path
import logging

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from pandas_datareader import data
from dateutil.relativedelta import relativedelta

from btc_analysis.calc import date_gen, date_gen_TS
from btc_analysis.config import (GOLD_OUNCES_SUPPLY, INDEX_DB_NAME,
                                 SILVER_OUNCES_SUPPLY, START_DATE, USD_SUPPLY)
from btc_analysis.mongo_func import mongo_upload, query_mongo, mongo_coll_drop
from btc_analysis.statistics import hist_std_dev

# -----------------------
# TIME FUNCTIONS
# -----------------------


def yesterday_str(format_="%Y-%m-%d"):

    today_str = datetime.now().strftime(format_)
    today = datetime.strptime(today_str, format_)
    today_TS = int(today.replace(tzinfo=timezone.utc).timestamp())
    yesterday_TS = today_TS - 86400
    yesterday_date = datetime.fromtimestamp(int(yesterday_TS))
    yesterday = yesterday_date.strftime(format_)

    return yesterday


# ----------------------------
# INDEX COLLECTIONS CHECKING
# ---------------------------

def index_coll_check(collection_name):

    yesterday = yesterday_str()

    crypto_price = query_mongo("index", collection_name)
    last_row = crypto_price.tail(1)
    last_date = np.array(last_row["Date"])[0]

    file_name = collection_name + ".csv"
    upload_name = "collection_" + collection_name

    if crypto_price == []:

        crypto_df = pd.read_csv(
            Path("source_data", "index_collections", file_name))
        mongo_upload(crypto_df, upload_name, db_name="index")

    else:

        if yesterday != last_date:

            mongo_coll_drop("index", db_name="index")
            crypto_df = pd.read_csv(
                Path("source_data", "index_collections", file_name))
            mongo_upload(crypto_df, upload_name, db_name="index")

        else:

            print("collection from index database are up to date")


# ----------------------------
# MARKET DATA OPERATIONS

# this set of functions are used to download and aggregate
# data from Yahoo Finance API
# ---------------------------


def all_series_download(series_code_list, all_el_list,
                        start_period, end_period):

    all_series_df_price = pd.DataFrame(columns=all_el_list)
    all_series_df_volume = pd.DataFrame(columns=all_el_list)

    for i, element in enumerate(series_code_list):

        var = all_el_list[i]

        single_series = single_series_download(
            element, start_period, end_period)

        if "BTC" in all_el_list:

            date_arr = single_series["Date"]

        else:

            if "Petrol" in all_el_list:

                date_arr = single_series["Date"]

            else:

                date_arr = single_series["Date"]

        all_series_df_price[var] = single_series["Close"]
        all_series_df_volume[var] = single_series["Volume"]

    all_series_df_price["Date"] = date_arr
    all_series_df_volume["Date"] = date_arr

    return all_series_df_price, all_series_df_volume


def single_series_download(series_code, start_period, end_period):

    print(series_code)
    # creatre object
    try:

        series_obj = yf.Ticker(series_code)

    except Exception:

        logging.error("Exception occurred", exc_info=True)
        logging.info(
            'The aseet with code {series_code} failed to download')

    # create the complete array of date
    date_arr = np.array(date_gen(start_period, end_period, holiday="N"))
    date_df = pd.DataFrame(columns=["Date"])
    date_df["Date"] = date_arr

    # get historical market data
    df = series_obj.history(start=start_period, end=end_period)
    df.reset_index(inplace=True)

    # modifying date format
    df["Date"] = [x.strftime("%Y-%m-%d") for x in df["Date"]]
    df = df[["Date", "Close", "Volume"]]

    merged = pd.merge(date_df, df, how="left", on="Date")

    return merged


def single_series_to_return(df_data, head_element, date_col="N"):

    # creatinmg a temporary df with prices only
    df_price = pd.DataFrame(columns=["Return"])
    df_price["Return"] = df_data[head_element]

    # computing the series price return
    return_df = df_price.pct_change()

    return_df["Date"] = df_data["Date"]
    return_df = return_df.sort_values(by=["Date"], ascending=False)

    if date_col == "N":

        return_df = return_df.drop(columns=["Date"])

    else:
        pass

    return return_df


def all_series_to_return(all_price_df, series_list):

    date_arr = pd.DataFrame(columns=["Date"])
    date_arr["Date"] = all_price_df["Date"]
    rev_date_arr = date_arr.sort_values(by=["Date"], ascending=False)

    all_ret_df = pd.DataFrame(columns=["Date"])
    all_ret_df["Date"] = rev_date_arr["Date"]

    for element in series_list:

        single_series = all_price_df[["Date", element]]
        single_series_ret = single_series_to_return(single_series, element)

        all_ret_df[element] = single_series_ret

    return all_ret_df


def all_series_to_logret(all_price_df):

    all_price_pure = all_price_df.drop(columns=["Date"])

    log_ret_df = np.log(all_price_pure / all_price_pure.shift(1))

    return log_ret_df


def mkt_data_op(series_code_list, all_el_list_d,
                all_el_list_r,
                start_period, end_period):

    (all_series_df_price,
     all_series_df_volume) = all_series_download(series_code_list,
                                                 all_el_list_d,
                                                 start_period,
                                                 end_period)

    # price and returns operation
    complete_series_df_price = all_series_df_price
    complete_series_df_price = add_crypto(all_series_df_price)
    mongo_upload(complete_series_df_price, "collection_prices_y")

    all_ret_df = all_series_to_return(complete_series_df_price, all_el_list_r)

    mongo_upload(all_ret_df, "collection_returns_y")

    all_logret_df = all_series_to_logret(complete_series_df_price)

    mongo_upload(all_logret_df, "collection_logreturns_y")

    # volume operation

    complete_series_df_volume = add_crypto(
        all_series_df_volume, collection="crypto_volume")

    df_all_pair = query_mongo("index", "index_data_feed")

    try:

        no_stable_vol_df = crypto_vol_no_stable(df_all_pair)

    except Exception:

        logging.error("Exception occurred", exc_info=True)
        logging.info(
            'The collection with all the exchanges values of volume\
             may be not updated')

    complete_series_df_volume = add_no_stable(
        complete_series_df_volume, no_stable_vol_df)
    date_arr = complete_series_df_volume["Date"]
    complete_series_df_volume = complete_series_df_volume.drop(columns="Date")

    complete_series_df_vol_rolling = complete_series_df_volume.rolling(7).sum()
    complete_series_df_vol_rolling["Date"] = date_arr
    mongo_upload(complete_series_df_vol_rolling, "collection_volume_y")

# -----------------------------
# ADDING CRYPTOCURRENCIES DATA TO DATAFRAME
# ----------------------------

# function that adds the crypto prices or volume retrived from the "index"
# database. The default value of the varibale "collection" implies that
# the prices will be added, if the volumes are needed specify "crypto_volume"


def add_crypto(initial_df, collection="crypto_price"):

    if collection == "crypto_price":

        crypto_df = query_mongo("index", collection)
        yahoo_old_crypto, _ = crypto_old_series_y(START_DATE, "2015-12-31")

    elif collection == "crypto_volume":

        crypto_df = query_mongo("index", collection)
        _, yahoo_old_crypto = crypto_old_series_y(START_DATE, "2015-12-31")

    crypto_df = crypto_df[["Date", "BTC", "ETH", "LTC", "XRP", "BCH"]]
    crypto_df = crypto_df.rename({"BTC": "BITCOIN"})

    tot_crypto_df = yahoo_old_crypto.append(crypto_df, sort=True)
    tot_crypto_df.reset_index(drop=True, inplace=True)

    complete_df = pd.merge(initial_df, tot_crypto_df, on="Date", how="left")

    complete_df = complete_df[["Date",
                               "BTC",
                               "ETH",
                               "LTC",
                               "XRP",
                               "BCH",
                               'GOLD',
                               'SILVER',
                               'COPPER',
                               'NATURAL_GAS',
                               'CRUDE OIL',
                               'CORN',
                               'EUR',
                               'GBP',
                               'JPY',
                               'CHF',
                               'NASDAQ',
                               'DOWJONES',
                               'S&P500',
                               'EUROSTOXX50',
                               'VIX',
                               'US TREASURY',
                               'EUR Aggregate Bond',
                               'US Aggregate Bond',
                               'US index',
                               'TESLA',
                               'AMAZON',
                               'APPLE',
                               'NETFLIX'
                               ]]

    return complete_df


# function that allows to download from Yahoo Finance the historical series
# of crypto prior to 01/01/2016 (the starting date of "index" DB series)

def crypto_old_series_y(start, stop):

    yahoo_code = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'BCH-USD']

    yahoo_name = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH']

    (crypto_df_price,
     crypto_df_volume) = all_series_download(yahoo_code,
                                             yahoo_name,
                                             start, stop)

    return crypto_df_price, crypto_df_volume


# -----------------------------
# STABLECOIN VOLUME OPERATION
# ------------------------------

# function that allows to isolate the volumes of BTC related to stablecoins
# transaction (USDT and USDC only)

def stablecoin_volume(all_exc_df):

    date_arr = date_gen_TS("01-01-2016")

    stable_vol_df = pd.DataFrame(columns=["Date", "Volume"])
    stable_vol_df["Date"] = date_arr

    only_stable_usdc = all_exc_df.loc[all_exc_df.Pair == "btcusdc"]
    only_stable_usdt = all_exc_df.loc[all_exc_df.Pair == "btcusdt"]
    only_stable = only_stable_usdt.append(only_stable_usdc)

    for date in date_arr:

        only_stable_date = only_stable.loc[only_stable.Time == date]

        df_sum = only_stable_date.sum(axis=0, skipna=True)
        vol_sum = float(np.array(df_sum["Pair Volume"]))

        stable_vol_df.loc[stable_vol_df.Date == date, "Volume"] = vol_sum

    return stable_vol_df


# function that takes as input the df with all the exchanges values
# of volume and then subtracts the volumes related to stablecoins
# transactions

def crypto_vol_no_stable(all_exc_df):

    only_stable_vol = stablecoin_volume(all_exc_df)
    vol_arr = np.array(only_stable_vol["Volume"])

    total_crypto_vol = query_mongo(INDEX_DB_NAME, "crypto_volume")
    total_crypto_vol = total_crypto_vol[["Time", "Date", "BTC"]]

    total_crypto_vol["BTC"] = total_crypto_vol["BTC"].sub(vol_arr)

    return total_crypto_vol


# function that add to a given dataframe (initial_df) the data related
# to BTC volumes without stablecoins transaction

def add_no_stable(initial_df, no_stable_vol_df):

    no_stable_vol_df = no_stable_vol_df.drop(columns="Time")

    _, yahoo_old_crypto = crypto_old_series_y(START_DATE, "2015-12-31")

    crypto_df = yahoo_old_crypto[["Date", "BTC"]]

    tot_crypto_df = crypto_df.append(no_stable_vol_df, sort=True)
    tot_crypto_df.reset_index(drop=True, inplace=True)
    tot_crypto_df = tot_crypto_df.rename(columns={"BTC": "BTC no stable"})

    complete_df = pd.merge(initial_df, tot_crypto_df, on="Date", how="left")

    complete_df = complete_df[["Date",
                               "BTC",
                               "BTC no stable",
                               "ETH",
                               "LTC",
                               "XRP",
                               "BCH",
                               'GOLD',
                               'SILVER',
                               'COPPER',
                               'NATURAL_GAS',
                               'CRUDE OIL',
                               'CORN',
                               'EUR',
                               'GBP',
                               'JPY',
                               'CHF',
                               'NASDAQ',
                               'DOWJONES',
                               'S&P500',
                               'EUROSTOXX50',
                               'VIX',
                               'US TREASURY',
                               'EUR Aggregate Bond',
                               'US Aggregate Bond',
                               'US index',
                               'TESLA',
                               'AMAZON',
                               'APPLE',
                               'NETFLIX'
                               ]]

    return complete_df

# -----------------------
# MARKET CAP OPERATION
# -----------------------

# function that downloads the market cap information from Yahoo Finance


def mkt_cap_downloader(tickers_list, name_list):

    mkt_cap_df = pd.DataFrame()
    i = 0
    # yf.pdr_override()

    for str in tickers_list:

        name = name_list[i]
        market_cap = pd.DataFrame(
            {name: int(data.get_quote_yahoo(str)['marketCap'])}, index=[0])
        mkt_cap_df[name] = market_cap[name]

        i = i+1

    return mkt_cap_df


def mkt_cap_adder(mkt_cap_df, USD_SUPPLY,
                  GOLD_OUNCES_SUPPLY, SILVER_OUNCES_SUPPLY):

    mkt_cap_df["USD"] = USD_SUPPLY

    all_yahoo = query_mongo("btc_analysis", "all_prices_y")
    last_day_yahoo = all_yahoo.tail(2)
    last_day_yahoo = last_day_yahoo.head(1)

    gold_mkt_cap = GOLD_OUNCES_SUPPLY * np.array(last_day_yahoo["GOLD"])
    silver_mkt_cap = SILVER_OUNCES_SUPPLY * np.array(last_day_yahoo["SILVER"])

    mkt_cap_df["Gold"] = gold_mkt_cap
    mkt_cap_df["Silver"] = silver_mkt_cap

    return mkt_cap_df


def mkt_cap_op(tickers_list, name_list, yesterday_human):

    mkt_cap_df = mkt_cap_downloader(tickers_list, name_list)

    mkt_cap_df_comp = mkt_cap_adder(
        mkt_cap_df, USD_SUPPLY,
        GOLD_OUNCES_SUPPLY, SILVER_OUNCES_SUPPLY)

    btc_mkt_cap = mkt_cap_btc(yesterday_human)

    mkt_cap_df_comp["BTC"] = btc_mkt_cap

    mongo_upload(mkt_cap_df_comp, "collection_market_cap")


def mkt_cap_btc(yesterday_human):

    blockchain_stats_op()

    btc_supply_df = query_mongo("btc_analysis", "btc_total_supply")
    btc_supply_df_last = btc_supply_df.tail(1)

    query_btc_price = {"Date": yesterday_human}
    all_price_df = query_mongo("index", "crypto_price", query_btc_price)

    btc_price = np.array(all_price_df["BTC"])
    btc_supply = np.array(btc_supply_df_last["Supply"])

    btc_mkt_cap = btc_price * btc_supply

    return btc_mkt_cap


def mkt_cap_stable_op(tickers_list, name_list, yesterday_human):

    mkt_cap_stable = mkt_cap_downloader(tickers_list, name_list)

    return mkt_cap_stable


def ticker_price_downloader(tickers_list, name_list):

    ticker_price_df = pd.DataFrame()
    i = 0

    for str in tickers_list:

        name = name_list[i]
        ticker_price = pd.DataFrame(
            {name: int(data.get_quote_yahoo(str)['price'])}, index=[0])
        ticker_price_df[name] = ticker_price[name]

        i = i+1

    return ticker_price_df

# ------------------------
# BTC NETWORK
# -----------------------

# function that download data from blockchain.info website


def blockchain_stats_api():

    entrypoint = "https://api.blockchain.info/stats"

    response = requests.get(entrypoint)

    try:
        response = response.json()
        r = response
        sats_for_btc = 100000000
        timestamp = r["timestamp"]
        total_supply = r["totalbc"] / sats_for_btc
        total_blocks = r["n_blocks_total"]
        daily_btc = r["n_btc_mined"] / sats_for_btc
        daily_block = r["n_blocks_mined"]
        hash_rate = r["hash_rate"]
        difficulty = r["difficulty"]

        rawdata = {
            "Timestamp": timestamp,
            "Supply": total_supply,
            "Block Number": total_blocks,
            "Daily BTC": daily_btc,
            "Daily Block": daily_block,
            "Hash Rate": hash_rate,
            "Difficulty": difficulty,
        }

        return rawdata

    except KeyError:

        err = "This key doesn't exist"
        print(err)

        return err

    except json.decoder.JSONDecodeError:

        err = "No value in response"
        print(err)

        return err


def blockchain_stats_op():

    raw_data = blockchain_stats_api()

    raw_data_df = pd.DataFrame(raw_data, index=[0])

    mongo_upload(raw_data_df, "collection_btc_network")


def check_and_add_supply():

    yesterday = yesterday_str("%d-%m-%Y")

    df_from_csv = pd.read_csv(
        Path("source_data", "BTC_issuance.csv"), sep="|")
    last_day = df_from_csv.tail(1)
    last_date = np.array(last_day["Date"])[0]

    if last_date == yesterday:

        pass

    else:

        supply_df = query_mongo("btc_analysis", "btc_supply")
        day_issuance = np.array(supply_df["Daily BTC"])[0]
        day_block = np.array(supply_df["Daily Block"])[0]
        array_to_add = np.column_stack((yesterday, day_issuance, day_block))
        df_to_add = pd.DataFrame(array_to_add, columns=[
                                 "Date", "BTC Issuance", "BTC Blocks"])

        df_to_add.to_csv(Path("source_data", "BTC_issuance.csv"),
                         mode='a', index=False, header=False, sep='|')


def to_cumulative(issuance_df):

    complete_df = issuance_df.copy()
    complete_df["BTC Issuance"] = [float(x)
                                   for x in complete_df["BTC Issuance"]]
    complete_df["BTC Blocks"] = [float(x) for x in complete_df["BTC Blocks"]]
    complete_df["Supply"] = complete_df["BTC Issuance"].cumsum()
    complete_df["Total Blocks"] = complete_df["BTC Blocks"].cumsum()

    return complete_df


def theoretical_supply(df):

    final_df = df.copy()
    supply_array = np.array([])

    reward = 50
    block_threshold = 210000

    i = 0

    for daily_block in final_df["BTC Blocks"]:

        cum_to_check = final_df["Total Blocks"].iloc[i]

        if cum_to_check >= block_threshold:

            new_reward = cum_to_check - block_threshold
            old_reward = daily_block - new_reward

            daily_btc = old_reward * reward + new_reward * (reward / 2)

            block_threshold = block_threshold + 210000
            reward = reward / 2

        else:

            daily_btc = daily_block * reward

        supply_array = np.append(supply_array, daily_btc)
        # supply_array = np.row_stack((supply_array, daily_btc))
        i = i + 1

    final_df["Theoretical Issuance"] = supply_array
    final_df["Theoretical Supply"] = final_df["Theoretical Issuance"].cumsum()

    return final_df


def btc_supply_op(issuance_df):

    complete_df = to_cumulative(issuance_df)
    final_df = theoretical_supply(complete_df)

    return final_df


def check_and_add_daily(new_df, coll_to_look, coll_to_upload, type_="other"):

    if type_ == "other":

        yesterday = yesterday_str("%Y-%m-%d")

    elif type_ == "price":

        yesterday = yesterday_str("%d-%m-%Y")

    df_hist = query_mongo("btc_analysis", coll_to_look)
    last_day = df_hist.tail(1)
    last_date = np.array(last_day["Date"])[0]

    if last_date == yesterday:

        pass

    else:

        mongo_upload(new_df, coll_to_upload)


def check_missing_days(coll_to_look, type_="other"):

    if type_ == "other":

        yesterday = yesterday_str("%Y-%m-%d")

    elif type_ == "price":

        yesterday = yesterday_str("%d-%m-%Y")

    df_hist = query_mongo("btc_analysis", coll_to_look)

    last_day = df_hist.tail(1)
    last_date = np.array(last_day["Date"])[0]
    print(last_date)
    list_of_days = date_gen(last_date, yesterday)
    print(list_of_days)
    list_of_days.pop(0)

    return list_of_days

    
# ----------------------
# HISTORICAL VOLATILITY
# ----------------------


def historical_vola(return_df, logret_df, window_days):

    date = return_df["Date"]
    date = date.sort_values(ascending=True)
    date.reset_index(drop=True, inplace=True)

    logret_df.fillna(0, inplace=True)

    hist_vola = hist_std_dev(logret_df, window=window_days)
    hist_vola["Date"] = date
    hist_vola = hist_vola.tail(len(date) - window_days)
    hist_vola.reset_index(drop=True, inplace=True)

    return hist_vola


def ewm_volatility(return_df, square_root=252):

    date = return_df["Date"]
    date = date.sort_values(ascending=True)
    date.reset_index(drop=True, inplace=True)

    span = len(np.array(return_df["BTC"])) - 1

    ewm_vola_df = return_df.ewm(span=span).std() * np.sqrt(square_root)
    ewm_vola_df["Date"] = date

    return ewm_vola_df


# --------------------------
# BTC Derivatives

def daily_btc_fut_download():

    y_str = yesterday_str()
    CME_df = single_series_download("BTC=F", "2021-01-01", y_str)
    print(CME_df)
    CME_vol = np.array(CME_df["Volume"])[0]
    Bakkt_df = single_series_download("BTM=F", "2021-01-01", y_str)
    print(Bakkt_df)
    Bakkt_vol = np.array(Bakkt_df["Volume"])[0]

    fut_arr = np.column_stack((y_str, CME_vol, Bakkt_vol))
    final_df = pd.DataFrame(fut_arr, columns=["Date", "CME", "Bakkt"])

    return final_df


def btc_fut_downloader(tickers_list, name_list):

    fut_df = pd.DataFrame()
    yesterday = yesterday_str()

    i = 0

    for str in tickers_list:

        name = name_list[i]
        returned = pd.DataFrame(
            {name: int(data.get_data_yahoo(str, start=yesterday_str_,
                                           end=yesterday_str_)["Volume"])}, index=[0])
        print(returned)
        fut_df[name] = returned[name]

        i = i+1

    return fut_df


# def derivatives_rearrange(initial_df):

#     initial_df["Date"] = [datetime.strptime(x, "%Y-%m-%d") for x in initial_df["Date"]]

#     initial_df["Year"] = [d.year for d in initial_df["Date"]]

#     initial_df["Month"] = [d.month for d in initial_df["Date"]]

#     initial_df["Month-Year"] =


#     return final_df


def quarter_date_start(initial_year):

    yesterday_ = yesterday_str()
    yesterday_date = datetime.strptime(yesterday_, "%Y-%m-%d")
    current_year = int(yesterday_date.year)

    q_list = yearly_quarter_start(int(initial_year))

    if int(initial_year) < current_year:

        for y in range(int(initial_year) + 1, current_year + 1):

            new_list = yearly_quarter_start(y)
            q_list.extend(new_list)

    return start_q_list


def quarter_date_end(start_q_list):

    delta = relativedelta(days=-1)

    start_q_list_ = [datetime.strptime(x, "%Y-%m-%d") for x in start_q_list]

    end_q_list_ = [d + delta for d in start_q_list_]

    end_q_list = [x.strftime("%Y-%m-%d") for x in end_q_list_]

    return end_q_list


def yearly_quarter_start(year):

    first = "01-01-" + str(year)
    second = "01-04-" + str(year)
    third = "01-07-" + str(year)
    fourth = "01-10-" + str(year)

    yearly_q_list = [first, second, third, fourth]

    return yearly_q_list


# ---------------------------
# Derivatives

def btc_der_op(series_code_list, all_el_list_d,
               all_el_list_r,
               start_period, end_period):

    _, series_df_volume = all_series_download(series_code_list,
                                              all_el_list_d,
                                              start_period,
                                              end_period)

    # volume operation

    no_stable_vol_df = crypto_vol_no_stable(df_all_pair)
    complete_series_df_volume = add_no_stable(
        complete_series_df_volume, no_stable_vol_df)
    date_arr = complete_series_df_volume["Date"]
    complete_series_df_volume = complete_series_df_volume.drop(columns="Date")

    complete_series_df_vol_rolling = complete_series_df_volume.rolling(7).sum()
    complete_series_df_vol_rolling["Date"] = date_arr
    mongo_upload(complete_series_df_vol_rolling, "collection_volume_y")
