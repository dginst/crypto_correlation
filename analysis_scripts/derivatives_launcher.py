from btc_analysis.market_data import daily_btc_fut_download, btc_fut_downloader
from btc_analysis.config import BTC_FUT_TICKER, BTC_FUT_NAME

x = daily_btc_fut_download()
print(x)


# TBD