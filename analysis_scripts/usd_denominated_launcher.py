import logging

from btc_analysis.calc import usd_normalized_total
from btc_analysis.config import DB_NAME, WINDOW_LIST
from btc_analysis.dashboard_func import dash_usd_den_df
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     query_mongo)

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('usd_denominated_launcher.py start')

# mongo collection operations

mongo_coll_drop("norm")

mongo_indexing()

# usd denominated computation

yahoo_ret_df = query_mongo(DB_NAME, "all_returns_y")

usd_normalized_total(yahoo_ret_df)

# reunification of collection for dashboard

dash_usd_den_df(WINDOW_LIST)

logging.info('usd_denominated_launcher.py end')
