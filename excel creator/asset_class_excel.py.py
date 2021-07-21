from pathlib import Path

from btc_analysis.calc import last_quarter_end
from btc_analysis.config import CORR_MATRIX_LIST, DB_NAME, VARIOUS_LIST_Y
from btc_analysis.excel_func import yahoo_to_excel
from btc_analysis.mongo_func import query_mongo

# ----------------------
# define the current end of quarter date

date = last_quarter_end(out="str_excel")

# -------------------------------------
# downloading from MongoDB

# mongo download for yahoo
dyn_yahoo_corr_3Y = query_mongo(DB_NAME, "dyn_yahoo_correlation_3Y")
dyn_yahoo_corr_1Y = query_mongo(DB_NAME, "dyn_yahoo_correlation_1Y")
dyn_yahoo_corr_1Q = query_mongo(DB_NAME, "dyn_yahoo_correlation_1Q")
dyn_yahoo_corr_1M = query_mongo(DB_NAME, "dyn_yahoo_correlation_1M")

stat_yahoo_corr_all = query_mongo(
    DB_NAME, "stat_yahoo_correlation_all_quarter")
stat_yahoo_corr_3Y = query_mongo(DB_NAME, "stat_yahoo_correlation_3Y_quarter")
stat_yahoo_corr_1Y = query_mongo(DB_NAME, "stat_yahoo_correlation_1Y_quarter")
stat_yahoo_corr_1Q = query_mongo(DB_NAME, "stat_yahoo_correlation_1Q_quarter")
stat_yahoo_corr_1M = query_mongo(DB_NAME, "stat_yahoo_correlation_1M_quarter")


# --------------------
# excel creation

file_name = "yahoo_correlation_" + date + ".xlsx"
spec_path = Path("excel creator", "output", file_name)

yahoo_to_excel(spec_path, VARIOUS_LIST_Y, CORR_MATRIX_LIST,
               dyn_yahoo_corr_3Y, dyn_yahoo_corr_1Y, dyn_yahoo_corr_1Q,
               dyn_yahoo_corr_1M, stat_yahoo_corr_all, stat_yahoo_corr_3Y,
               stat_yahoo_corr_1Y, stat_yahoo_corr_1Q, stat_yahoo_corr_1M)
