import logging

from btc_analysis.config import (ASSET_LIST, CRYPTO_LIST, YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME)
from btc_analysis.market_data import mkt_data_op, yesterday_str, today_str
from btc_analysis.mongo_func import mongo_indexing

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('yahoo_series_daily_launcher.py start')

# mongo collections oprerations
mongo_indexing()

# ---------------------------------------------
# yahoo series update

today_str = today_str()
yesterday_str = yesterday_str()

list_to_return = CRYPTO_LIST + ASSET_LIST

mkt_data_op(YAHOO_TO_DOWNLOAD_CODE, YAHOO_TO_DOWNLOAD_NAME,
            list_to_return, yesterday_str, today_str, daily="Y")


logging.info('yahoo_series_daily_launcher.py end')
