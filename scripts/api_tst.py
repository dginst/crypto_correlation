import yfinance as yf
from datetime import datetime
from btc_analysis.calc import date_gen
import pandas as pd
import numpy as np
from btc_analysis.mongo_func import (
    mongo_upload, mongo_indexing, query_mongo,
    mongo_coll_drop
)
from btc_analysis.market_data import (
    mkt_data_op
)
from btc_analysis.config import (VARIOUS_LIST_Y)


# XW=F wheat
# ZC=F Corn 0.795082
# BKF 0.821206
# (PANUS) SCHZ 0.7328
# (PANEUR) C33.PA 0.796
# natural gas NG=F
mongo_coll_drop("yahoo")

# to_download = ["BTC", "Petrol", "Gold", "Corn",
#                "MSCI", "Natural Gas", "PANEUR", "PANUS", 'S&P500']

# to_download_code = ["BTC-USD", "CL=F", "GC=F",
#                     "XW=F", "BKF", "NG=F", "C33.PA", "SCHZ", '^GSPC']
to_download = ['S&P500',
               'DOWJONES',
               'GOLD',
               'SILVER',
               'COPPER',
               'NATURAL_GAS',
               'PETROL',
               'CORN',
               'EUR',
               'GBP',
               'JPY',
               'CHF',
               'EUROSTOXX50',
               'VIX',
               'NASDAQ',
               'US_TREASURY',
               'BBG Barclays PAN EURO Aggregate',
               'US Aggregate Bond',
               'US index',
               'TESLA',
               'AMAZON']

to_download_code = ['^GSPC',
                    '^DJI',
                    'GC=F',
                    'SI=F',
                    'HG=F',
                    'NG=F',
                    "CL=F",
                    "ZC=F",
                    'EURUSD=X',
                    'GBPUSD=X',
                    'JPYUSD=X',
                    'CHFUSD=X',
                    '^STOXX50E',
                    '^VIX',
                    '^IXIC',
                    'ZB=F',
                    'EAGG.PA',
                    'SCHZ',
                    'DX-Y.NYB',
                    'TSLA',
                    'AMZN']

# to_download = ["BTC", "Gold", "Silver", "Copper"]

# to_download_code = ["BTC-EUR", "GC=F", "SI=F", "HG=F"]

# mongo_coll_drop("yahoo_metal")

mkt_data_op(to_download_code, to_download, VARIOUS_LIST_Y,
            "2012-12-31", "2021-01-12")

###### test coorelation nuovo paniere #######################

# to_download = ["Petrol", "Corn", "MSCI", "Natural Gas", "PANEUR", "PANUS"]

# to_download_code = ["CL=F", "XW=F", "BKF", "NG=F", "C33.PA", "SCHZ"]

# var_ret = query_mongo("btc_analysis", "return_various")
# var_ret = var_ret.loc[var_ret.Date.between("2019-01-01", "2020-09-30")]
# print(var_ret)
# yah_ret = query_mongo("btc_analysis", "all_returns")

# wti_check = var_ret[["Date", "WTI"]]
# wti_check["Petrol"] = yah_ret["Petrol"]
# wti_petr_corr = wti_check.corr()
# print(wti_petr_corr)

# corn_check = var_ret[["Date", "GRAIN"]]
# corn_check["Corn"] = yah_ret["Corn"]
# corn_corr = corn_check.corr()
# print(corn_corr)

# metal_check = var_ret[["Date", "IND_METALS"]]
# metal_check["Metal"] = yah_ret["Metal"]
# metal_corr = metal_check.corr()
# print(metal_corr)

# M_check = var_ret[["Date", "MSCI BRIC "]]
# M_check["MSCI"] = yah_ret["MSCI"]
# M_corr = M_check.corr()
# print(M_corr)

# pane_check = var_ret[["Date", "BBG Barclays PAN EURO Aggregate"]]
# pane_check["PANEUR"] = yah_ret["PANEUR"]
# pane_corr = pane_check.corr()
# print(pane_corr)

# panus_check = var_ret[["Date", "BBG Barclays PAN US Aggregate"]]
# panus_check["PANUS"] = yah_ret["PANUS"]
# panus_corr = panus_check.corr()
# print(panus_corr)
