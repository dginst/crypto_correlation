from btc_analysis.mongo_func import query_mongo
from btc_analysis.excel_func import (corr_to_excel, metal_corr_to_excel,
                                     var_to_excel, yahoo_to_excel, alt_to_excel)

from btc_analysis.config import (DB_NAME, VARIOUS_LIST, VAR_STATIC_LIST,
                                 VARIOUS_LIST_Y, VAR_STATIC_LIST_Y,
                                 CRYPTO_LIST, CRYPTO_STATIC_LIST,
                                 )


# mongo download for Altcoin Correlation
dyn_alt_corr_3Y = query_mongo(DB_NAME, "dyn_alt_correlation_3Y")
dyn_alt_corr_1Y = query_mongo(DB_NAME, "dyn_alt_correlation_1Y")
dyn_alt_corr_1Q = query_mongo(DB_NAME, "dyn_alt_correlation_1Q")
dyn_alt_corr_1M = query_mongo(DB_NAME, "dyn_alt_correlation_1M")
stat_alt_corr_all = query_mongo(DB_NAME, "stat_alt_correlation_all")

stat_alt_corr_3Y = query_mongo(DB_NAME, "stat_alt_correlation_3Y")

stat_alt_corr_1Y = query_mongo(DB_NAME, "stat_alt_correlation_1Y")

stat_alt_corr_1Q = query_mongo(DB_NAME, "stat_alt_correlation_1Q")

stat_alt_corr_1M = query_mongo(DB_NAME, "stat_alt_correlation_1M")


# mongo download for yahoo
dyn_yahoo_corr_3Y = query_mongo(DB_NAME, "dyn_yahoo_correlation_3Y")
dyn_yahoo_corr_1Y = query_mongo(DB_NAME, "dyn_yahoo_correlation_1Y")
dyn_yahoo_corr_1Q = query_mongo(DB_NAME, "dyn_yahoo_correlation_1Q")
dyn_yahoo_corr_1M = query_mongo(DB_NAME, "dyn_yahoo_correlation_1M")
stat_yahoo_corr_all = query_mongo(DB_NAME, "stat_yahoo_correlation_all")
print(stat_yahoo_corr_all)

stat_yahoo_corr_all = stat_yahoo_corr_all.drop(index=[7, 22, 23, 24, 25, 26],
                                               columns=["AMAZON", "SILVER", "US index", "APPLE", "TESLA", "NETFLIX"])
stat_yahoo_corr_3Y = query_mongo(DB_NAME, "stat_yahoo_correlation_3Y")
stat_yahoo_corr_3Y = stat_yahoo_corr_3Y.drop(index=[7, 22, 23, 24, 25, 26],
                                             columns=["AMAZON", "SILVER", "US index", "APPLE", "TESLA", "NETFLIX"])
stat_yahoo_corr_1Y = query_mongo(DB_NAME, "stat_yahoo_correlation_1Y")
stat_yahoo_corr_1Y = stat_yahoo_corr_1Y.drop(index=[7, 22, 23, 24, 25, 26],
                                             columns=["AMAZON", "SILVER", "US index", "APPLE", "TESLA", "NETFLIX"])
stat_yahoo_corr_1Q = query_mongo(DB_NAME, "stat_yahoo_correlation_1Q")
stat_yahoo_corr_1Q = stat_yahoo_corr_1Q.drop(index=[7, 22, 23, 24, 25, 26],
                                             columns=["AMAZON", "SILVER", "US index", "APPLE", "TESLA", "NETFLIX"])
stat_yahoo_corr_1M = query_mongo(DB_NAME, "stat_yahoo_correlation_1M")
stat_yahoo_corr_1M = stat_yahoo_corr_1M.drop(index=[7, 22, 23, 24, 25, 26],
                                             columns=["AMAZON", "SILVER", "US index", "APPLE", "TESLA", "NETFLIX"])

# corr_to_excel(dyn_var_corr_3Y, dyn_var_corr_1Y,
#               dyn_var_corr_1Q, dyn_var_corr_1M,
#               stat_var_corr_all, stat_var_corr_3Y,
#               stat_var_corr_1Y, stat_var_corr_1Q,
#               stat_var_corr_1M, dyn_SP500_corr_3Y,
#               dyn_alt_corr_3Y, dyn_alt_corr_1Y,
#               dyn_alt_corr_1Q, dyn_alt_corr_1M,
#               stat_alt_corr_all, stat_alt_corr_3Y,
#               stat_alt_corr_1Y, stat_alt_corr_1Q,
#               stat_alt_corr_1M)


# # metal part
# dyn_met_corr_3Y = query_mongo(DB_NAME, "dyn_met_correlation_3Y")
# dyn_met_corr_1Y = query_mongo(DB_NAME, "dyn_met_correlation_1Y")
# dyn_met_corr_1Q = query_mongo(DB_NAME, "dyn_met_correlation_1Q")
# dyn_met_corr_1M = query_mongo(DB_NAME, "dyn_met_correlation_1M")

# metal_corr_to_excel(dyn_met_corr_3Y, dyn_met_corr_1Y,
#                     dyn_met_corr_1Q, dyn_met_corr_1M)


# var_to_excel('file_name_var.xlsx', VARIOUS_LIST, VAR_STATIC_LIST,
#              dyn_var_corr_3Y, dyn_var_corr_1Y,
#              dyn_var_corr_1Q, dyn_var_corr_1M,
#              stat_var_corr_all, stat_var_corr_3Y,
#              stat_var_corr_1Y,
#              stat_var_corr_1Q, stat_var_corr_1M,
#              )

yahoo_to_excel("yahoo_correlation_27_01_2021.xlsx", VARIOUS_LIST_Y, VAR_STATIC_LIST_Y,
               dyn_yahoo_corr_3Y, dyn_yahoo_corr_1Y, dyn_yahoo_corr_1Q,
               dyn_yahoo_corr_1M, stat_yahoo_corr_all, stat_yahoo_corr_3Y,
               stat_yahoo_corr_1Y, stat_yahoo_corr_1Q, stat_yahoo_corr_1M)


alt_to_excel("altcoin_correlation_27_01_2021.xlsx",  CRYPTO_LIST, CRYPTO_STATIC_LIST,
             dyn_alt_corr_3Y, dyn_alt_corr_1Y,
             dyn_alt_corr_1Q, dyn_alt_corr_1M,
             stat_alt_corr_all, stat_alt_corr_3Y,
             stat_alt_corr_1Y,
             stat_alt_corr_1Q, stat_alt_corr_1M)
