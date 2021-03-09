from btc_analysis.config import DB_NAME
from btc_analysis.market_data import historical_vola
from btc_analysis.mongo_func import mongo_coll_drop, mongo_upload, query_mongo

mongo_coll_drop("vola")

return_df = query_mongo(DB_NAME, "all_returns_y")
logret_df = query_mongo(DB_NAME, "all_logreturns_y")

hist_vola_252 = historical_vola(return_df, logret_df, 252)
hist_vola_90 = historical_vola(return_df, logret_df, 90)
hist_vola_30 = historical_vola(return_df, logret_df, 30)

mongo_upload(hist_vola_252, "collection_volatility_252")
mongo_upload(hist_vola_90, "collection_volatility_90")
mongo_upload(hist_vola_30, "collection_volatility_30")
