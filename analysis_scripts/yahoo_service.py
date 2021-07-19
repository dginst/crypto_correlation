from btc_analysis.config import (NAME_FOR_MKT_CAP, TICKERS_FOR_MKT_CAP,
                                 YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN,
                                 YAHOO_NAME_SERV, YAHOO_TO_DOWNLOAD_SERV)
from btc_analysis.market_data import (mkt_cap_op,
                                      mkt_data_op,
                                      yesterday_str,
                                      index_coll_check
                                      )
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     )

mongo_indexing()


# index_coll_check()
# ---------------------------------------------
# yahoo series update

mongo_coll_drop("yahoo")

yesterday_str = yesterday_str()

mkt_data_op(YAHOO_TO_DOWNLOAD_SERV, YAHOO_NAME_SERV,
            YAHOO_NAME_SERV, "2020-01-01", yesterday_str)
