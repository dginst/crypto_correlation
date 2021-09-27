from pathlib import Path

from btc_analysis.calc import last_quarter_end
from btc_analysis.config import (CORR_MATRIX_LIST, CORR_MATRIX_LIST_ASSET,
                                 CORR_MATRIX_LIST_CRYPTO, DB_NAME)
from btc_analysis.excel_func import static_corr_to_excel
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

file_name_tot = "correlation_matrix_total_" + date + ".xlsx"
spec_path_tot = Path("excel creator", "output", file_name_tot)

static_corr_to_excel(spec_path_tot, CORR_MATRIX_LIST,
                     stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                     stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                     stat_yahoo_corr_1M)


file_name_asset = "correlation_matrix_asset_" + date + ".xlsx"
spec_path_asset = Path("excel creator", "output", file_name_asset)

static_corr_to_excel(spec_path_asset, CORR_MATRIX_LIST_ASSET,
                     stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                     stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                     stat_yahoo_corr_1M, matrix_type="asset")


file_name_crypto = "correlation_matrix_crypto_" + date + ".xlsx"
spec_path_crypto = Path("excel creator", "output", file_name_crypto)

static_corr_to_excel(spec_path_crypto, CORR_MATRIX_LIST_CRYPTO,
                     stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                     stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                     stat_yahoo_corr_1M, matrix_type="crypto")
