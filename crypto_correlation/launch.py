from btc_analysis.mongo_func import (
    query_mongo, mongo_indexing, mongo_upload, mongo_coll_drop
)

from btc_analysis.config import (
    CRYPTO_LIST, CRYPTO_STATIC_LIST, DB_NAME,
    VARIOUS_LIST, INDEX_DB_NAME
)
from btc_analysis.calc import (
    roll_single_time, dynamic_corr,
    dynamic_total, static_corr, correlation_op,
    metal_corr_op, return_retrieve, static_corr_op,
    dynamic_corr_op, price_retrieve, return_in_btc_comp,
    yahoo_price_fix
)

from btc_analysis.excel_func import (
    alt_to_excel
)
import pandas as pd
from scipy.stats.stats import pearsonr
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


mongo_coll_drop("btc_den")
mongo_indexing()

tot_price = query_mongo(DB_NAME, "all_prices_y")
tot_price = yahoo_price_fix(tot_price)
# tot_price_a = yahoo_price_fix(tot_price[["Date", "AMAZON"]])

alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)

yahoo_df_3Y = return_in_btc_comp(tot_price, "3Y")
alt_df_3Y = return_in_btc_comp(alt_price_df, "3Y")

mongo_upload(yahoo_df_3Y, "collection_yahoo_btc_den_3Y")
mongo_upload(alt_df_3Y, "collection_alt_btc_den_3Y")

yahoo_df_1Y = return_in_btc_comp(tot_price, "1Y")
alt_df_1Y = return_in_btc_comp(alt_price_df, "1Y")

mongo_upload(yahoo_df_1Y, "collection_yahoo_btc_den_1Y")
mongo_upload(alt_df_1Y, "collection_alt_btc_den_1Y")

yahoo_df_6M = return_in_btc_comp(tot_price, "6M")
print(yahoo_df_6M)
alt_df_6M = return_in_btc_comp(alt_price_df, "6M")

mongo_upload(yahoo_df_6M, "collection_yahoo_btc_den_6M")
mongo_upload(alt_df_6M, "collection_alt_btc_den_6M")

yahoo_df_3M = return_in_btc_comp(tot_price, "3M")
alt_df_3M = return_in_btc_comp(alt_price_df, "3M")

mongo_upload(yahoo_df_3M, "collection_yahoo_btc_den_3M")
mongo_upload(alt_df_3M, "collection_alt_btc_den_3M")

yahoo_df_1M = return_in_btc_comp(tot_price, "1M")
alt_df_1M = return_in_btc_comp(alt_price_df, "1M")

mongo_upload(yahoo_df_1M, "collection_yahoo_btc_den_1M")
mongo_upload(alt_df_1M, "collection_alt_btc_den_1M")
