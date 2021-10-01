import logging

from btc_analysis.calc import price_retrieve, return_retrieve, static_corr_op
from btc_analysis.config import (CORR_MATRIX_LIST, DB_NAME, INDEX_DB_NAME,
                                 STAT_CORR_WINDOW_LIST)
from btc_analysis.dashboard_func import dash_static_corr_df
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)


# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('btc_corr_static_launcher.py start')

# mongo collections operations
mongo_coll_drop("static_alt")
mongo_coll_drop("static_yahoo")
mongo_indexing()

# --------------------------------------------
# BTC correlation with yahoo assets

tot_ret = query_mongo(DB_NAME, "all_returns_y")
tot_ret = tot_ret.rename(
    columns={'EUR Aggregate Bond': "PAN EUR"})
tot_price = query_mongo(DB_NAME, "all_prices_y")

static_all, static_3Y, static_1Y, static_1Q, static_1M = static_corr_op(
    tot_ret, CORR_MATRIX_LIST)

mongo_upload(static_all, "collection_all_stat_yahoo")
mongo_upload(static_3Y, "collection_3Y_stat_yahoo")
mongo_upload(static_1Y, "collection_1Y_stat_yahoo")
mongo_upload(static_1Q, "collection_1Q_stat_yahoo")
mongo_upload(static_1M, "collection_1M_stat_yahoo")

static_all_q, static_3Y_q, static_1Y_q, static_1Q_q, static_1M_q = static_corr_op(
    tot_ret, CORR_MATRIX_LIST, quarter="Y")

mongo_upload(static_all_q, "collection_all_stat_yahoo_quarter")
mongo_upload(static_3Y_q, "collection_3Y_stat_yahoo_quarter")
mongo_upload(static_1Y_q, "collection_1Y_stat_yahoo_quarter")
mongo_upload(static_1Q_q, "collection_1Q_stat_yahoo_quarter")
mongo_upload(static_1M_q, "collection_1M_stat_yahoo_quarter")

# -----------------
# correlation total dataframes for dash

dash_static_corr_df(STAT_CORR_WINDOW_LIST)

# ------------------------------------------------------------------------
# BTC correlations with altcoins

alt_ret_df = return_retrieve("crypto_price_return", db_name=INDEX_DB_NAME)
alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)

(stat_alt_corr_all, stat_alt_corr_3Y, stat_alt_corr_1Y,
 stat_alt_corr_1Q, stat_alt_corr_1M) = static_corr_op(alt_ret_df)

mongo_upload(stat_alt_corr_all, "collection_all_stat_alt")
mongo_upload(stat_alt_corr_3Y, "collection_3Y_stat_alt")
mongo_upload(stat_alt_corr_1Y, "collection_1Y_stat_alt")
mongo_upload(stat_alt_corr_1Q, "collection_1Q_stat_alt")
mongo_upload(stat_alt_corr_1M, "collection_1M_stat_alt")


logging.info('btc_corr_static_launcher.py end')
