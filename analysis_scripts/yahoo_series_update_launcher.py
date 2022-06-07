import logging

from btc_analysis.config import (ASSET_LIST, CRYPTO_LIST, YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN)
from btc_analysis.market_data import mkt_data_op, yesterday_str
from btc_analysis.mongo_func import mongo_coll_drop, mongo_indexing

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('yahoo_series_update_launcher.py start')

# mongo collections oprerations
mongo_coll_drop("yahoo")
mongo_indexing()

# ---------------------------------------------
# yahoo series update

yesterday_str_ = yesterday_str()

list_to_return = CRYPTO_LIST + ASSET_LIST

mkt_data_op(YAHOO_TO_DOWNLOAD_CODE, YAHOO_TO_DOWNLOAD_NAME,
            list_to_return, "2015-12-31", yesterday_str_)


logging.info('yahoo_series_update_launcher.py end')
