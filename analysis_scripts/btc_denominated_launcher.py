import logging

from btc_analysis.calc import (btc_denominated_total, price_retrieve,
                               yahoo_price_fix)
from btc_analysis.config import DB_NAME, INDEX_DB_NAME, WINDOW_LIST
from btc_analysis.dashboard_func import dash_btc_den_df
from btc_analysis.market_data import add_crypto_v2
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
#
crypto_price = query_mongo(DB_NAME, "crypto_prices")
yahoo_price_df = add_crypto_v2(all_yahoo_price, crypto_price)
yahoo_price_df = yahoo_price_fix(yahoo_price_df)
#
# yahoo_price_df = yahoo_price_fix(all_yahoo_price)

# alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)

btc_denominated_total(yahoo_price_df, yahoo_price_df)

# --------------
# total btc denominated dataframes for dashboard

dash_btc_den_df(WINDOW_LIST)


logging.info('btc_denominated_launcher.py end')
