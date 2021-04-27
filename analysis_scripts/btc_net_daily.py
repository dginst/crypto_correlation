import pandas as pd
import numpy as np

from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)
from btc_analysis.market_data import (
    btc_supply_op, check_and_add_daily, blockchain_stats_op, yesterday_str)


mongo_coll_drop("supply")
mongo_coll_drop("btc_network")

mongo_indexing()

yesterday = yesterday_str("%Y-%m-%d")
yesterday_ = yesterday_str("%d-%m-%Y")

# ---
# btc price collection update

crypto_price_df = query_mongo("index", "crypto_price")
btc_tot_df = crypto_price_df[["BTC"]]
btc_last = np.array(btc_tot_df.tail(1))[0]

new_arr = np.column_stack((yesterday_, btc_last))

new_df = pd.DataFrame(new_arr, columns=["Date", "BTC Price"])
print(new_df)

check_and_add_daily(new_df, "btc_price", "collection_btc_price")

# ---
# daily blockchain info

blockchain_stats_op()

daily_df = query_mongo("btc_analysis", "btc_network")
print(daily_df)

# ---
# hash rate

hr_df = daily_df.copy()
hr_df = hr_df[["Hash Rate"]]
hr_df["Date"] = yesterday
print(hr_df)

check_and_add_daily(hr_df, "hash_rate", "collection_hash_rate")

# ----
# supply

supply_df = daily_df.copy()
supply_df = supply_df[["Daily BTC", "Daily Block"]]

# cum_sum = supply_df.cumsum()
# last_values = cum_sum.tail(1)
new_btc = np.array(supply_df["Daily BTC"])[0]
new_block = np.array(supply_df["Daily Block"])[0]
new_supply_arr = np.column_stack((yesterday, new_btc, new_block))
new_supply_df = pd.DataFrame(new_supply_arr, columns=[
                             "Date", "BTC Issuance", "BTC Blocks"])

# updating Block Number and BTC Issuance
check_and_add_daily(new_supply_df, "btc_hist_supply",
                    "collection_hist_supply")

# update supply computation and upload

initial_supply_df = query_mongo("btc_analysis", "btc_hist_supply")

final_supply_df = btc_supply_op(initial_supply_df)

mongo_upload(final_supply_df, "collection_total_supply")

# ----
# difficulty