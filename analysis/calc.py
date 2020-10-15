import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import (
    CRYPTO_LIST, REF_CRYPTO, REF_VARIOUS,
    VARIOUS_LIST, DB_NAME
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


def static_corr(return_df, time_window):

    first_row = return_df.head(1)
    first_date = str(first_row["Date"].to_numpy()[0])

    delta_date = roll_single_time(first_date, time_window)

    df_to_compute = return_df.loc[return_df.Date.between(
        delta_date, first_date, inclusive=True)]

    corr_matrix = df_to_compute.corr()

    return corr_matrix


def static_corr_op(return_df):

    static_3Y = static_corr(return_df, "3Y")
    static_1Y = static_corr(return_df, "1Y")
    static_1Q = static_corr(return_df, "1Q")
    static_1M = static_corr(return_df, "1M")

    return static_3Y, static_1Y, static_1Q, static_1M


def dynamic_corr_op(return_df, corr_set):

    corr_3Y = dynamic_total(return_df, "3Y", corr_set)
    corr_1Y = dynamic_total(return_df, "1Y", corr_set)
    corr_1Q = dynamic_total(return_df, "1Q", corr_set)
    corr_1M = dynamic_total(return_df, "1M", corr_set)

    return corr_3Y, corr_1Y, corr_1Q, corr_1M


def return_retrieve(collection):

    return_df = query_mongo(DB_NAME, collection)
    return_df = return_df.sort_values(by=["Date"], ascending=False)
    return_df.reset_index(drop=True, inplace=True)

    return return_df


def correlation_op():

    mongo_correlation_drop()

    alt_ret_df = return_retrieve("return_crypto")
    var_ret_df = return_retrieve("return_various")

    # dynamic correlations
    (dyn_alt_corr_3Y, dyn_alt_corr_1Y,
     dyn_alt_corr_1Q, dyn_alt_corr_1M) = dynamic_corr_op(
        alt_ret_df, "altcoin")

    (dyn_var_corr_3Y, dyn_var_corr_1Y,
     dyn_var_corr_1Q, dyn_var_corr_1M) = dynamic_corr_op(
         var_ret_df, "various")

    # static correlations
    (stat_alt_corr_3Y, stat_alt_corr_1Y,
     stat_alt_corr_1Q, stat_alt_corr_1M) = static_corr_op(alt_ret_df)

    (stat_var_corr_3Y, stat_var_corr_1Y,
     stat_var_corr_1Q, stat_var_corr_1M) = static_corr_op(var_ret_df)

    mongo_upload(dyn_alt_corr_3Y, "collection_3Y_dyn_alt")
    mongo_upload(dyn_alt_corr_1Y, "collection_1Y_dyn_alt")
    mongo_upload(dyn_alt_corr_1Q, "collection_1Q_dyn_alt")
    mongo_upload(dyn_alt_corr_1M, "collection_1M_dyn_alt")

    mongo_upload(dyn_var_corr_3Y, "collection_3Y_dyn_var")
    mongo_upload(dyn_var_corr_1Y, "collection_1Y_dyn_var")
    mongo_upload(dyn_var_corr_1Q, "collection_1Q_dyn_var")
    mongo_upload(dyn_var_corr_1M, "collection_1M_dyn_var")

    mongo_upload(stat_alt_corr_3Y, "collection_3Y_stat_alt")
    mongo_upload(stat_alt_corr_1Y, "collection_1Y_stat_alt")
    mongo_upload(stat_alt_corr_1Q, "collection_1Q_stat_alt")
    mongo_upload(stat_alt_corr_1M, "collection_1M_stat_alt")

    mongo_upload(stat_var_corr_3Y, "collection_3Y_var_alt")
    mongo_upload(stat_var_corr_1Y, "collection_1Y_var_alt")
    mongo_upload(stat_var_corr_1Q, "collection_1Q_var_alt")
    mongo_upload(stat_var_corr_1M, "collection_1M_var_alt")
