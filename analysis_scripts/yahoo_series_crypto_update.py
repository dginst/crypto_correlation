import logging

from btc_analysis.config import (YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN)
from btc_analysis.market_data import mkt_data_op, yesterday_str
from btc_analysis.mongo_func import mongo_coll_drop, mongo_indexing

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('yahoo_series_crypto_update_launcher.py start')

# mongo collections oprerations
mongo_coll_drop("yahoo")
mongo_indexing()

# ---------------------------------------------
# yahoo series update

yesterday_str = yesterday_str()

mkt_data_op(YAHOO_TO_DOWNLOAD_CODE, YAHOO_TO_DOWNLOAD_NAME,
            YAHOO_TO_RETURN, "2015-12-31", yesterday_str)


logging.info('yahoo_series_update_launcher.py end')
