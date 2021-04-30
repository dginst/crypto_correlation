from pathlib import Path

import pandas as pd
import numpy as np

from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload)


mongo_coll_drop("stable_hist")


mongo_indexing()

# --------

csv_tether_price = pd.read_csv(
    Path("source_data", "tether.csv"), sep="|")

csv_tether_price["Price"] = [x.replace(",", ".")
                             for x in csv_tether_price["Price"]]
csv_tether_price["Market Cap"] = [
    float(x) for x in csv_tether_price["Market Cap"]]
csv_tether_price["Price"] = [
    float(x) for x in csv_tether_price["Price"]]

csv_usdcoin_price = pd.read_csv(
    Path("source_data", "USDC.csv"), sep="|")
csv_usdcoin_price["Price"] = [x.replace(",", ".")
                              for x in csv_usdcoin_price["Price"]]
csv_usdcoin_price["Market Cap"] = [
    float(x) for x in csv_usdcoin_price["Market Cap"]]
csv_usdcoin_price["Price"] = [
    float(x) for x in csv_usdcoin_price["Price"]]

date_arr = np.array(csv_tether_price["Date"])
USDT_supply = np.array(
    csv_tether_price["Market Cap"]/csv_tether_price["Price"])
USDC_supply = np.array(
    csv_usdcoin_price["Market Cap"]/csv_usdcoin_price["Price"])

stable_arr = np.column_stack((date_arr, USDT_supply, USDC_supply))
stable_df = pd.DataFrame(stable_arr, columns=[
                         "Date", "USDT Supply", "USDC Supply"])

mongo_upload(stable_df, "collection_stablecoin_all")
