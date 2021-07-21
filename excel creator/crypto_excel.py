from pathlib import Path

from btc_analysis.calc import last_quarter_end
from btc_analysis.config import CRYPTO_LIST, CRYPTO_STATIC_LIST, DB_NAME
from btc_analysis.excel_func import alt_to_excel
from btc_analysis.mongo_func import query_mongo

# ----------------------
# define the current end of quarter date

date = last_quarter_end(out="str_excel")

# -------------------------------------
# downloading from MongoDB

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


# --------------------
# excel creation

file_name = "altcoin_correlation_" + date + ".xlsx"
spec_path = Path("excel creator", "output", file_name)

alt_to_excel(spec_path, CRYPTO_LIST, CRYPTO_STATIC_LIST,
             dyn_alt_corr_3Y, dyn_alt_corr_1Y,
             dyn_alt_corr_1Q, dyn_alt_corr_1M,
             stat_alt_corr_all, stat_alt_corr_3Y,
             stat_alt_corr_1Y,
             stat_alt_corr_1Q, stat_alt_corr_1M)
