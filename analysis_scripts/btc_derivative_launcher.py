from btc_analysis.config import (NAME_FOR_MKT_CAP, TICKERS_FOR_MKT_CAP,
                                 YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN)
from btc_analysis.market_data import (mkt_cap_op,
                                      mkt_data_op,
                                      yesterday_str,
                                      index_coll_check
                                      )
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     )

mongo_indexing()

initial_date = "01/01/2020"

yesterday_str = yesterday_str()


