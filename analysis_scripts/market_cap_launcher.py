from btc_analysis.config import (NAME_FOR_MKT_CAP, TICKERS_FOR_MKT_CAP)
from btc_analysis.market_data import (mkt_cap_op, yesterday_str
                                      )
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     )

mongo_indexing()


# -----------------------
# market cap update

mongo_coll_drop("market_cap")

yesterday_str = yesterday_str()

mkt_cap_op(TICKERS_FOR_MKT_CAP, NAME_FOR_MKT_CAP, yesterday_str)
