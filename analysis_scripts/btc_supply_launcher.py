from pathlib import Path

import pandas as pd
from btc_analysis.market_data import (blockchain_stats_op, btc_supply_op,
                                      check_and_add_supply)
from btc_analysis.mongo_func import mongo_coll_drop, mongo_upload

mongo_coll_drop("supply")

blockchain_stats_op()

check_and_add_supply()
issuance_df = pd.read_csv(Path("source_data", "BTC_issuance.csv"), sep="|")

supply_df = btc_supply_op(issuance_df)

mongo_upload(supply_df, "collection_total_supply")
