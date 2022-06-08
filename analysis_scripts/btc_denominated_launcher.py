import logging

from btc_analysis.calc import btc_denominated_total
from btc_analysis.config import DB_NAME, WINDOW_LIST
from btc_analysis.dashboard_func import dash_btc_den_df
from btc_analysis.mongo_func import (mongo_coll_drop, mongo_indexing,
                                     query_mongo)


# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('btc_denominated_launcher.py start')

# mongo collections operations
mongo_coll_drop("btc_den")
mongo_indexing()

all_yahoo_price = query_mongo(DB_NAME, "all_prices_y")

btc_denominated_total(all_yahoo_price)

# --------------
# total btc denominated dataframes for dashboard

dash_btc_den_df(WINDOW_LIST)


logging.info('btc_denominated_launcher.py end')
