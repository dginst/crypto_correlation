import pandas as pd
from datetime import datetime, date

from btc_analysis.mongo_func import query_mongo, mongo_upload
from btc_analysis.market_data import yesterday_str
from btc_analysis.calc import last_quarter_end

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

    static_df = reunite_df(window_list, "yahoo", "static")

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
