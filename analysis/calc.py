import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import (
    CRYPTO_LIST, REF_CRYPTO, REF_VARIOUS,
    VARIOUS_LIST, DB_NAME, VAR_STATIC_LIST,
    REF_SP500, VS_SP500_LIST
)
from mongo_func import (
    mongo_correlation_drop, query_mongo,
    mongo_upload
)


def dynamic_total(tot_ret_df, time_window, corr_set):

    tot_corr = tot_ret_df[["Date"]]

    if corr_set == "altcoin":

        ref_variable = REF_CRYPTO
        others_comm = CRYPTO_LIST

    elif corr_set == "various":

        ref_variable = REF_VARIOUS
        others_comm = VARIOUS_LIST

    elif corr_set == "SP500":

        ref_variable = REF_SP500
        others_comm = VS_SP500_LIST

    ref_comm_df = tot_ret_df[["Date", ref_variable]]

    try:

        others_comm.remove(ref_variable)

    except ValueError:
        pass

    for element in others_comm:

        comm_df = tot_ret_df[["Date", element]]

        single_corr = dynamic_corr(ref_comm_df, comm_df, time_window)
        single_corr.reset_index(drop=True, inplace=True)

        tot_corr[element] = single_corr[element]

    return tot_corr


def dynamic_corr(first_df, second_df, time_window):

    column_set = list(second_df.columns)

    try:
        column_set.remove("Date")
    except ValueError:
        pass

    corr_series = pd.DataFrame(columns=column_set)

    for date in first_df["Date"]:

        delta_date = roll_single_time(date, time_window)

        sub_first_df = first_df.loc[first_df.Date.between(
            delta_date, date, inclusive=True)]

        sub_second_df = second_df.loc[second_df.Date.between(
            delta_date, date, inclusive=True)]

        merged = pd.merge(sub_first_df, sub_second_df, on=["Date"])

        merged = merged.drop(columns=["Date"])

        day_corr = merged.corr()

        value_of_int = day_corr.iloc[[0], [1]]

        corr_series = corr_series.append(value_of_int)

    return corr_series


def roll_single_time(date, time_window):

    date = datetime.strptime(date, "%Y-%m-%d")

    if time_window == "1Y":

        delta = relativedelta(months=-12)

    elif time_window == "3Y":

        delta = relativedelta(months=-36)

    elif time_window == "1Q":

        delta = relativedelta(months=-3)

    elif time_window == "1M":

        delta = relativedelta(months=-1)

    date_delta = date + delta

    date_delta = date_delta.strftime("%Y-%m-%d")

    return date_delta


def roll_time_arr(date_arr, time_window):

    date_delta = pd.DataFrame(date_arr, columns=["Date"])

    date_delta["Date"] = [datetime.strptime(
        x, "%Y-%m-%d") for x in date_delta["Date"]]

    if time_window == "1Y":

        delta = relativedelta(months=-12)

    elif time_window == "3Y":

        delta = relativedelta(months=-36)

    elif time_window == "1Q":

        delta = relativedelta(months=-3)

    elif time_window == "1M":

        delta = relativedelta(months=-1)

    date_delta["Delta Date"] = [x + delta for x in date_delta["Date"]]

    return date_delta


def static_corr(return_df, time_window=None):

    if time_window is None:

        df_to_compute = return_df

    else:

        first_row = return_df.head(1)
        first_date = str(first_row["Date"].to_numpy()[0])

        delta_date = roll_single_time(first_date, time_window)

        df_to_compute = return_df.loc[return_df.Date.between(
            delta_date, first_date, inclusive=True)]

    corr_matrix = df_to_compute.corr()

    return corr_matrix


def static_corr_op(return_df):

    static_all = static_corr(return_df)
    static_3Y = static_corr(return_df, "3Y")
    static_1Y = static_corr(return_df, "1Y")
    static_1Q = static_corr(return_df, "1Q")
    static_1M = static_corr(return_df, "1M")

    return static_all, static_3Y, static_1Y, static_1Q, static_1M


def dynamic_corr_op(return_df, corr_set):

    corr_3Y = dynamic_total(return_df, "3Y", corr_set)
    corr_1Y = dynamic_total(return_df, "1Y", corr_set)
    corr_1Q = dynamic_total(return_df, "1Q", corr_set)
    corr_1M = dynamic_total(return_df, "1M", corr_set)

    return corr_3Y, corr_1Y, corr_1Q, corr_1M


def return_retrieve(collection, corr_type=None):

    return_df = query_mongo(DB_NAME, collection)
    return_df = return_df.sort_values(by=["Date"], ascending=False)

    if collection == "return_crypto":

        for coin in CRYPTO_LIST:

            return_df[coin] = [float(x) for x in return_df[coin]]

    elif collection == "return_various":

        if corr_type is None:

            for var in VARIOUS_LIST:

                return_df[var] = [float(x) for x in return_df[var]]

        elif corr_type == "SP500":

            for var in VS_SP500_LIST:

                return_df[var] = [float(x) for x in return_df[var]]

    return_df.reset_index(drop=True, inplace=True)

    return return_df


def static_return_adj(var_ret_df, alt_ret_df):

    btc_series = alt_ret_df[["Date", "BTC"]]
    eth_series = alt_ret_df[["Date", "ETH"]]
    ltc_series = alt_ret_df[["Date", "LTC"]]
    xrp_series = alt_ret_df[["Date", "XRP"]]

    var_date = var_ret_df["Date"]

    merged_btc = pd.merge(var_date, btc_series, on="Date")
    merged_eth = pd.merge(var_date, eth_series, on="Date")
    merged_ltc = pd.merge(var_date, ltc_series, on="Date")
    merged_xrp = pd.merge(var_date, xrp_series, on="Date")

    merged_btc = merged_btc.drop(columns="Date")
    merged_eth = merged_eth.drop(columns="Date")
    merged_ltc = merged_ltc.drop(columns="Date")
    merged_xrp = merged_xrp.drop(columns="Date")

    var_ret_df[""] = merged_eth  # modified, check the logic
    var_ret_df["ETH"] = merged_eth
    var_ret_df["LTC"] = merged_ltc
    var_ret_df["XRP"] = merged_xrp

    adj_ret_df = var_ret_df[VAR_STATIC_LIST]

    return adj_ret_df


def correlation_op():

    # mongo_correlation_drop()

    # alt_ret_df = return_retrieve("return_crypto")
    var_ret_df = return_retrieve("return_various")
    SP500_ret_df = return_retrieve("return_various", corr_type="SP500")

    # var_ret_comp_df = static_return_adj(var_ret_df, alt_ret_df)

    # dynamic correlations
    # (dyn_alt_corr_3Y, dyn_alt_corr_1Y,
    #  dyn_alt_corr_1Q, dyn_alt_corr_1M) = dynamic_corr_op(
    #     alt_ret_df, "altcoin")

    # (dyn_var_corr_3Y, dyn_var_corr_1Y,
    #  dyn_var_corr_1Q, dyn_var_corr_1M) = dynamic_corr_op(
    #      var_ret_df, "various")

    (dyn_SP500_corr_3Y, dyn_SP500_corr_1Y,
     dyn_SP500_corr_1Q, dyn_SP500_corr_1M) = dynamic_corr_op(
        SP500_ret_df, "SP500")

    # static correlations
    # (stat_alt_corr_all, stat_alt_corr_3Y, stat_alt_corr_1Y,
    #  stat_alt_corr_1Q, stat_alt_corr_1M) = static_corr_op(alt_ret_df)

    # (stat_var_corr_all, stat_var_corr_3Y, stat_var_corr_1Y,
    #  stat_var_corr_1Q, stat_var_corr_1M) = static_corr_op(var_ret_comp_df)

    # upload collections on MongoDB
    # mongo_upload(dyn_alt_corr_3Y, "collection_3Y_dyn_alt")
    # mongo_upload(dyn_alt_corr_1Y, "collection_1Y_dyn_alt")
    # mongo_upload(dyn_alt_corr_1Q, "collection_1Q_dyn_alt")
    # mongo_upload(dyn_alt_corr_1M, "collection_1M_dyn_alt")

    # mongo_upload(dyn_var_corr_3Y, "collection_3Y_dyn_var")
    # mongo_upload(dyn_var_corr_1Y, "collection_1Y_dyn_var")
    # mongo_upload(dyn_var_corr_1Q, "collection_1Q_dyn_var")
    # mongo_upload(dyn_var_corr_1M, "collection_1M_dyn_var")

    mongo_upload(dyn_SP500_corr_3Y, "collection_3Y_dyn_SP500")
    mongo_upload(dyn_SP500_corr_1Y, "collection_1Y_dyn_SP500")
    mongo_upload(dyn_SP500_corr_1Q, "collection_1Q_dyn_SP500")
    mongo_upload(dyn_SP500_corr_1M, "collection_1M_dyn_SP500")

    # mongo_upload(stat_alt_corr_all, "collection_all_stat_alt")
    # mongo_upload(stat_alt_corr_3Y, "collection_3Y_stat_alt")
    # mongo_upload(stat_alt_corr_1Y, "collection_1Y_stat_alt")
    # mongo_upload(stat_alt_corr_1Q, "collection_1Q_stat_alt")
    # mongo_upload(stat_alt_corr_1M, "collection_1M_stat_alt")

    # mongo_upload(stat_var_corr_all, "collection_all_stat_var")
    # mongo_upload(stat_var_corr_3Y, "collection_3Y_stat_var")
    # mongo_upload(stat_var_corr_1Y, "collection_1Y_stat_var")
    # mongo_upload(stat_var_corr_1Q, "collection_1Q_stat_var")
    # mongo_upload(stat_var_corr_1M, "collection_1M_stat_var")
