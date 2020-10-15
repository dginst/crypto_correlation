from mongo_func import (
    query_mongo, mongo_indexing, mongo_upload
)
from config import (
    DB_NAME
)

from calc import (
    roll_single_time, dynamic_corr,
    dynamic_total, static_corr
)
import pandas as pd
from scipy.stats.stats import pearsonr
import numpy as np

mongo_indexing()

tot_ret = query_mongo(DB_NAME, "return_various")

tot_ret = tot_ret.sort_values(by=["Date"], ascending=False)
tot_ret.reset_index(drop=True, inplace=True)
print(tot_ret)

tot = static_corr(tot_ret, "1Y")
# mongo_upload(tot, "collection_static_alt")
print(tot)

# corr_1Y = dynamic_total(tot_ret, "1Y", "various")
# mongo_upload(corr_1Y, "collection_1Y_dyn_var")
# corr_1Q = dynamic_total(tot_ret, "1Q", "various")
# mongo_upload(corr_1Q, "collection_1Q_dyn_var")
# corr_1M = dynamic_total(tot_ret, "1M", "various")
# mongo_upload(corr_1M, "collection_1M_dyn_var")
# print(corr_3Y)
# corr_1Y = dynamic_total(tot_ret, "1Y")
# mongo_upload(corr_1Y, "collection_1Y_dyn")
# print(corr_1Y)
# corr_1Q = dynamic_total(tot_ret, "1Q")
# mongo_upload(corr_1Q, "collection_1Q_dyn")
# corr_3M = dynamic_total(tot_ret, "1M")
# mongo_upload(corr_3M, "collection_3M_dyn")

# btc_ret = tot_ret[["Date", "BTC"]]

# eth_ret = tot_ret[["Date", "ETH"]]

# prov = dynamic_corr(btc_ret, eth_ret, "1Y")

# print(prov)

# merged = btc_ret
# merged["ETH"] = eth_ret
# corr_tot = merged.corr()
# print(btc_ret)
# print(eth_ret)

# correl = btc_ret.corr()
# print(correl)

# s = roll_time(tot_ret["Date"], "1Y")

# s = s.sort_values(by=["Date"], ascending=False)

# print(s)
