import pandas as pd
from datetime import datetime

from btc_analysis.mongo_func import query_mongo
from btc_analysis.market_data import yesterday_str
from btc_analysis.calc import last_quarter_end


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

    static_df = reunite_df(window_list, "yahoo", "static")

    return static_df


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
