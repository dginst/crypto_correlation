from datetime import datetime

import numpy as np
import pandas as pd

from btc_analysis.calc import last_q_end_word, last_quarter_end
from btc_analysis.market_data import yesterday_str
from btc_analysis.mongo_func import mongo_upload, query_mongo

# -------------------


def btc_total_dfs(window_list, operation):

    if operation == "btc_denominated":

        altcoin_df = reunite_df(window_list, "altcoin",
                                "btc_denominated", quarter="Y")
        yahoo_df = reunite_df(window_list, "yahoo",
                              "btc_denominated", quarter="Y")

    elif operation == "correlation":

        yahoo_df = reunite_df(window_list, "yahoo", "correlation")
        altcoin_df = reunite_df(window_list, "alt", "correlation")

    return altcoin_df, yahoo_df


def usd_den_total_df(window_list):

    total_df = reunite_df(window_list, "other", "usd_denominated", quarter="Y")

    return total_df


def vola_total_df(days_list):

    total_df = reunite_df(days_list, "other", "volatility")

    return total_df


def static_corr_df(window_list):

    static_df = reunite_df(window_list, "yahoo", "static_y", quarter="Y")

    return static_df


# --------------


def reunite_df(window_list, typology, op, quarter="N"):

    col_set = column_set_finder(typology, op)
    unified_df = pd.DataFrame(columns=col_set)

    for w in window_list:

        df = retrieve_and_add(w, typology, op)
        unified_df = unified_df.append(df)

        if quarter == "Y":

            df_q = retrieve_and_add(w, typology, op, as_of="_quarter")
            unified_df = unified_df.append(df_q)

    return unified_df


def retrieve_and_add(window, typology, op, as_of=""):

    if op == "correlation":

        coll = "dyn" + "_" + typology + "_" + "correlation" + "_" + window

    elif op == "static":

        coll = "stat" + "_" + typology + "_" + "correlation" + "_" + window

    elif op == "static_y":

        coll = "stat" + "_" + typology + "_" + "correlation" + "_" + window + as_of
        print(coll)

    elif op == "btc_denominated":

        coll = typology + "_" + "btc_denominated" + "_" + window + as_of

    elif op == "usd_denominated":

        coll = "normalized_prices_" + window + as_of

    elif op == "volatility":

        coll = "volatility_" + window

    df = query_mongo("btc_analysis", coll)

    if op == "volatility":

        df["Days"] = window

    else:

        df["Window"] = window

    if as_of == "":

        df["As Of"] = yesterday_str()

    else:

        df["As Of"] = last_quarter_end()  # .strftime("%d-%m-%Y")

    return df


def column_set_finder(typology, op):

    if op == "correlation":

        coll = "dyn" + "_" + typology + "_" + "correlation" + "_1M"

    elif op == "static_y":

        coll = "stat" + "_" + typology + "_" + "correlation" + "_1M"

    elif op == "static":

        coll = "stat" + "_" + typology + "_" + "correlation" + "_1M"

    elif op == "btc_denominated":

        coll = typology + "_" + "btc_denominated" + "_1M"

    elif op == "usd_denominated":

        coll = "normalized_prices_1M"

    elif op == "volatility":

        coll = "volatility_30"

    df_col = query_mongo("btc_analysis", coll)

    if op == "volatility":

        df_col["Days"] = "30"

    else:

        df_col["Window"] = "1M"

    col_set = df_col.columns

    return col_set


# ------------
# correlation and btc denominated dfs unification and upload


def dash_btc_den_df(window_list):

    crypto_df, yahoo_df = btc_total_dfs(window_list, "btc_denominated")
    mongo_upload(crypto_df, "collection_dash_btc_den_crypto")
    mongo_upload(yahoo_df, "collection_dash_btc_den_yahoo")


def dash_correlation_df(window_list):

    crypto_df, yahoo_df = btc_total_dfs(window_list, "correlation")
    mongo_upload(crypto_df, "collection_dash_corr_crypto")
    mongo_upload(yahoo_df, "collection_dash_corr_yahoo")


def dash_usd_den_df(window_list):

    usd_den_tot = usd_den_total_df(window_list)
    mongo_upload(usd_den_tot, "collection_dash_usd_den")


def dash_volatility_df(days_list):

    vola_df = vola_total_df(days_list)
    mongo_upload(vola_df, "collection_dash_volatility")


def dash_static_corr_df(window_list):

    static_df = static_corr_df(window_list)
    mongo_upload(static_df, "collection_dash_static_corr")


# -------------

def date_elements():

    yesterday = yesterday_str()

    max_year = int(datetime.strptime(yesterday, "%Y-%m-%d").year)
    max_month = int(datetime.strptime(yesterday, "%Y-%m-%d").month)
    max_day = int(datetime.strptime(yesterday, "%Y-%m-%d").day)

    return max_year, max_month, max_day


# ------
# BTC statistics and network functions

def btc_price_min(price_df):

    price_df["Year"] = [int(x.year) for x in price_df["Datetime"]]

    list_of_year = list(np.array(price_df["Year"].unique()))

    minimum_arr = np.array([])
    date_arr = np.array([])
    value_arr = np.array([])

    for y in list_of_year:

        y_price = np.array(price_df.loc[price_df.Year == y, "BTC Price"])

        min_val = min(y_price)

        min_date = np.array(price_df.loc[price_df["BTC Price"]
                                         == min_val, "Datetime"])[0]

        min_date = pd.to_datetime(str(min_date))
        min_date = min_date.strftime('%Y-%m-%d')

        date_arr = np.append(date_arr, min_date)
        value_arr = np.append(value_arr, min_val)

    minimum_arr = np.column_stack((date_arr, value_arr))

    minimum_df = pd.DataFrame(minimum_arr, columns=["Date", "BTC Price"])
    minimum_df["Datetime"] = [datetime.strptime(
        d, '%Y-%m-%d') for d in minimum_df["Date"]]

    minimum_df["Year"] = [int(x.year) for x in minimum_df["Datetime"]]
    minimum_df = minimum_df.drop_duplicates(subset=["Year"])
    minimum_df = minimum_df.drop(columns=["Year"])

    return minimum_df


# -------
# performances for table

def perf_df_creator(initial_df):

    list_of_asset = np.array(list(initial_df.columns))

    first_row = np.array(initial_df.head(1))
    last_row = np.array(initial_df.tail(1))

    num = last_row - first_row

    perf_arr = (num / first_row) * 100

    final_arr = np.column_stack((list_of_asset, perf_arr.T))

    final_df = pd.DataFrame(final_arr, columns=["Crypto-Asset", "Performance"])

    return final_df


def btc_yearly_perf(initial_df):

    initial_df["Year"] = [int(d.year) for d in initial_df["Datetime"]]

    yesterday_str_ = yesterday_str("%d-%m-%Y")
    yesterday_date = datetime.strptime(yesterday_str_, "%d-%m-%Y")
    day_curr = int(yesterday_date.day)
    month_curr = int(yesterday_date.month)
    year_curr = int(yesterday_date.year)

    last_quarter = last_q_end_word()
    last_q_date = datetime.strptime(last_quarter_end(), "%d-%m-%Y")
    last_q_date_ = last_q_date.strftime("%d-%m-%Y")

    list_of_year = list(np.array(initial_df["Year"].unique()))

    tot_arr = np.array([])
    year_arr = np.array([])
    value_arr = np.array([])
    perf_arr = np.array([])

    for y in list_of_year:

        y_df = initial_df.loc[initial_df.Year == y, "BTC Price"]
        y_df_plus = initial_df.loc[initial_df.Year == y]

        if y == year_curr:

            if month_curr <= 3:

                if month_curr == 1:

                    m_ = "Jan"

                elif month_curr == 2:

                    m_ = "Feb"

                elif month_curr == 3:

                    m_ = "Mar"

                date_string = str(day_curr) + " " + m_ + " " + str(y)
                y_last = np.array(
                    y_df_plus.loc[y_df_plus.Date == yesterday_str_, "BTC Price"])[0]

            else:

                date_string = last_quarter
                y_last = np.array(
                    y_df_plus.loc[y_df_plus.Date == last_q_date_, "BTC Price"])[0]

        else:

            date_string = "31 Dec " + str(y)
            y_last = np.array(y_df.tail(1))[0]

        y_first = np.array(y_df.head(1))[0]

        y_perf = ((y_last - y_first) / y_first)*100

        year_arr = np.append(year_arr, date_string)
        value_arr = np.append(value_arr, y_last)
        perf_arr = np.append(perf_arr, y_perf)

    tot_arr = np.column_stack((year_arr, value_arr, perf_arr))

    final_df = pd.DataFrame(
        tot_arr, columns=["Date", "Price", "Yearly Performance"])

    return final_df
