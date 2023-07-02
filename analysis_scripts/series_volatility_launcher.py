import logging

from btc_analysis.config import DB_NAME, VOLA_DAY_LIST
from btc_analysis.dashboard_func import dash_volatility_df
from btc_analysis.market_data import ewm_volatility, historical_vola, decay_volatility
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     mongo_upload, query_mongo)

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('series_volatility_launcher.py start')

# mongo collections operations
mongo_coll_drop("vola")
mongo_indexing()

return_df = query_mongo(DB_NAME, "all_returns_y")
logret_df = query_mongo(DB_NAME, "all_logreturns_y")

hist_vola_252 = historical_vola(return_df, logret_df, 252)
hist_vola_90 = historical_vola(return_df, logret_df, 90)
hist_vola_30 = historical_vola(return_df, logret_df, 30)
ewma_vola = ewm_volatility(return_df)


mongo_upload(hist_vola_252, "collection_volatility_252")
mongo_upload(hist_vola_90, "collection_volatility_90")
mongo_upload(hist_vola_30, "collection_volatility_30")
mongo_upload(ewma_vola, "collection_volatility_ewm")


# --------
# dataframes unification for dashboard
dash_volatility_df(VOLA_DAY_LIST)


logging.info('series_volatility_launcher.py end')
