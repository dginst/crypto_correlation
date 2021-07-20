from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from btc_analysis.market_data import (btc_supply_op, check_missing_days,
                                      yesterday_str)
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)

mongo_coll_drop("hash_rate")
mongo_coll_drop("hist_supply")
mongo_coll_drop("btc_price")

mongo_indexing()

# --------
# BTC Price

# upload the oldest values
csv_btc_price = pd.read_csv(
    Path("source_data", "BTC_price.csv"), sep="|")


mongo_upload(csv_btc_price, "collection_btc_price")

# upload the latest values
yesterday_ = yesterday_str("%d-%m-%Y")
crypto_price_df = query_mongo("index", "crypto_price")
btc_tot_df = crypto_price_df[["BTC"]]

list_of_missing = check_missing_days("btc_price", type_="price")
lenght_missing = len(list_of_missing)

list_of_missing = [datetime.strptime(
    d, "%Y-%m-%d") for d in list_of_missing]
list_of_missing = [d.strftime("%d-%m-%Y") for d in list_of_missing]

if lenght_missing > 1:

    btc_missing = np.array(btc_tot_df.tail(lenght_missing))
    new_arr = np.column_stack((list_of_missing, btc_missing))
    new_df = pd.DataFrame(new_arr, columns=["Date", "BTC Price"])
    new_df["BTC Price"] = [float(x) for x in new_df["BTC Price"]]
    mongo_upload(new_df, "collection_btc_price")

elif lenght_missing == 1:

    btc_last = np.array(btc_tot_df.tail(1))[0]
    new_arr = np.column_stack((yesterday_, btc_last))
    new_df = pd.DataFrame(new_arr, columns=["Date", "BTC Price"])
    new_df["BTC Price"] = [float(x) for x in new_df["BTC Price"]]
    mongo_upload(new_df, "collection_btc_price")

elif lenght_missing == 0:

    pass


# ----------
# hash rate

csv_hash_rate = pd.read_csv(
    Path("source_data", "hash_rate.csv"), sep="|")


mongo_upload(csv_hash_rate, "collection_hash_rate")

# --------
# supply

csv_supply = pd.read_csv(
    Path("source_data", "BTC_issuance.csv"), sep="|")

mongo_upload(csv_supply, "collection_hist_supply")

# ------
# difficulty
