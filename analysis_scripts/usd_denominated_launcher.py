from btc_analysis.calc import usd_normalized_total
from btc_analysis.config import DB_NAME, WINDOW_LIST
from btc_analysis.mongo_func import mongo_coll_drop, query_mongo
from btc_analysis.dashboard_func import dash_usd_den_df

mongo_coll_drop("norm")

yahoo_ret_df = query_mongo(DB_NAME, "all_returns_y")

usd_normalized_total(yahoo_ret_df)

# ------------

dash_usd_den_df(WINDOW_LIST)
