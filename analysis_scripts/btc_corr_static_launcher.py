from btc_analysis.mongo_func import (
    query_mongo, mongo_upload, mongo_coll_drop
)
from btc_analysis.config import (
    DB_NAME, INDEX_DB_NAME, CORR_WINDOW_LIST, CORR_MATRIX_LIST
)
from btc_analysis.calc import (
    return_retrieve, static_corr_op,
    dynamic_corr_op, price_retrieve
)
from btc_analysis.dashboard_func import (dash_correlation_df)

mongo_coll_drop("static_alt")
mongo_coll_drop("static_yahoo")

# --------------------------------------------
# BTC correlation with yahoo assets

tot_ret = query_mongo(DB_NAME, "all_returns_y")
tot_price = query_mongo(DB_NAME, "all_prices_y")

static_all, static_3Y, static_1Y, static_1Q, static_1M = static_corr_op(
    tot_ret, CORR_MATRIX_LIST)

mongo_upload(static_all, "collection_all_stat_yahoo")
mongo_upload(static_3Y, "collection_3Y_stat_yahoo")
mongo_upload(static_1Y, "collection_1Y_stat_yahoo")
mongo_upload(static_1Q, "collection_1Q_stat_yahoo")
mongo_upload(static_1M, "collection_1M_stat_yahoo")


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

# -----------------
# correlation total dataframes for dash
