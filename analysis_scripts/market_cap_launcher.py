import logging

from btc_analysis.config import NAME_FOR_MKT_CAP, TICKERS_FOR_MKT_CAP
from btc_analysis.market_data import mkt_cap_op, yesterday_str
from btc_analysis.mongo_func import mongo_coll_drop, mongo_indexing

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('market_cap_launcher.py start')

# mongo collections operations
mongo_coll_drop("market_cap")

mongo_indexing()

# -----------------------
# market cap update

yesterday_str = yesterday_str()

mkt_cap_op(TICKERS_FOR_MKT_CAP, NAME_FOR_MKT_CAP, yesterday_str)


logging.info('market_cap_launcher.py end')
