import logging
import pandas as pd
import numpy as np

from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)
from btc_analysis.market_data import (
    btc_supply_op, check_and_add_daily, blockchain_stats_op, yesterday_str,
    check_missing_days)

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('btc_net_daily.py start')

# --
mongo_coll_drop("supply")
mongo_coll_drop("btc_network")

mongo_indexing()

yesterday = yesterday_str("%Y-%m-%d")
yesterday_ = yesterday_str("%d-%m-%Y")

# ---
# btc price collection update

try:

    crypto_price_df = query_mongo("index", "crypto_price")
    btc_tot_df = crypto_price_df[["BTC"]]

    list_of_missing = check_missing_days("btc_price", type_="price")
    lenght_missing = len(list_of_missing)

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


except Exception:

    logging.error("Exception occurred", exc_info=True)
    logging.info(
        'BTC prices collection failed to update')
    pass

# ---
# daily blockchain info

try:

    blockchain_stats_op()

    daily_df = query_mongo("btc_analysis", "btc_network")

except Exception:

    logging.error("Exception occurred", exc_info=True)
    logging.info(
        'BTC network operation failed to update')
    pass
# ---
# hash rate

try:

    hr_df = daily_df.copy()
    hr_df = hr_df[["Hash Rate"]]
    hr_df["Date"] = yesterday
    hr_df["Hash Rate"] = [float(x) for x in hr_df["Hash Rate"]]

    check_and_add_daily(hr_df, "hash_rate", "collection_hash_rate")

except Exception:

    logging.error("Exception occurred", exc_info=True)
    logging.info(
        'BTC hash rate collection failed to update')
    pass

# ----
# supply

try:

    supply_df = daily_df.copy()
    supply_df = supply_df[["Daily BTC", "Daily Block"]]

    new_btc = np.array(supply_df["Daily BTC"])[0]
    new_block = np.array(supply_df["Daily Block"])[0]
    new_supply_arr = np.column_stack((yesterday, new_btc, new_block))
    new_supply_df = pd.DataFrame(new_supply_arr, columns=[
        "Date", "BTC Issuance", "BTC Blocks"])

    new_supply_df["BTC Issuance"] = [float(x)
                                     for x in new_supply_df["BTC Issuance"]]
    new_supply_df["BTC Blocks"] = [float(x)
                                   for x in new_supply_df["BTC Blocks"]]

    # updating Block Number and BTC Issuance
    check_and_add_daily(new_supply_df, "btc_hist_supply",
                        "collection_hist_supply")

    # update supply computation and upload

    initial_supply_df = query_mongo("btc_analysis", "btc_hist_supply")

    final_supply_df = btc_supply_op(initial_supply_df)

    mongo_upload(final_supply_df, "collection_total_supply")

except Exception:

    logging.error("Exception occurred", exc_info=True)
    logging.info(
        'BTC supply collection failed to update')
    pass
# ----
# difficulty


# ----
logging.info('btc_net_daily.py end')
