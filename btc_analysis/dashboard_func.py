import pandas as pd
from btc_analysis.mongo_func import (
    query_mongo
)


def btc_total_dfs(window_list, operation):

    if operation == "btc_denominated":

        altcoin_df = reunite_df(window_list, "altcoin", "btc_denominated")
        yahoo_df = reunite_df(window_list, "yahoo", "btc_denominated")

    elif operation == "correlation":

        yahoo_df = reunite_df(window_list, "yahoo", "correlation")
        altcoin_df = reunite_df(window_list, "alt", "correlation")

    return altcoin_df, yahoo_df


def usd_den_total_df(window_list):

    total_df = reunite_df(window_list, "other", "usd_denominated")

    return total_df


def vola_total_df(days_list):

    total_df = reunite_df(days_list, "other", "volatility")

    return total_df


def reunite_df(window_list, typology, op):

    col_set = column_set_finder(typology, op)
    unified_df = pd.DataFrame(columns=col_set)

    for w in window_list:

        df = retrieve_and_add(w, typology, op)
        unified_df = unified_df.append(df)

    return unified_df


def retrieve_and_add(window, typology, op):

    if op == "correlation":

        coll = "dyn" + "_" + typology + "_" + "correlation" + "_" + window

    elif op == "btc_denominated":

        coll = typology + "_" + "btc_denominated" + "_" + window

    elif op == "usd_denominated":

        coll = "normalized_prices_" + window

    elif op == "volatility":

        coll = "volatility_" + window

    df = query_mongo("btc_analysis", coll)

    if op == "volatility":

        df["Days"] = window

    else:

        df["Window"] = window

    return df


def column_set_finder(typology, op):

    if op == "correlation":

        coll = "dyn" + "_" + typology + "_" + "correlation" + "_1M"

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
