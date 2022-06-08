from datetime import datetime, timezone

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from btc_analysis.config import (ASSET_LIST, CRYPTO_LIST, DB_NAME, REF_CRYPTO, REF_SP500,
                                 REF_VARIOUS, VAR_STATIC_LIST, VARIOUS_LIST,
                                 VARIOUS_LIST_Y, VS_SP500_LIST)
from btc_analysis.mongo_func import mongo_upload, query_mongo

# -----------------------
# TIME FUNCTIONS
# -----------------------

# function that generate an array of date in timstamp format starting from
# start_date to end_date given in mm-dd-yyyy format;
# if not specified end_date = today()
# function only returns timestamp value in second since epoch where every
# day is in the exact 12:00 am UTC
# function considers End of Day price series so, if not otherwise specified,
# the returned array of date will be from start to today - 1 (EoD = 'Y')


def date_gen_TS(start_date, end_date=None, timeST="Y", clss="array", EoD="Y"):

    if end_date is None:

        end_date = datetime.now().strftime("%m-%d-%Y")

    date_index = pd.date_range(start_date, end_date)

    if timeST == "Y":

        date_ll = [
            int(date.replace(tzinfo=timezone.utc).timestamp()) for date in date_index
        ]

    else:

        date_ll = [datetime.strftime(date, "%m-%d-%Y") for date in date_index]

    if clss == "array":

        date_ll = np.array(date_ll)

    if EoD == "Y":

        date_ll = date_ll[: len(date_ll) - 1]

    return date_ll


def date_gen(start_date, end_date, holiday="Y"):

    if holiday == "N":

        date_index = pd.bdate_range(start_date, end_date)
        date_list = [datetime.strftime(
            date, "%Y-%m-%d") for date in date_index]

    else:

        date_index = pd.date_range(start_date, end_date)
        print(date_index)
        date_list = [datetime.strftime(date, "%Y-%m-%d")
                     for date in date_index]

    return date_list


def roll_single_time(date, time_window):

    try:

        date = datetime.strptime(date, "%Y-%m-%d")

    except ValueError:

        date = datetime.strptime(date, "%d-%m-%Y")

    if time_window == "1Y":

        delta = relativedelta(months=-12)

    elif time_window == "5Y":

        delta = relativedelta(months=-60)

    elif time_window == "2Y":

        delta = relativedelta(months=-24)

    elif time_window == "3Y":

        delta = relativedelta(months=-36)

    elif (time_window == "1Q") or (time_window == "3M"):

        delta = relativedelta(months=-3)

    elif time_window == "6M":

        delta = relativedelta(months=-6)

    elif time_window == "1M":

        delta = relativedelta(months=-1)

    elif time_window == "1D":

        delta = relativedelta(days=-1)

    elif time_window == "1W":

        delta = relativedelta(days=-7)

    elif time_window == "YTD":

        curr_year = str(date.year)
        ytd = curr_year + "-01-01"
        date_ytd = datetime.strptime(ytd, "%Y-%m-%d")

    if time_window == "YTD":

        date_delta = date_ytd
        date_delta = date_delta.strftime("%Y-%m-%d")

    else:

        date_delta = date + delta
        date_delta = date_delta.strftime("%Y-%m-%d")

    return date_delta


def roll_time_arr(date_arr, time_window):

    date_delta = pd.DataFrame(date_arr, columns=["Date"])

    date_delta["Date"] = [datetime.strptime(
        x, "%Y-%m-%d") for x in date_delta["Date"]]

    if time_window == "1Y":

        delta = relativedelta(months=-12)

    elif time_window == "2Y":

        delta = relativedelta(months=-24)

    elif time_window == "5Y":

        delta = relativedelta(months=-60)

    elif time_window == "3Y":

        delta = relativedelta(months=-36)

    elif time_window == "1Q":

        delta = relativedelta(months=-3)

    elif time_window == "1M":

        delta = relativedelta(months=-1)

    date_delta["Delta Date"] = [x + delta for x in date_delta["Date"]]

    return date_delta


def window_period_back(date_df, time_window, quarter="N"):

    if quarter == "N":

        last_date = max(date_df)

    else:

        last_date = last_quarter_end()

    first_date = roll_single_time(last_date, time_window)

    while first_date in date_df:

        first_date = roll_single_time(first_date, "1D")

    return first_date, last_date


def last_quarter_end(out="string"):

    today_month = int(datetime.now().month)
    today_year = int(datetime.now().year)
    last_year = today_year - 1

    if today_month <= 3:

        quart = "31-12-" + str(last_year)

    elif today_month <= 6:

        quart = "31-03-" + str(today_year)

    elif today_month <= 9:

        quart = "30-06-" + str(today_year)

    elif today_month <= 12:

        quart = "30-09-" + str(today_year)

    if out == "string":

        last_q_date_end = quart

    elif out == "date":

        last_q_date_end = datetime.strptime(quart, "%d-%m-%Y")

    elif out == "str_excel":

        last_q_date_end = quart[:2] + "_" + quart[3:5] + "_" + quart[6:]

    return last_q_date_end


def last_q_end_word():

    today_month = int(datetime.now().month)
    today_year = int(datetime.now().year)
    last_year = today_year - 1

    if today_month <= 3:

        quart = "31 Dec " + str(last_year)

    elif today_month <= 6:

        quart = "31 Mar " + str(today_year)

    elif today_month <= 9:

        quart = "30 Jun " + str(today_year)

    elif today_month <= 12:

        quart = "30 Sep " + str(today_year)

    last_q_date_end = quart

    return last_q_date_end


def quarter_from_date(df, col_name):

    dff = df.copy()
    dff[col_name] = [datetime.strptime(d, "%d-%m-%Y") for d in dff[col_name]]

    first_date = np.array(dff[col_name].head(1))[0]
    last_date = np.array(dff[col_name].tail(1))[0]

    year_list = [d.year for d in dff[col_name]]
    year_list = list(dict.fromkeys(year_list))

    all_quarter = quarter_list(year_list)

    sel_quarter = all_quarter.loc[all_quarter.Quarter > first_date]
    sel_quarter = sel_quarter.loc[sel_quarter.Quarter <= last_date]

    return sel_quarter


def quarter_list(year_list):

    quarter_array = np.array([])

    for y in year_list:

        q1 = "31-03-" + str(y)
        quarter_array = np.append(quarter_array, q1)
        q2 = "30-06-" + str(y)
        quarter_array = np.append(quarter_array, q2)
        q3 = "30-09-" + str(y)
        quarter_array = np.append(quarter_array, q3)
        q4 = "31-12-" + str(y)
        quarter_array = np.append(quarter_array, q4)

    quarter_df_date = pd.DataFrame(quarter_array, columns=["Quarter"])
    quarter_df_date["Quarter"] = [datetime.strptime(
        d, "%d-%m-%Y") for d in quarter_df_date["Quarter"]]

    return quarter_df_date


def add_quarter(df, col_name):

    new_df = df.copy()

    try:

        new_df[col_name] = [datetime.strptime(
            d, "%d-%m-%Y") for d in new_df[col_name]]

    except TypeError:
        pass

    quarter_arr = np.array([])

    for el in new_df[col_name]:

        if el.month <= 3:
            quarter_arr = np.append(quarter_arr, "Q1")

        elif el.month <= 6:
            quarter_arr = np.append(quarter_arr, "Q2")

        elif el.month <= 9:
            quarter_arr = np.append(quarter_arr, "Q3")

        else:
            quarter_arr = np.append(quarter_arr, "Q4")

    new_df["Quarter String"] = quarter_arr
    try:

        new_df["Year-Quarter"] = new_df["Year"].astype(
            str) + "-" + new_df["Quarter String"]

    except KeyError:

        new_df["Year"] = [int(x.year) for x in new_df[col_name]]
        new_df["Year-Quarter"] = new_df["Year"].astype(
            str) + "-" + new_df["Quarter String"]

    return new_df

# ----------------------------------
# RETURN RETRIEVE AND SETUP OPERATION
# ----------------------------------


def price_retrieve(collection, db_name=DB_NAME):

    price_df = query_mongo(db_name, collection)
    price_df = price_df.sort_values(
        by=["Date"], ascending=False)
    price_df.reset_index(drop=True, inplace=True)

    try:
        price_df = price_df.drop(columns="Time")

    except KeyError:
        pass

    return price_df


def yahoo_price_fix(df):

    header = list(df.columns)

    date_arr = df["Date"]

    # initializing the fixed df and assigning the Date column
    fixed_df = pd.DataFrame(columns=header)
    fixed_df["Date"] = df["Date"]

    try:
        header.remove("Date")
    except ValueError:
        pass

    # fillind NaN value with a string
    df.fillna("NaN", inplace=True)

    for element in header:

        el_df = pd.DataFrame(columns=["Date", element])
        el_df["Date"] = df["Date"]
        el_df[element] = df[element]

        # extract a list of Date corresponding to NaN values
        nan_list = list(
            el_df.loc[el_df[element] == "NaN", "Date"])

        for nan in nan_list:

            nan_pos = date_arr[date_arr == nan].index[0]
            prev_date = date_arr.iloc[nan_pos - 1]

            prev_price = el_df.loc[el_df.Date == prev_date, element]

            el_df.iloc[nan_pos, 1] = np.array(prev_price)[0]

        fixed_df[element] = el_df[element]

    return fixed_df


def return_retrieve(collection, db_name=DB_NAME):

    return_df = query_mongo(db_name, collection)
    return_df = return_df.sort_values(by=["Date"], ascending=False)

    try:
        return_df = return_df.drop(columns="Time")

    except KeyError:
        pass

    column_set = list(return_df.columns)

    try:
        column_set.remove("Date")
    except ValueError:
        pass

    for el in column_set:

        return_df[el] = [float(x) for x in return_df[el]]

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

    var_ret_df["BTC"] = merged_btc
    var_ret_df["ETH"] = merged_eth
    var_ret_df["LTC"] = merged_ltc
    var_ret_df["XRP"] = merged_xrp

    adj_ret_df = var_ret_df[VAR_STATIC_LIST]

    return adj_ret_df


# --------------------------
# DYNAMIC CORRELATIONS
# --------------------------


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
            delta_date, date, inclusive='both')]

        sub_second_df = second_df.loc[second_df.Date.between(
            delta_date, date, inclusive='both')]

        merged = pd.merge(sub_first_df, sub_second_df, on=["Date"])
        merged.reset_index(inplace=True, drop=True)

        merged = merged.drop(columns=["Date"])

        day_corr = merged.corr()

        value_of_int = day_corr.iloc[[0], [1]]
 
        corr_series = pd.concat((corr_series, value_of_int))
        corr_series.reset_index(inplace=True, drop=True)

    return corr_series


def dynamic_total(tot_ret_df, time_window, corr_set):

    tot_ret_dff = tot_ret_df.copy()
    tot_corr = tot_ret_df[["Date"]]

    if corr_set == "altcoin":

        ref_variable = REF_CRYPTO
        others_comm = CRYPTO_LIST

    elif corr_set == "assets":

        ref_variable = REF_CRYPTO
        others_comm = ["BTC"] + ASSET_LIST

    ref_comm_df = tot_ret_dff[["Date", ref_variable]]

    for element in others_comm:

        comm_df = tot_ret_dff[["Date", element]]
        single_corr = dynamic_corr(ref_comm_df, comm_df, time_window)

        if element == ref_variable:

            single_corr = single_corr.drop(columns=element)
            single_corr = single_corr.rename(columns={element + '_y': element})

        single_corr.reset_index(drop=True, inplace=True)
        tot_corr[element] = single_corr[element]

    return tot_corr


def dynamic_corr_op(return_df, corr_set):

    corr_YTD = dynamic_total(return_df, "YTD", corr_set)
    corr_3Y = dynamic_total(return_df, "3Y", corr_set)
    corr_1Y = dynamic_total(return_df, "1Y", corr_set)
    corr_1Q = dynamic_total(return_df, "1Q", corr_set)
    corr_1M = dynamic_total(return_df, "1M", corr_set)

    return corr_YTD, corr_3Y, corr_1Y, corr_1Q, corr_1M


# ----------------------------
# STATIC CORRELATION
# --------------------------


def static_corr(return_df, time_window=None, comp_set=None, quarter="N"):

    last_q = last_quarter_end()

    if time_window is None:

        df_to_compute = return_df

        if quarter == "Y":

            df_to_compute = df_to_compute.loc[df_to_compute.Date < last_q]

        else:
            pass

    else:

        if quarter == "Y":

            first_date = last_q

        else:

            first_row = return_df.head(1)
            first_date = str(first_row["Date"].to_numpy()[0])

        delta_date = roll_single_time(first_date, time_window)

        df_to_compute = return_df.loc[return_df.Date.between(
            delta_date, first_date, inclusive='both')]

    if comp_set is None:
        pass

    else:
        df_to_compute = df_to_compute[comp_set]

    corr_matrix = df_to_compute.corr()

    return corr_matrix


def static_corr_op(return_df, comp_set=None, quarter="N"):

    static_all = static_corr(return_df, comp_set=comp_set, quarter=quarter)
    static_3Y = static_corr(return_df, "3Y", comp_set, quarter=quarter)
    static_1Y = static_corr(return_df, "1Y", comp_set, quarter=quarter)
    static_1Q = static_corr(return_df, "1Q", comp_set, quarter=quarter)
    static_1M = static_corr(return_df, "1M", comp_set, quarter=quarter)

    return static_all, static_3Y, static_1Y, static_1Q, static_1M


# ---------------------------------
# BTC DENOMINATED PRICES
# ---------------------------------

def return_in_btc_comp(total_df, time_window, quarter="N"):
    """
    time_window can be "5Y", "3Y", "2Y", "1Y", "6M", "3M", "1M", "1W", "YTD"
    """

    # order values from oldest to newest
    total_df = total_df.sort_values(by=["Date"], ascending=True)

    date_df = total_df["Date"]

    first_date, last_date = window_period_back(date_df, time_window, quarter)

    try:

        last_date = datetime.strptime(last_date, "%d-%m-%Y")
        last_date = last_date.strftime("%Y-%m-%d")

    except ValueError:
        pass

    total_df = total_df.loc[total_df.Date.between(
        first_date, last_date, inclusive='both')]
    total_df.reset_index(drop=True, inplace=True)

    sub_date = pd.DataFrame(columns=["Date"])
    sub_date["Date"] = total_df["Date"]
    sub_date.reset_index(drop=True, inplace=True)

    total_df = total_df.drop(columns=["Date"])
    header = total_df.columns
    btc_series = pd.DataFrame(columns=["BTC"])
    btc_series["BTC"] = total_df["BTC"]

    # transforming into numpy array
    total_arr = np.array(total_df)
    btc_series = np.array(btc_series)

    # dividing for BTC price series
    df_in_btc = np.divide(total_arr, btc_series,
                          out=np.zeros_like(total_arr),
                          where=btc_series != 0.0)

    first_row = df_in_btc[0, :]

    normalized_arr = np.divide(df_in_btc, first_row,
                               out=np.zeros_like(df_in_btc),
                               where=first_row != 0.0)

    normalized_df = pd.DataFrame(normalized_arr, columns=header)
    normalized_df = pd.concat([sub_date, normalized_df], axis=1)

    return normalized_df


def btc_denominated_total(input_df:pd.DataFrame):

    df = input_df.copy()

    crypto_col = ["Date"] + CRYPTO_LIST
    asset_col = ["Date", "BTC"] + ASSET_LIST
    alt_price_df = df[crypto_col]
    yahoo_price_df = df[asset_col]
    # computation as of yesterday

    yahoo_df_YTD = return_in_btc_comp(yahoo_price_df, "YTD")
    alt_df_YTD = return_in_btc_comp(alt_price_df, "YTD")

    mongo_upload(yahoo_df_YTD, "collection_yahoo_btc_den_YTD")
    mongo_upload(alt_df_YTD, "collection_alt_btc_den_YTD")

    yahoo_df_5Y = return_in_btc_comp(yahoo_price_df, "5Y")
    alt_df_5Y = return_in_btc_comp(alt_price_df, "5Y")

    mongo_upload(yahoo_df_5Y, "collection_yahoo_btc_den_5Y")
    mongo_upload(alt_df_5Y, "collection_alt_btc_den_5Y")

    yahoo_df_3Y = return_in_btc_comp(yahoo_price_df, "3Y")
    alt_df_3Y = return_in_btc_comp(alt_price_df, "3Y")

    mongo_upload(yahoo_df_3Y, "collection_yahoo_btc_den_3Y")
    mongo_upload(alt_df_3Y, "collection_alt_btc_den_3Y")

    yahoo_df_2Y = return_in_btc_comp(yahoo_price_df, "2Y")
    alt_df_2Y = return_in_btc_comp(alt_price_df, "2Y")

    mongo_upload(yahoo_df_2Y, "collection_yahoo_btc_den_2Y")
    mongo_upload(alt_df_2Y, "collection_alt_btc_den_2Y")

    yahoo_df_1Y = return_in_btc_comp(yahoo_price_df, "1Y")
    alt_df_1Y = return_in_btc_comp(alt_price_df, "1Y")

    mongo_upload(yahoo_df_1Y, "collection_yahoo_btc_den_1Y")
    mongo_upload(alt_df_1Y, "collection_alt_btc_den_1Y")

    yahoo_df_6M = return_in_btc_comp(yahoo_price_df, "6M")
    alt_df_6M = return_in_btc_comp(alt_price_df, "6M")

    mongo_upload(yahoo_df_6M, "collection_yahoo_btc_den_6M")
    mongo_upload(alt_df_6M, "collection_alt_btc_den_6M")

    yahoo_df_3M = return_in_btc_comp(yahoo_price_df, "3M")
    alt_df_3M = return_in_btc_comp(alt_price_df, "3M")

    mongo_upload(yahoo_df_3M, "collection_yahoo_btc_den_3M")
    mongo_upload(alt_df_3M, "collection_alt_btc_den_3M")

    yahoo_df_1M = return_in_btc_comp(yahoo_price_df, "1M")
    alt_df_1M = return_in_btc_comp(alt_price_df, "1M")

    mongo_upload(yahoo_df_1M, "collection_yahoo_btc_den_1M")
    mongo_upload(alt_df_1M, "collection_alt_btc_den_1M")

    yahoo_df_1W = return_in_btc_comp(yahoo_price_df, "1W")
    alt_df_1W = return_in_btc_comp(alt_price_df, "1W")

    mongo_upload(yahoo_df_1W, "collection_yahoo_btc_den_1W")
    mongo_upload(alt_df_1W, "collection_alt_btc_den_1W")

    # computation as of last quarter

    yahoo_df_YTD_quarter = return_in_btc_comp(
        yahoo_price_df, "YTD", quarter="Y")
    alt_df_YTD_quarter = return_in_btc_comp(alt_price_df, "YTD", quarter="Y")

    mongo_upload(yahoo_df_YTD_quarter, "collection_yahoo_btc_den_YTD_quarter")
    mongo_upload(alt_df_YTD_quarter, "collection_alt_btc_den_YTD_quarter")

    yahoo_df_5Y_quarter = return_in_btc_comp(yahoo_price_df, "5Y", quarter="Y")
    alt_df_5Y_quarter = return_in_btc_comp(alt_price_df, "5Y", quarter="Y")

    mongo_upload(yahoo_df_5Y_quarter, "collection_yahoo_btc_den_5Y_quarter")
    mongo_upload(alt_df_5Y_quarter, "collection_alt_btc_den_5Y_quarter")

    yahoo_df_3Y_quarter = return_in_btc_comp(yahoo_price_df, "3Y", quarter="Y")
    alt_df_3Y_quarter = return_in_btc_comp(alt_price_df, "3Y", quarter="Y")

    mongo_upload(yahoo_df_3Y_quarter, "collection_yahoo_btc_den_3Y_quarter")
    mongo_upload(alt_df_3Y_quarter, "collection_alt_btc_den_3Y_quarter")

    yahoo_df_2Y_quarter = return_in_btc_comp(yahoo_price_df, "2Y", quarter="Y")
    alt_df_2Y_quarter = return_in_btc_comp(alt_price_df, "2Y", quarter="Y")

    mongo_upload(yahoo_df_2Y_quarter, "collection_yahoo_btc_den_2Y_quarter")
    mongo_upload(alt_df_2Y_quarter, "collection_alt_btc_den_2Y_quarter")

    yahoo_df_1Y_quarter = return_in_btc_comp(yahoo_price_df, "1Y", quarter="Y")
    alt_df_1Y_quarter = return_in_btc_comp(alt_price_df, "1Y", quarter="Y")

    mongo_upload(yahoo_df_1Y_quarter, "collection_yahoo_btc_den_1Y_quarter")
    mongo_upload(alt_df_1Y_quarter, "collection_alt_btc_den_1Y_quarter")

    yahoo_df_6M_quarter = return_in_btc_comp(yahoo_price_df, "6M", quarter="Y")
    alt_df_6M_quarter = return_in_btc_comp(alt_price_df, "6M", quarter="Y")

    mongo_upload(yahoo_df_6M_quarter, "collection_yahoo_btc_den_6M_quarter")
    mongo_upload(alt_df_6M_quarter, "collection_alt_btc_den_6M_quarter")

    yahoo_df_3M_quarter = return_in_btc_comp(yahoo_price_df, "3M", quarter="Y")
    alt_df_3M_quarter = return_in_btc_comp(alt_price_df, "3M", quarter="Y")

    mongo_upload(yahoo_df_3M_quarter, "collection_yahoo_btc_den_3M_quarter")
    mongo_upload(alt_df_3M_quarter, "collection_alt_btc_den_3M_quarter")

    yahoo_df_1M_quarter = return_in_btc_comp(yahoo_price_df, "1M", quarter="Y")
    alt_df_1M_quarter = return_in_btc_comp(alt_price_df, "1M", quarter="Y")

    mongo_upload(yahoo_df_1M_quarter, "collection_yahoo_btc_den_1M_quarter")
    mongo_upload(alt_df_1M_quarter, "collection_alt_btc_den_1M_quarter")

    yahoo_df_1W_quarter = return_in_btc_comp(yahoo_price_df, "1W", quarter="Y")
    alt_df_1W_quarter = return_in_btc_comp(alt_price_df, "1W", quarter="Y")

    mongo_upload(yahoo_df_1W_quarter, "collection_yahoo_btc_den_1W_quarter")
    mongo_upload(alt_df_1W_quarter, "collection_alt_btc_den_1W_quarter")


# ---------------------------------
# USD DENOMINATED PRICES
# ---------------------------------


def usd_normalized_calc(yahoo_returns, time_window, quarter="N"):
    """
    time_window can be "5Y "3Y", "2Y", 1Y", "6M", "3M", "1M", "1W", "YTD"
    """

    yahoo_returns = yahoo_returns.sort_values(by=["Date"], ascending=True)
    yahoo_returns = yahoo_returns.replace(np.inf, np.nan)
    yahoo_returns.fillna(0, inplace=True)

    date_df = yahoo_returns["Date"]

    yahoo_returns.reset_index(drop=True, inplace=True)

    yahoo_col_tot = list(yahoo_returns.columns)
    yahoo_col = yahoo_col_tot.copy()
    yahoo_col.remove("Date")

    first_date, last_date = window_period_back(date_df, time_window, quarter)

    try:

        last_date = datetime.strptime(last_date, "%d-%m-%Y")
        last_date = last_date.strftime("%Y-%m-%d")

    except ValueError:
        pass

    total_df = yahoo_returns.loc[yahoo_returns.Date.between(
        first_date, last_date, inclusive='both')]

    sub_date = pd.DataFrame(columns=["Date"])
    sub_date["Date"] = total_df["Date"]
    sub_date.reset_index(drop=True, inplace=True)

    norm_matrix = np.array(total_df["Date"])

    for asset in yahoo_col:

        asset_col = np.array(total_df[asset])
        asset_col = asset_col[1:len(asset_col)]
        norm_arr = np.array([1])
        current_value = 1

        for ret in asset_col:

            next_value = current_value * (1 + ret)
            norm_arr = np.append(norm_arr, next_value)

            current_value = next_value

        norm_matrix = np.column_stack((norm_matrix, norm_arr))

    header = yahoo_col_tot
    norm_df = pd.DataFrame(norm_matrix, columns=header)

    return norm_df


def usd_normalized_total(yahoo_price_df):

    # computation as of yesterday

    yahoo_df_YTD = usd_normalized_calc(yahoo_price_df, "YTD")

    mongo_upload(yahoo_df_YTD, "collection_normalized_prices_YTD")

    yahoo_df_5Y = usd_normalized_calc(yahoo_price_df, "5Y")

    mongo_upload(yahoo_df_5Y, "collection_normalized_prices_5Y")

    yahoo_df_3Y = usd_normalized_calc(yahoo_price_df, "3Y")

    mongo_upload(yahoo_df_3Y, "collection_normalized_prices_3Y")

    yahoo_df_2Y = usd_normalized_calc(yahoo_price_df, "2Y")

    mongo_upload(yahoo_df_2Y, "collection_normalized_prices_2Y")

    yahoo_df_1Y = usd_normalized_calc(yahoo_price_df, "1Y")

    mongo_upload(yahoo_df_1Y, "collection_normalized_prices_1Y")

    yahoo_df_6M = usd_normalized_calc(yahoo_price_df, "6M")

    mongo_upload(yahoo_df_6M, "collection_normalized_prices_6M")

    yahoo_df_3M = usd_normalized_calc(yahoo_price_df, "3M")

    mongo_upload(yahoo_df_3M, "collection_normalized_prices_3M")

    yahoo_df_1M = usd_normalized_calc(yahoo_price_df, "1M")

    mongo_upload(yahoo_df_1M, "collection_normalized_prices_1M")

    yahoo_df_1W = usd_normalized_calc(yahoo_price_df, "1W")

    mongo_upload(yahoo_df_1W, "collection_normalized_prices_1W")

    # computation as of last quarter end

    yahoo_df_YTD_quarter = usd_normalized_calc(
        yahoo_price_df, "YTD", quarter="Y")

    mongo_upload(yahoo_df_YTD_quarter,
                 "collection_normalized_prices_YTD_quarter")

    yahoo_df_5Y_quarter = usd_normalized_calc(
        yahoo_price_df, "5Y", quarter="Y")

    mongo_upload(yahoo_df_5Y_quarter,
                 "collection_normalized_prices_5Y_quarter")

    yahoo_df_3Y_quarter = usd_normalized_calc(
        yahoo_price_df, "3Y", quarter="Y")

    mongo_upload(yahoo_df_3Y_quarter,
                 "collection_normalized_prices_3Y_quarter")

    yahoo_df_2Y_quarter = usd_normalized_calc(
        yahoo_price_df, "2Y", quarter="Y")

    mongo_upload(yahoo_df_2Y_quarter,
                 "collection_normalized_prices_2Y_quarter")

    yahoo_df_1Y_quarter = usd_normalized_calc(
        yahoo_price_df, "1Y", quarter="Y")

    mongo_upload(yahoo_df_1Y_quarter,
                 "collection_normalized_prices_1Y_quarter")

    yahoo_df_6M_quarter = usd_normalized_calc(
        yahoo_price_df, "6M", quarter="Y")

    mongo_upload(yahoo_df_6M_quarter,
                 "collection_normalized_prices_6M_quarter")

    yahoo_df_3M_quarter = usd_normalized_calc(
        yahoo_price_df, "3M", quarter="Y")

    mongo_upload(yahoo_df_3M_quarter,
                 "collection_normalized_prices_3M_quarter")

    yahoo_df_1M_quarter = usd_normalized_calc(
        yahoo_price_df, "1M", quarter="Y")

    mongo_upload(yahoo_df_1M_quarter,
                 "collection_normalized_prices_1M_quarter")

    yahoo_df_1W_quarter = usd_normalized_calc(
        yahoo_price_df, "1W", quarter="Y")

    mongo_upload(yahoo_df_1W_quarter,
                 "collection_normalized_prices_1W_quarter")


# ---
# Quarter Performances

def quarter_perfomance(price_df):

    dff_for_list = price_df.copy()
    dff = price_df.copy()

    quarter_list = quarter_from_date(dff_for_list, "Date")
    quarter_list["Quarter"] = [d.strftime(
        "%d-%m-%Y") for d in quarter_list["Quarter"]]
    dff = dff.rename(columns={"Date": "Quarter"})

    quarter_price = pd.merge(quarter_list, dff, on="Quarter", how="left")
    quarter_price["Quarter Performance"] = quarter_price["BTC Price"].pct_change()
    quarter_price = add_quarter(quarter_price, "Quarter")

    return quarter_price
