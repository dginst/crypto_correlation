import logging

from btc_analysis.market_data import crypto_price_and_volume
from btc_analysis.mongo_func import mongo_coll_drop, mongo_upload, query_mongo

# logging configuration
logging.basicConfig(filename='log_file.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('crypto_series_setup_launcher.py start')

# mongo collections oprerations
mongo_coll_drop("crypto_all")

index_crypto_prices = query_mongo("index", "crypto_price")
index_crypto_volume = query_mongo("index", "crypto_volume")

# put new_coin_stop_date="index_start" and use_index=True to use the index values and collections
crypto_prices, crypto_volumes = crypto_price_and_volume(index_crypto_prices, index_crypto_prices, use_index=False)

print(crypto_prices)

mongo_upload(crypto_prices, "collection_crypto_prices")
mongo_upload(crypto_volumes, "collection_crypto_volume")

logging.info('crypto_series_setup_launcher.py end')