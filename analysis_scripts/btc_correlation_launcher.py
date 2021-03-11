from btc_analysis.mongo_func import (
    query_mongo, mongo_upload, mongo_coll_drop
)
from btc_analysis.config import (
    DB_NAME, INDEX_DB_NAME
)
from btc_analysis.calc import (
    return_retrieve, static_corr_op,
    dynamic_corr_op, price_retrieve
)

mongo_coll_drop("static_alt")
mongo_coll_drop("static_yahoo")
mongo_coll_drop("dynamic_alt")
mongo_coll_drop("dynamic_yahoo")

# --------------------------------------------
# BTC correlation with yahoo assets

tot_ret = query_mongo(DB_NAME, "all_returns_y")
tot_price = query_mongo(DB_NAME, "all_prices_y")

static_all, static_3Y, static_1Y, static_1Q, static_1M = static_corr_op(
    tot_ret)
corr_YTD, corr_3Y, corr_1Y, corr_1Q, corr_1M = dynamic_corr_op(
    tot_ret, "various_y")

mongo_upload(corr_YTD, "collection_YTD_dyn_yahoo")
mongo_upload(corr_3Y, "collection_3Y_dyn_yahoo")
mongo_upload(corr_1Y, "collection_1Y_dyn_yahoo")
mongo_upload(corr_1Q, "collection_1Q_dyn_yahoo")
mongo_upload(corr_1M, "collection_1M_dyn_yahoo")
mongo_upload(static_all, "collection_all_stat_yahoo")
mongo_upload(static_3Y, "collection_3Y_stat_yahoo")
mongo_upload(static_1Y, "collection_1Y_stat_yahoo")
mongo_upload(static_1Q, "collection_1Q_stat_yahoo")
mongo_upload(static_1M, "collection_1M_stat_yahoo")


# ------------------------------------------------------------------------
# BTC corelations with altcoins

alt_ret_df = return_retrieve("crypto_price_return", db_name=INDEX_DB_NAME)
alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)


(dyn_alt_corr_YTD, dyn_alt_corr_3Y, dyn_alt_corr_1Y,
 dyn_alt_corr_1Q, dyn_alt_corr_1M) = dynamic_corr_op(
    alt_ret_df, "altcoin")

(stat_alt_corr_all, stat_alt_corr_3Y, stat_alt_corr_1Y,
 stat_alt_corr_1Q, stat_alt_corr_1M) = static_corr_op(alt_ret_df)

mongo_upload(dyn_alt_corr_YTD, "collection_YTD_dyn_alt")
mongo_upload(dyn_alt_corr_3Y, "collection_3Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Y, "collection_1Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Q, "collection_1Q_dyn_alt")
mongo_upload(dyn_alt_corr_1M, "collection_1M_dyn_alt")
mongo_upload(stat_alt_corr_all, "collection_all_stat_alt")
mongo_upload(stat_alt_corr_3Y, "collection_3Y_stat_alt")
mongo_upload(stat_alt_corr_1Y, "collection_1Y_stat_alt")
mongo_upload(stat_alt_corr_1Q, "collection_1Q_stat_alt")
mongo_upload(stat_alt_corr_1M, "collection_1M_stat_alt")
