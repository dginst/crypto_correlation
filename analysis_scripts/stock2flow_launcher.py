from pathlib import Path

import pandas as pd
from btc_analysis.config import HALVING_DATE
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)
from btc_analysis.stock2flow_func import (S2F_complete_model, S2F_definition,
                                          S2FX_complete_model, S2FX_definition,
                                          check_and_add, days_to_halving,
                                          halving_performace)

mongo_coll_drop("S2F")

mongo_indexing()

# ----------
# data gathering
# ---------
check_and_add()
initial_data = pd.read_csv(
    Path("source_data", "initial_data_S2F.csv"), sep="|")

BTC_prices = pd.read_csv(
    Path("source_data", "BTC_price.csv"), sep="|")

# adding the day to halving in each days

price_df = days_to_halving(BTC_prices, HALVING_DATE)
mongo_upload(price_df, "collection_S2F_BTC")
d = query_mongo("btc_analysis", "S2F_BTC_price")

# -----------------------
# S2F stadard model definition

slope, intercept = S2F_definition(initial_data)
final_df = S2F_complete_model(slope, intercept)
mongo_upload(final_df, "collection_S2F")

# dataframe for perfomaces comparison
halving_perf_df = halving_performace(price_df, final_df)
mongo_upload(halving_perf_df, "collection_S2F_performance")

# S2F CROSS ASSET MODEL DEFINITION

slope_, intercept_ = S2FX_definition(initial_data, 4)
final_df_ = S2FX_complete_model(slope_, intercept_)

mongo_upload(final_df_, "collection_S2FX")
