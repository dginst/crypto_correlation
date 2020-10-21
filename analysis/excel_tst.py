from mongo_func import query_mongo
from excel_func import corr_to_excel
from config import DB_NAME


dyn_var_corr_3Y = query_mongo(DB_NAME, "dyn_var_correlation_3Y")
dyn_var_corr_1Y = query_mongo(DB_NAME, "dyn_var_correlation_1Y")
dyn_var_corr_1Q = query_mongo(DB_NAME, "dyn_var_correlation_1Q")
dyn_var_corr_1M = query_mongo(DB_NAME, "dyn_var_correlation_1M")
stat_var_corr_all = query_mongo(DB_NAME, "stat_var_correlation_all")
stat_var_corr_3Y = query_mongo(DB_NAME, "stat_var_correlation_3Y")
stat_var_corr_1Y = query_mongo(DB_NAME, "stat_var_correlation_1Y")
stat_var_corr_1Q = query_mongo(DB_NAME, "stat_var_correlation_1Q")
stat_var_corr_1M = query_mongo(DB_NAME, "stat_var_correlation_1M")
dyn_SP500_corr_3Y = query_mongo(DB_NAME, "dyn_SP500_correlation_3Y")

corr_to_excel(dyn_var_corr_3Y, dyn_var_corr_1Y,
              dyn_var_corr_1Q, dyn_var_corr_1M,
              stat_var_corr_all, stat_var_corr_3Y,
              stat_var_corr_1Y,
              stat_var_corr_1Q, stat_var_corr_1M,
              dyn_SP500_corr_3Y)
