import logging

from btc_analysis.calc import (dynamic_corr_op, price_retrieve,
                               return_retrieve, static_corr_op)
from btc_analysis.config import CORR_WINDOW_LIST, DB_NAME, INDEX_DB_NAME
from btc_analysis.dashboard_func import dash_correlation_df
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('btc_corr_dynamic_launcher.py start')

# mongo collections operations
mongo_coll_drop("dynamic_alt")
mongo_coll_drop("dynamic_yahoo")
mongo_indexing()

# --------------------------------------------
# BTC correlation with yahoo assets

tot_ret = query_mongo(DB_NAME, "all_returns_y")
tot_price = query_mongo(DB_NAME, "all_prices_y")

corr_YTD, corr_3Y, corr_1Y, corr_1Q, corr_1M = dynamic_corr_op(
    tot_ret, "various_y")

mongo_upload(corr_YTD, "collection_YTD_dyn_yahoo")
mongo_upload(corr_3Y, "collection_3Y_dyn_yahoo")
mongo_upload(corr_1Y, "collection_1Y_dyn_yahoo")
mongo_upload(corr_1Q, "collection_1Q_dyn_yahoo")
mongo_upload(corr_1M, "collection_1M_dyn_yahoo")

# ------------------------------------------------------------------------
# BTC correlations with altcoins

alt_ret_df = return_retrieve("crypto_price_return", db_name=INDEX_DB_NAME)
alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)


(dyn_alt_corr_YTD, dyn_alt_corr_3Y, dyn_alt_corr_1Y,
 dyn_alt_corr_1Q, dyn_alt_corr_1M) = dynamic_corr_op(
    alt_ret_df, "altcoin")

mongo_upload(dyn_alt_corr_YTD, "collection_YTD_dyn_alt")
mongo_upload(dyn_alt_corr_3Y, "collection_3Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Y, "collection_1Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Q, "collection_1Q_dyn_alt")
mongo_upload(dyn_alt_corr_1M, "collection_1M_dyn_alt")

# -----------------
# correlation total dataframes for dash

dash_correlation_df(CORR_WINDOW_LIST)

logging.info('btc_corr_dynamic_launcher.py end')
