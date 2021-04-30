import numpy as np
import pandas as pd
from btc_analysis.config import STABLECOIN_NAME, STABLECOIN_TICKER
from btc_analysis.market_data import (mkt_cap_stable_op,
                                      ticker_price_downloader, yesterday_str)
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload)

mongo_coll_drop("stable_daily")

mongo_indexing()

yesterday_str_ = yesterday_str("%Y-%m-%d")


stable_mkt_cap = mkt_cap_stable_op(
    STABLECOIN_TICKER, STABLECOIN_NAME, yesterday_str_)

stable_price = ticker_price_downloader(STABLECOIN_TICKER, STABLECOIN_NAME)
print(stable_price)

USDT_supply = np.array(stable_mkt_cap["USDT"]/stable_price["USDT"])[0]
USDC_supply = np.array(stable_mkt_cap["USDC"]/stable_price["USDC"])[0]
print(USDT_supply)
daily_arr = np.column_stack((yesterday_str_, USDT_supply, USDC_supply))

stable_daily_df = pd.DataFrame(
    daily_arr, columns=["Date", "USDT Supply", "USDC Supply"])
stable_daily_df["USDT Supply"] = [
    float(x) for x in stable_daily_df["USDT Supply"]]
stable_daily_df["USDC Supply"] = [
    float(x) for x in stable_daily_df["USDC Supply"]]

mongo_upload(stable_daily_df, "collection_stablecoin_daily")
mongo_upload(stable_daily_df, "collection_stablecoin_all")
