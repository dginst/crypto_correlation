import yfinance as yf
from calc import date_gen
import pandas as pd
import numpy as np
from mongo_func import (
    mongo_upload
)


def all_series_download(series_code_list, all_el_list,
                        start_period, end_period):

    all_series_df = pd.DataFrame(columns=all_el_list)

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
    df = df[["Date", "Close"]]

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


def mkt_data_op(series_code_list, all_el_list,
                start_period, end_period):

    all_series_df = all_series_download(series_code_list, all_el_list,
                                        start_period, end_period)

    mongo_upload(all_series_df, "collection_prices")

    all_ret_df = all_series_to_return(all_series_df, all_el_list)

    mongo_upload(all_ret_df, "collection_returns")

    all_logret_df = all_series_to_logret(all_series_df)

    mongo_upload(all_logret_df, "collection_logreturns")
