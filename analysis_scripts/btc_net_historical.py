from pathlib import Path

import pandas as pd
import numpy as np

from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)
from btc_analysis.market_data import btc_supply_op


mongo_coll_drop("hash_rate")
mongo_coll_drop("hist_supply")
mongo_coll_drop("btc_price")

mongo_indexing()

# --------
# BTC Price

csv_btc_price = pd.read_csv(
    Path("source_data", "BTC_price.csv"), sep="|")


mongo_upload(csv_btc_price, "collection_btc_price")


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
