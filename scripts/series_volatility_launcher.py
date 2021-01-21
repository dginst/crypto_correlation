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

hist_vola = hist_std_dev(logret_df)
hist_vola["Date"] = date

print(len(date) - 252)
hist_vola = hist_vola.tail(len(date) - 252)
print(hist_vola)
hist_vola.reset_index(drop=True, inplace=True)

mongo_upload(hist_vola, "collection_volatility_252")
