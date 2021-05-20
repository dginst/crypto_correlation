import logging

from btc_analysis.config import YAHOO_TO_CAPM
from btc_analysis.efficient_frontier import eff_front_op
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('markovitz_launcher.py start')

# mongo collections operations
mongo_coll_drop("markovitz")
mongo_indexing()

# retriving prices and logreturn from MongoDB
all_price_df = query_mongo("btc_analysis", "all_prices_y")
prices = all_price_df[YAHOO_TO_CAPM]

log_ret_df = query_mongo("btc_analysis", "all_logreturns_y")
log_ret = log_ret_df[YAHOO_TO_CAPM]

# computing the optimal allocation with and without BTC
tot_df, comp_tot_df = eff_front_op(
    prices, log_ret, stock_to_remove="BTC")

mongo_upload(tot_df, "collection_CAPM")
mongo_upload(comp_tot_df, "collection_CAPM_no_BTC")

logging.info('markovitz_launcher.py end')
