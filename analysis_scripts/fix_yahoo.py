from btc_analysis.mongo_func import (
    query_mongo, mongo_indexing, mongo_upload
)

from btc_analysis.config import (
    CRYPTO_LIST, CRYPTO_STATIC_LIST, DB_NAME,
    VARIOUS_LIST
)
from btc_analysis.calc import (
    roll_single_time, dynamic_corr,
    dynamic_total, static_corr, correlation_op,
    metal_corr_op, return_retrieve, static_corr_op,
    dynamic_corr_op
)

from btc_analysis.excel_func import (
    alt_to_excel
)
import pandas as pd
from scipy.stats.stats import pearsonr
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
# mongo_indexing()


def yahoo_series_fix(single_series):

    delta = relativedelta(days=-1)
    col = list(single_series.columns)
    try:
        col.remove("Date")
    except ValueError:
        pass

    single_series["Date"] = [datetime.strptime(
        date, "%Y-%m-%d") for date in single_series["Date"]]

    # while single_series.loc[single_series[col[0]].isnull(), "Date"].empty is False:

    nan_value_date = pd.DataFrame(columns=["Date"])
    previous_date = pd.DataFrame(columns=["Date"])
    nan_value_date["Date"] = single_series.loc[single_series[col[0]].isnull(),
                                               "Date"]

    previous_date["Date"] = [(date + delta)
                             for date in nan_value_date["Date"]]
    print(previous_date)

    for date in previous_date["Date"]:

        print(date)
        if date.strftime("%Y-%m-%d") == "2012-12-30":
            print("inside")

            day_price = 0

        else:

            day_price = np.array(
                single_series.loc[single_series.Date == date, col])

            while day_price.size > 0:
                print("inside")
                date = date + delta
                print(date)

                try:

                    day_price = np.array(
                        single_series.loc[single_series.Date == date, col])
                except ValueError:
                    pass
                print(day_price)

            print(day_price)

        single_series.loc[single_series.Date ==
                          (date - delta), col] = day_price

        print(single_series.loc[single_series.Date ==
                                (date - delta), col])

    fixed_series = single_series

    return fixed_series


tot_price = query_mongo(DB_NAME, "all_prices_y")

x = yahoo_series_fix(tot_price[["Date", "EUROSTOXX50"]])
print(x.head(68))
print(x.loc[x["EUROSTOXX50"].isnull(), "Date"])
print(x.loc[x["EUROSTOXX50"].isnull(), "Date"].empty)
