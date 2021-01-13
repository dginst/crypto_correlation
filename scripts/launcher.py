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
    dynamic_corr_op, price_retrieve
)

from btc_analysis.excel_func import (
    alt_to_excel
)
import pandas as pd
from scipy.stats.stats import pearsonr
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
# mongo_indexing()

# price_df = query_mongo(DB_NAME, "all_prices")
# for y in VARIOUS_LIST:

#     price_df[y] = [float(x) for x in price_df[y]]

# return_df = price_df.sort_values(by=["Date"], ascending=True)
# return_df = return_df.reset_index(drop=True)
# print(return_df)

# date = pd.DataFrame(columns=["Date"])
# date["Date"] = return_df["Date"]
# print(date)
# return_df = return_df.drop(columns=["Date"])
# return_df = return_df.pct_change()


# return_df["Date"] = date["Date"]

# return_df = return_df[["Date", "BITCOIN", "ETH", "LTC", "XRP", "GOLD", "IND_METALS", "WTI",
#                        "GRAIN", "EUR", "CHF", "GBP", "JPY",
#                        "NASDAQ", "EUROSTOXX50", "S&P500",
#                        "MSCI BRIC ", "VIX Index",
#                        "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
#                        "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]]
# return_df = return_df.sort_values(by=["Date"], ascending=False)
# tot_ret = return_df.reset_index(drop=True)
# mongo_upload(tot_ret, "collection_returns")
# return_df = query_mongo(DB_NAME, "return_crypto")

# return_df = return_df.sort_values(by=["Date"], ascending=False)
# return_df.reset_index(drop=True, inplace=True)

# for y in CRYPTO_LIST:

#     return_df[y] = [float(x) for x in return_df[y]]

# print(return_df)

# tot = static_corr(return_df, "1Y")
# # mongo_upload(tot, "collection_static_alt")
# print(tot)
mongo_coll_drop("static_alt")
mongo_coll_drop("static_yahoo")
mongo_coll_drop("dynamic_alt")
mongo_coll_drop("dynamic_yahoo")

tot_ret = query_mongo(DB_NAME, "all_returns_y")
tot_price = query_mongo(DB_NAME, "all_prices_y")

static_all, static_3Y, static_1Y, static_1Q, static_1M = static_corr_op(
    tot_ret)
corr_3Y, corr_1Y, corr_1Q, corr_1M = dynamic_corr_op(tot_ret, "various_y")


mongo_upload(corr_3Y, "collection_3Y_dyn_yahoo")
mongo_upload(corr_1Y, "collection_1Y_dyn_yahoo")
mongo_upload(corr_1Q, "collection_1Q_dyn_yahoo")
mongo_upload(corr_1M, "collection_1M_dyn_yahoo")
mongo_upload(static_all, "collection_all_stat_yahoo")
mongo_upload(static_3Y, "collection_3Y_stat_yahoo")
mongo_upload(static_1Y, "collection_1Y_stat_yahoo")
mongo_upload(static_1Q, "collection_1Q_stat_yahoo")
mongo_upload(static_1M, "collection_1M_stat_yahoo")

# mongo_upload(corr_3Y, "collection_3Y_dyn_var")
# mongo_upload(corr_1Y, "collection_1Y_dyn_var")
# mongo_upload(corr_1Q, "collection_1Q_dyn_var")
# mongo_upload(corr_1M, "collection_1M_dyn_var")
# mongo_upload(static_all, "collection_all_stat_var")
# mongo_upload(static_3Y, "collection_3Y_stat_var")
# mongo_upload(static_1Y, "collection_1Y_stat_var")
# mongo_upload(static_1Q, "collection_1Q_stat_var")
# mongo_upload(static_1M, "collection_1M_stat_var")

# corr_1Y = dynamic_total(tot_ret, "1Y")
# mongo_upload(corr_1Y, "collection_1Y_dyn")
# corr_1Q = dynamic_total(tot_ret, "1Q")
# mongo_upload(corr_1Q, "collection_1Q_dyn")
# corr_3M = dynamic_total(tot_ret, "1M")
# mongo_upload(corr_3M, "collection_3M_dyn")

# btc_ret = tot_ret[["Date", "BTC"]]

# eth_ret = tot_ret[["Date", "ETH"]]

# prov = dynamic_corr(btc_ret, eth_ret, "1Y")

# print(prov)

# merged = btc_ret
# merged["ETH"] = eth_ret
# corr_tot = merged.corr()
# print(btc_ret)
# print(eth_ret)

# correl = btc_ret.corr()
# print(correl)

# s = roll_time(tot_ret["Date"], "1Y")

# s = s.sort_values(by=["Date"], ascending=False)

# print(s)

# alt_ret_df = return_retrieve("crypto_price_return", db_name='index')
# print(alt_ret_df)
# correlation_op()
# # metal_corr_op()

# # mongo download for Altcoin Correlation
# dyn_alt_corr_3Y = query_mongo(DB_NAME, "dyn_alt_correlation_3Y")
# dyn_alt_corr_1Y = query_mongo(DB_NAME, "dyn_alt_correlation_1Y")
# dyn_alt_corr_1Q = query_mongo(DB_NAME, "dyn_alt_correlation_1Q")
# dyn_alt_corr_1M = query_mongo(DB_NAME, "dyn_alt_correlation_1M")
# stat_alt_corr_all = query_mongo(DB_NAME, "stat_alt_correlation_all")
# stat_alt_corr_3Y = query_mongo(DB_NAME, "stat_alt_correlation_3Y")
# stat_alt_corr_1Y = query_mongo(DB_NAME, "stat_alt_correlation_1Y")
# stat_alt_corr_1Q = query_mongo(DB_NAME, "stat_alt_correlation_1Q")
# stat_alt_corr_1M = query_mongo(DB_NAME, "stat_alt_correlation_1M")

# alt_to_excel('_Altcoin-Correlations.xlsx', CRYPTO_LIST, CRYPTO_STATIC_LIST,
#              dyn_alt_corr_3Y, dyn_alt_corr_1Y,
#              dyn_alt_corr_1Q, dyn_alt_corr_1M,
#              stat_alt_corr_all, stat_alt_corr_3Y,
#              stat_alt_corr_1Y,
#              stat_alt_corr_1Q, stat_alt_corr_1M)
alt_ret_df = return_retrieve("crypto_price_return", db_name=INDEX_DB_NAME)
alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)


(dyn_alt_corr_3Y, dyn_alt_corr_1Y,
 dyn_alt_corr_1Q, dyn_alt_corr_1M) = dynamic_corr_op(
    alt_ret_df, "altcoin")

(stat_alt_corr_all, stat_alt_corr_3Y, stat_alt_corr_1Y,
 stat_alt_corr_1Q, stat_alt_corr_1M) = static_corr_op(alt_ret_df)

mongo_upload(dyn_alt_corr_3Y, "collection_3Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Y, "collection_1Y_dyn_alt")
mongo_upload(dyn_alt_corr_1Q, "collection_1Q_dyn_alt")
mongo_upload(dyn_alt_corr_1M, "collection_1M_dyn_alt")
mongo_upload(stat_alt_corr_all, "collection_all_stat_alt")
mongo_upload(stat_alt_corr_3Y, "collection_3Y_stat_alt")
mongo_upload(stat_alt_corr_1Y, "collection_1Y_stat_alt")
mongo_upload(stat_alt_corr_1Q, "collection_1Q_stat_alt")
mongo_upload(stat_alt_corr_1M, "collection_1M_stat_alt")
