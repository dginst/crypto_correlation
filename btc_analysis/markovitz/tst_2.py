
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
from btc_analysis.efficient_frontier import (
    sharpe_simulation, efficient_frontier,
    ret_vol_sharpe_from_w, optmization_single,
    min_max_ret, eff_front_op
)
from btc_analysis.mongo_func import (
    query_mongo
)
from btc_analysis.excel_func import (
    statistics_to_excel
)
from btc_analysis.statistics import (
    worst_drawdown, statistics_calc
)
import matplotlib.pyplot as plt

VARIOUS_LIST_Y = ["BTC",
                  "ETH",
                  "LTC",
                  "XRP",
                  'GOLD',
                  'COPPER',
                  'NATURAL_GAS',
                  'PETROL',
                  'CORN',
                  'EUR',
                  'GBP',
                  'JPY',
                  'CHF',
                  'NASDAQ',
                  'DOWJONES',
                  'S&P500',
                  'EUROSTOXX50',
                  'VIX',
                  'US_TREASURY',
                  'BBG Barclays PAN EURO Aggregate',
                  'US Aggregate Bond'
                  ]

all_price_df = query_mongo("btc_analysis", "all_prices_y")
w_price_df = all_price_df[["Date", "BTC"]]
prices = all_price_df[VARIOUS_LIST_Y]
log_ret_df = query_mongo("btc_analysis", "all_logreturns_y")
logs = log_ret_df[VARIOUS_LIST_Y]

tot_df, comp_tot_df = eff_front_op(
    prices, logs, stock_to_remove="BTC")

ef_df = pd.DataFrame(
    columns=['Return', 'Volatility w BTC', 'Volatility w_o BTC'])
ef_df['Return w BTC'] = tot_df["Return"]
ef_df['Return w_o BTC'] = comp_tot_df["Return"]
ef_df['Volatility w BTC'] = tot_df["Volatility"]
ef_df['Volatility w_o BTC'] = comp_tot_df["Volatility"]


statist_df = statistics_calc(all_price_df, "BTC")


statistics_to_excel("stat_test_y_19_11.xlsx", statist_df, ef_df, tot_df,
                    comp_tot_df)


moving_avgs_20 = all_price_df['BTC'].rolling(window=20).mean()
moving_avgs_120 = all_price_df['BTC'].rolling(window=120).mean()
moving_avgs_20.plot(label='20 days moving average')
moving_avgs_120.plot(label='120 days moving average')
all_price_df['BTC'].plot(label='Index Levels')
# plt.ylabel(ticker + ' levels')
# plt.legend()
# plt.title(ticker + ' levels and Moving averages')
plt.show()
