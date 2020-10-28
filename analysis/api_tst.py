import yfinance as yf
from datetime import datetime
from calc import date_gen
import pandas as pd
import numpy as np
from mongo_func import (
    mongo_upload, mongo_indexing, query_mongo,
    mongo_coll_drop
)


def all_series_download(series_code_list, all_el_list,
                        start_period, end_period):

    all_series_df = pd.DataFrame(columns=all_el_list)

    for i, element in enumerate(series_code_list):

        var = all_el_list[i]

        single_series = single_series_download(
            element, start_period, end_period)

        if var == "Petrol":

            date_arr = single_series["Date"]
        
        elif var == "BTC":

            date_arr = single_series["Date"]

        all_series_df[var] = single_series["Close"]

    all_series_df["Date"] = date_arr

    return all_series_df


def single_series_download(series_code, start_period, end_period):

    # creatre object
    series_obj = yf.Ticker(series_code)

    # create the complete array of date
    date_arr = np.array(date_gen(start_period, end_period, holiday="N"))
    date_df = pd.DataFrame(columns=["Date"])
    date_df["Date"] = date_arr

    # get historical market data
    df = series_obj.history(start=start_period, end=end_period)
    df.reset_index(inplace=True)

    # modifying date format
    df["Date"] = [x.strftime("%Y-%m-%d") for x in df["Date"]]
    # df["Date"] = [datetime.strptime(
    #    x, "%Y-%m-%d") for x in df["Date"]]

    df = df[["Date", "Close"]]
    # print(df)
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


def mkt_data_op(series_code_list, all_el_list,
                start_period, end_period):

    all_series_df = all_series_download(series_code_list, all_el_list,
                                        start_period, end_period)
    print(all_series_df)

    mongo_upload(all_series_df, "collection_metal_price")

    all_ret_df = all_series_to_return(all_series_df, all_el_list)
    print(all_ret_df)

    mongo_upload(all_ret_df, "collection_metal_ret")


# XW=F wheat
# to_download = ["Petrol", "Corn", "MSCI", "Metal", "PANEUR", "PANUS"]

# to_download_code = ["CL=F", "ZW=F", "ISV1.BE", "^SPGSIN", "EAGG.PA", "USAG.PA"]
to_download = ["BTC", "Gold", "Silver", "Copper"]

to_download_code = ["BTC-EUR", "GC=F", "SI=F", "HG=F"]

mongo_coll_drop("yahoo_metal")

mkt_data_op(to_download_code, to_download,
            "2014-01-01", "2020-09-30")


# var_ret = query_mongo("btc_analysis", "return_various")
# var_ret = var_ret.loc[var_ret.Date.between("2019-01-01", "2020-09-30")]
# print(var_ret)
# yah_ret = query_mongo("btc_analysis", "all_returns")

# wti_check = var_ret[["Date", "WTI"]]
# wti_check["Petrol"] = yah_ret["Petrol"]
# wti_petr_corr = wti_check.corr()
# print(wti_petr_corr)

# corn_check = var_ret[["Date", "GRAIN"]]
# corn_check["Corn"] = yah_ret["Corn"]
# corn_corr = corn_check.corr()
# print(corn_corr)

# metal_check = var_ret[["Date", "IND_METALS"]]
# metal_check["Metal"] = yah_ret["Metal"]
# metal_corr = metal_check.corr()
# print(metal_corr)

# M_check = var_ret[["Date", "MSCI BRIC "]]
# M_check["MSCI"] = yah_ret["MSCI"]
# M_corr = M_check.corr()
# print(M_corr)

# pane_check = var_ret[["Date", "BBG Barclays PAN EURO Aggregate"]]
# pane_check["PANEUR"] = yah_ret["PANEUR"]
# pane_corr = pane_check.corr()
# print(pane_corr)

# panus_check = var_ret[["Date", "BBG Barclays PAN US Aggregate"]]
# panus_check["PANUS"] = yah_ret["PANUS"]
# panus_corr = panus_check.corr()
# print(panus_corr)
