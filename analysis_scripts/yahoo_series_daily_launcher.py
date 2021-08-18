import logging

from btc_analysis.config import (YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN)
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

mkt_data_op(YAHOO_TO_DOWNLOAD_CODE, YAHOO_TO_DOWNLOAD_NAME,
            YAHOO_TO_RETURN, yesterday_str, today_str, daily="Y")


logging.info('yahoo_series_daily_launcher.py end')
