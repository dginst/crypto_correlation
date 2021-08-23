from pathlib import Path

from btc_analysis.calc import last_quarter_end
from btc_analysis.config import CORR_MATRIX_LIST
from btc_analysis.excel_func import yahoo_csv_to_excel

# ----------------------
# define the current end of quarter date

date = last_quarter_end(out="str_excel")

# -------------------------------------

stat_yahoo_corr_all = ""
stat_yahoo_corr_3Y = ""
stat_yahoo_corr_1Y = ""
stat_yahoo_corr_1Q = ""
stat_yahoo_corr_1M = ""


# --------------------
# excel creation

file_name = "correlation_matrix" + date + ".xlsx"
spec_path = Path("excel creator", "output", file_name)

yahoo_csv_to_excel(spec_path, CORR_MATRIX_LIST,
                   stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                   stat_yahoo_corr_1Y, stat_yahoo_corr_1Q, stat_yahoo_corr_1M)
