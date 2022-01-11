import logging

from btc_analysis.config import (YAHOO_TO_DOWNLOAD_CODE,
                                 YAHOO_TO_DOWNLOAD_NAME, YAHOO_TO_RETURN)
from btc_analysis.market_data import add_crypto, all_series_to_logret, all_series_to_return, mkt_data_op, yesterday_str
from btc_analysis.mongo_func import mongo_coll_drop, mongo_indexing, mongo_upload, query_mongo

# logging configuration
# logging.basicConfig(filename='log_file.log', filemode='a',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logging.info('yahoo_series_crypto_update_launcher.py start')

# mongo collections oprerations
price_df = query_mongo("btc_analysis", "all_prices_y")
complete_price_df = add_crypto(price_df)
print(complete_price_df)

return_ = all_series_to_return(complete_price_df, YAHOO_TO_RETURN)
print(return_)
logret = all_series_to_logret(complete_price_df)

volume_df = query_mongo("btc_analysis", "all_volume_y")
complete_vol_df = add_crypto(volume_df, collection="crypto_volume")
print(complete_vol_df)
mongo_coll_drop("yahoo")
mongo_upload(complete_price_df, "collection_prices_y")
mongo_upload(return_, "collection_returns_y")
mongo_upload(logret, "collection_logreturns_y")
mongo_upload(complete_vol_df, "collection_volume_y")

#logging.info('yahoo_series_update_launcher.py end')
