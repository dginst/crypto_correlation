import logging

from btc_analysis.market_data import crypto_price_and_vol_daily, yesterday_str, today_str
from btc_analysis.mongo_func import mongo_indexing, mongo_upload

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('crypto_series_daily_launcher.py start')

# mongo collections oprerations
mongo_indexing()

# ---------------------------------------------
# yahoo series update

today_str_ = today_str()
yesterday_str_ = yesterday_str()

crypto_prices, crypto_volumes =crypto_price_and_vol_daily(yesterday_str_, today_str_, how="yahoo")

mongo_upload(crypto_prices, "collection_crypto_prices")
mongo_upload(crypto_volumes, "collection_crypto_volume")

logging.info('crypto_series_daily_launcher.py end')