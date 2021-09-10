from pathlib import Path

from btc_analysis.calc import last_quarter_end
from btc_analysis.config import (
    CORR_MATRIX_LIST, CORR_MATRIX_LIST_ASSET, CORR_MATRIX_LIST_CRYPTO)
from btc_analysis.excel_func import yahoo_csv_to_excel

# ----------------------
# define the current end of quarter date

date = last_quarter_end(out="str_excel")

# -------------------------------------

stat_yahoo_corr_all = "all.csv"
stat_yahoo_corr_3Y = "3y.csv"
stat_yahoo_corr_1Y = "1y.csv"
stat_yahoo_corr_1Q = "1q.csv"
stat_yahoo_corr_1M = "1m.csv"


# --------------------
# excel creation

file_name_tot = "correlation_matrix_total_" + date + ".xlsx"
spec_path_tot = Path("excel creator", "output", file_name_tot)

yahoo_csv_to_excel(spec_path_tot, CORR_MATRIX_LIST,
                   stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                   stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                   stat_yahoo_corr_1M)


file_name_asset = "correlation_matrix_asset_" + date + ".xlsx"
spec_path_asset = Path("excel creator", "output", file_name_asset)

yahoo_csv_to_excel(spec_path_asset, CORR_MATRIX_LIST_ASSET,
                   stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                   stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                   stat_yahoo_corr_1M, matrix_type="asset")


file_name_crypto = "correlation_matrix_crypto_" + date + ".xlsx"
spec_path_crypto = Path("excel creator", "output", file_name_crypto)

yahoo_csv_to_excel(spec_path_asset, CORR_MATRIX_LIST_CRYPTO,
                   stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                   stat_yahoo_corr_1Y, stat_yahoo_corr_1Q,
                   stat_yahoo_corr_1M)
