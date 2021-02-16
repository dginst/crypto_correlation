from datetime import datetime, timezone
import yfinance as yf
from btc_analysis.calc import date_gen
import pandas as pd
import numpy as np
from btc_analysis.mongo_func import (
    mongo_upload, query_mongo
)
from btc_analysis.config import (START_DATE, INDEX_START_DATE)


def yesterday_str():

    today_str = datetime.now().strftime("%Y-%m-%d")
    today = datetime.strptime(today_str, "%Y-%m-%d")
    today_TS = int(today.replace(tzinfo=timezone.utc).timestamp())
    yesterday_TS = today_TS - 86400
    yesterday_date = datetime.fromtimestamp(int(yesterday_TS))
    yesterday = yesterday_date.strftime("%Y-%m-%d")

    return yesterday


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

    print(all_series_df_price)
    print(all_series_df_volume)

    # mongo_upload(all_series_df, "collection_prices_y")

    complete_series_df_price = add_crypto(all_series_df_price)
    mongo_upload(complete_series_df_price, "collection_prices_y")

    complete_series_df_volume = add_crypto(
        all_series_df_volume, collection="crypto_volume")
    mongo_upload(complete_series_df_volume, "collection_volume_y")

    all_ret_df = all_series_to_return(complete_series_df_price, all_el_list_r)

    mongo_upload(all_ret_df, "collection_returns_y")

    all_logret_df = all_series_to_logret(complete_series_df_price)

    mongo_upload(all_logret_df, "collection_logreturns_y")


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

    print(tot_crypto_df)

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
                               'PETROL',
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
                               'US_TREASURY',
                               'BBG Barclays PAN EURO Aggregate',
                               'US Aggregate Bond',
                               'US index',
                               'TESLA',
                               'AMAZON',
                               'APPLE',
                               'NETFLIX'
                               ]]

    return complete_df


def crypto_old_series_y(start, stop):

    yahoo_code = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'BCH-USD']

    yahoo_name = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH']

    crypto_df_price, crypto_df_volume = all_series_download(yahoo_code, yahoo_name,
                                                            start, stop)

    return crypto_df_price, crypto_df_volume
