from btc_analysis.mongo_func import (
    query_mongo, mongo_coll_drop,
    mongo_upload
)
from btc_analysis.statistics import (
    hist_std_dev
)
from btc_analysis.config import (
    DB_NAME
)


mongo_coll_drop("vola")

ret = query_mongo(DB_NAME, "all_returns_y")

date = ret["Date"]
date = date.sort_values(ascending=True)
date.reset_index(drop=True, inplace=True)

logret_df = query_mongo(DB_NAME, "all_logreturns_y")
logret_df.fillna(0, inplace=True)

hist_vola_252 = hist_std_dev(logret_df)
hist_vola_90 = hist_std_dev(logret_df, window=90)
hist_vola_30 = hist_std_dev(logret_df, window=30)

hist_vola_252["Date"] = date
hist_vola_90["Date"] = date
hist_vola_30["Date"] = date


hist_vola_252 = hist_vola_252.tail(len(date) - 252)
hist_vola_90 = hist_vola_252.tail(len(date) - 90)
hist_vola_30 = hist_vola_252.tail(len(date) - 30)


hist_vola_252.reset_index(drop=True, inplace=True)
hist_vola_90.reset_index(drop=True, inplace=True)
hist_vola_30.reset_index(drop=True, inplace=True)

mongo_upload(hist_vola_252, "collection_volatility_252")
mongo_upload(hist_vola_90, "collection_volatility_90")
mongo_upload(hist_vola_30, "collection_volatility_30")
