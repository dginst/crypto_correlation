from btc_analysis.mongo_func import (
    mongo_indexing, mongo_coll_drop, query_mongo
)
from btc_analysis.market_data import (
    mkt_data_op, yesterday_str, stablecoin_volume, crypto_vol_no_stable
)
from btc_analysis.config import (
    YAHOO_TO_RETURN,
    YAHOO_TO_DOWNLOAD_CODE,
    YAHOO_TO_DOWNLOAD_NAME)


mongo_indexing()

# ---------------------------------------------
# yahoo series update

mongo_coll_drop("yahoo")

yesterday_str = yesterday_str()

mkt_data_op(YAHOO_TO_DOWNLOAD_CODE, YAHOO_TO_DOWNLOAD_NAME,
            YAHOO_TO_RETURN, "2015-12-31", yesterday_str)
