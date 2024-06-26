DB_NAME = "btc_analysis"

MKT_ANALYSIS_START_DATE = "2012-12-31"

INDEX_START_DATE = "2016-01-01"

INDEX_DB_NAME = "index"

DAY_IN_SECONDS = 86400

SATOSHI_FOR_BTC = 100000000

# -----

CORR_WINDOW_LIST = ["3Y", "1Y", "1Q", "1M", "YTD"]

WINDOW_LIST = ["5Y", "3Y", "2Y", "1Y", "6M", "3M", "1M", "1W", "YTD"]

TIME_WINDOW = ["All", "3Y", "1Y", "1Q", "1M"]

STAT_CORR_WINDOW_LIST = ["all", "3Y", "1Y", "1Q", "1M"]

VOLA_DAY_LIST = ["252", "90", "30", "ewm"]

# -----------------------------------
# Crypto and anssets definition
# --------------------------------------

ASSET_CATEGORY = [
    "Crypto-currency",
    "Commodity",
    "Currency",
    "Equity",
    "Volatility",
    "Bond",
]

ORIGINAL_CRYPTO_LIST = [
    "BTC",
    "ETH",
    "XRP",
    "LTC",
    "BCH",
    "EOS",
    "ETC",
    "ZEC",
    "ADA",
    "XLM",
    "XMR",
    "BSV",
]


NEW_CRYPTO_LIST = ["MATIC", "SHIB", "AVAX", "DOGE", "DOT", "LUNA", "SOL"]

CRYPTO_LIST = ORIGINAL_CRYPTO_LIST + NEW_CRYPTO_LIST

ASSET_LIST = [
    "S&P500",
    "DOWJONES",
    "GOLD",
    "SILVER",
    "COPPER",
    "NATURAL_GAS",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "EUROSTOXX50",
    "VIX",
    "NASDAQ",
    "US TREASURY",
    "EUR Aggregate Bond",
    "US Aggregate Bond",
    "US index",
    "TESLA",
    "AMAZON",
    "APPLE",
    "NETFLIX",
    "NVIDIA",
]


# ------------------------------
# list for dynamic correlation
# ------------------------------

VARIOUS_LIST_Y = ["BTC"] + ASSET_LIST

REF_CRYPTO = "BTC"

# ------------------------------
# list for static correlation
# ------------------------------

METAL_LIST = ["Gold", "Silver", "Copper"]

CRYPTO_STATIC_LIST = [
    "BTC",
    "ETH",
    "XRP",
    "LTC",
    "BCH",
    "EOS",
    "ETC",
    "ZEC",
    "ADA",
    "XLM",
    "XMR",
    "BSV",
    "MATIC",
    "SHIB",
    "ADA",
    "AVAX",
    "DOGE",
    "DOT",
    "LUNA",
]


EQUITY = ["NASDAQ", "EUROSTOXX50", "S&P500", "MSCI BRIC ", "VIX Index"]

EQUITY_YAHOO = ["NASDAQ", "S&P500", "EUROSTOXX50", "VIX"]

BOND = [
    "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
    "BBG Barclays PAN EURO Aggregate",
    "BBG Barclays PAN US Aggregate",
]

BOND_YAHOO = ["US TREASURY", "PAN EUR"]

CURRENCY = ["EUR", "GBP", "JPY", "CHF"]

COMMODITY = ["GOLD", "IND_METALS", "WTI", "GRAIN"]

COMMODITY_YAHOO = ["GOLD", "COPPER", "CRUDE OIL", "CORN"]

CRYPTO_FOR_STATIC = ["BITCOIN", "ETH", "LTC", "XRP"]

CRYPTO_FOR_STATIC_YAHOO = ["BTC", "ETH", "LTC", "XRP"]

CRYPTO = [
    "BITCOIN",
    "BTC",
    "ETH",
    "LTC",
    "XRP",
    "BCH",
    "EOS",
    "ETC",
    "ZEC",
    "ADA",
    "XLM",
    "XMR",
    "BSV",
    "SOL",
]


SP500_GRAPH_LIST = [
    "BITCOIN",
    "GOLD",
    "GRAIN",
    "EUR",
    "JPY",
    "EUROSTOXX50",
    "VIX Index",
    "BBG Barclays PAN EURO Aggregate",
    "BBG Barclays PAN US Aggregate",
]

VAR_GRAPH_LIST = [
    "ETH",
    "XRP",
    "LTC",
    "GOLD",
    "GRAIN",
    "EUR",
    "JPY",
    "EUROSTOXX50",
    "S&P500",
    "VIX Index",
    "NASDAQ",
    "PETROL" "BBG Barclays PAN EURO Aggregate",
    "BBG Barclays PAN US Aggregate",
    "CORN",
    "US TREASURY",
    "BBG Barclays PAN EURO Aggregate",
]


CRYPTO_GRAPH_LIST = [
    "ETH",
    "XRP",
    "LTC",
    "BCH",
    "EOS",
    "ETC",
    "ZEC",
    "ADA",
    "XLM",
    "XMR",
    "BSV",
    "SOL",
]

METAL_GRAPH_LIST = ["Gold", "Silver", "Copper"]

VAR_STATIC_LIST = [
    "Date",
    "BITCOIN",
    "ETH",
    "LTC",
    "XRP",
    "GOLD",
    "IND_METALS",
    "WTI",
    "GRAIN",
    "EUR",
    "CHF",
    "GBP",
    "JPY",
    "NASDAQ",
    "EUROSTOXX50",
    "S&P500",
    "MSCI BRIC ",
    "VIX Index",
    "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
    "BBG Barclays PAN EURO Aggregate",
    "BBG Barclays PAN US Aggregate",
]

VAR_STATIC_LIST_Y = [
    "Date",
    "BTC",
    "ETH",
    "LTC",
    "XRP",
    "GOLD",
    "COPPER",
    "NATURAL_GAS",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "NASDAQ",
    "DOWJONES",
    "S&P500",
    "EUROSTOXX50",
    "VIX",
    "US TREASURY",
    "EUR Aggregate Bond",
    "US Aggregate Bond",
]

CORR_MATRIX_LIST = [
    "Date",
    "BTC",
    "ETH",
    "LTC",
    "XRP",
    "GOLD",
    "COPPER",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "NASDAQ",
    "S&P500",
    "EUROSTOXX50",
    "VIX",
    "US TREASURY",
    "EUR Aggregate Bond",
]


# ------------------------------------
# Variables for dashboards
# -------------------------------------------

GRAPH_LINE_WIDTH = 2


GRAPH_COLOR = {
    # commodity color
    "GRAIN": {
        "color": "#01A801",
        "width": GRAPH_LINE_WIDTH,
    },
    "CORN": {
        "color": "#01A801",
        "width": GRAPH_LINE_WIDTH,
    },
    "CRUDE OIL": {
        "color": "#CCCCCC",
        "width": GRAPH_LINE_WIDTH,
    },
    "NATURAL_GAS": {
        "color": "#01A801",
        "width": GRAPH_LINE_WIDTH,
    },
    # metal colors
    "Gold": {"color": "#00FF00", "width": GRAPH_LINE_WIDTH},
    "GOLD": {"color": "#00FF00", "width": GRAPH_LINE_WIDTH},
    "Silver": {"color": "#CCCCCC", "width": GRAPH_LINE_WIDTH},
    "SILVER": {"color": "#CCCCCC", "width": GRAPH_LINE_WIDTH},
    "Copper": {"color": "#B45F06", "width": GRAPH_LINE_WIDTH},
    "COPPER": {"color": "#B45F06", "width": GRAPH_LINE_WIDTH},
    # currency color
    "EUR": {"color": "#0000FF", "width": GRAPH_LINE_WIDTH},
    "JPY": {
        "color": "#0404B2",
        "width": GRAPH_LINE_WIDTH,
    },
    "GBP": {
        "color": "#3D85C6",
        "width": GRAPH_LINE_WIDTH,
    },
    "CHF": {
        "color": "#CC0000",
        "width": GRAPH_LINE_WIDTH,
    },
    # index color
    "EUROSTOXX50": {
        "color": "#444444",
        "width": GRAPH_LINE_WIDTH,
    },
    "S&P500": {"color": "#666666", "width": GRAPH_LINE_WIDTH},
    "VIX Index": {
        "color": "#6E6D6D",
        "width": GRAPH_LINE_WIDTH,
    },
    "VIX": {
        "color": "#6E6D6D",
        "width": GRAPH_LINE_WIDTH,
    },
    # treasury and bond color
    "EUR Aggregate Bond": {
        "color": "#999999",
        "width": GRAPH_LINE_WIDTH,
        # 'dash_type': 'long_dash'
    },
    "US Aggregate Bond": {
        "color": "#CCCCCC",
        "width": GRAPH_LINE_WIDTH,
    },
    "US TREASURY": {
        "color": "#999999",
        "width": GRAPH_LINE_WIDTH,
        # 'dash_type': 'long_dash'
    },
    # crytpo color
    "BITCOIN": {"color": "#FF9900", "width": GRAPH_LINE_WIDTH},
    "BTC": {"color": "#FF9900", "width": GRAPH_LINE_WIDTH},
    "ETH": {"color": "#0000FF", "width": GRAPH_LINE_WIDTH},
    "XRP": {"color": "#CC0000", "width": GRAPH_LINE_WIDTH},
    "LTC": {"color": "#CCCCCC", "width": GRAPH_LINE_WIDTH},
    "BCH": {"color": "#01A801", "width": GRAPH_LINE_WIDTH},
    "EOS": {"color": "#FFFF00", "width": GRAPH_LINE_WIDTH},
    "ETC": {"color": "#0B5394", "width": GRAPH_LINE_WIDTH},
    "ZEC": {"color": "#444444", "width": GRAPH_LINE_WIDTH},
    "ADA": {"color": "#674EA7", "width": GRAPH_LINE_WIDTH},
    "XLM": {"color": "#660000", "width": GRAPH_LINE_WIDTH},
    "XMR": {"color": "#0000FF", "width": GRAPH_LINE_WIDTH},
    "BSV": {"color": "#FF9900", "width": GRAPH_LINE_WIDTH},
    "Volatility w BTC": {"color": "#FF9900", "width": GRAPH_LINE_WIDTH},
    "Volatility w_o BTC": {"color": "#666666", "width": GRAPH_LINE_WIDTH},
    "Return w BTC": {"color": "#FF9900", "width": GRAPH_LINE_WIDTH},
    "Return w_o BTC": {"color": "#666666", "width": GRAPH_LINE_WIDTH},
}


FORMAT_DICT = {
    "white": {"bg_color": "#FFFFFF"},
    "light_grey": {"bg_color": "#F3F3F3", "num_format": "0.00%"},
    "lighter_blue": {"bg_color": "#CFE2F3", "num_format": "0.00%"},
    "light_blue": {"bg_color": "#9FC5E8", "num_format": "0.00%"},
    "sky_blue": {"bg_color": "#6FA8DC", "num_format": "0.00%"},
    "blue": {"bg_color": "#3D85C6", "num_format": "0.00%"},
    "lighter_orange": {"bg_color": "#FFF2CC", "num_format": "0.00%"},
    "light_orange": {"bg_color": "#FFE599", "num_format": "0.00%"},
    "orange": {"bg_color": "#FFD966", "num_format": "0.00%"},
    "dark_orange": {"bg_color": "#F1C232", "num_format": "0.00%"},
    "crypto_orange": {
        "bg_color": "#FF9900",
        "font_color": "#FFFFFF",
        "align": "center",
        "valign": "vcenter",
        "bold": True,
        "border": 1,
    },
    "crypto_orange_v": {
        "bg_color": "#FF9900",
        "font_color": "#FFFFFF",
        "bold": True,
        "border": 1,
    },
    "commodity_green": {
        "bg_color": "#6AA84F",
        "font_color": "#FFFFFF",
        "align": "center",
        "valign": "vcenter",
        "bold": True,
        "border": 1,
    },
    "commodity_green_v": {
        "bg_color": "#6AA84F",
        "font_color": "#FFFFFF",
        "bold": True,
        "border": 1,
    },
    "equity_grey": {
        "bg_color": "#444444",
        "font_color": "#FFFFFF",
        "align": "center",
        "valign": "vcenter",
        "bold": True,
        "border": 1,
    },
    "equity_grey_v": {
        "bg_color": "#444444",
        "font_color": "#FFFFFF",
        "bold": True,
        "border": 1,
    },
    "bond_grey": {
        "bg_color": "#999999",
        "font_color": "#FFFFFF",
        "align": "center",
        "valign": "vcenter",
        "bold": True,
        "border": 1,
    },
    "bond_grey_v": {
        "bg_color": "#999999",
        "font_color": "#FFFFFF",
        "bold": True,
        "border": 1,
    },
    "currency_blue": {
        "bg_color": "#0000FF",
        "font_color": "#FFFFFF",
        "align": "center",
        "valign": "vcenter",
        "bold": True,
        "border": 1,
    },
    "currency_blue_v": {
        "bg_color": "#0000FF",
        "font_color": "#FFFFFF",
        "bold": True,
        "border": 1,
    },
}


# ------------------------------------------------------

Y_FINANCE_DICT = {
    "S&P500": "^GSPC",
    "DOWJONES": "^DJI",
    "BTC": "BTC-USD",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "COPPER": "HG=F",
    "NATURAL_GAS": "NG=F",
    "CRUDE OIL": "CL=F",
    "CORN": "ZC=F",
    "EUR": "EURUSD=X",
    "GBP": "GBPUSD=X",
    "JPY": "JPYUSD=X",
    "CHF": "CHFUSD=X",
    "EUROSTOXX50": "^STOXX50E",
    "VIX": "^VIX",
    "NASDAQ": "^IXIC",
    "TESLA": "TSLA",
    "AMAZON": "AMZN",   
    "APPLE": "AAPL",
    "NETFLIX": "NFLX",
    "NVIDIA": "NVDA",
    "US TREASURY": "ZB=F",
    "EUR Aggregate Bond": "EAGG.PA",
    "US Aggregate Bond": "SCHZ",
    "USD index": "DX-Y.NYB",
}


STATISTICS = [
    "Mean Return",
    "Annualized Mean Return",
    "Mimimum Return",
    "Maximum Return",
    "Standard Deviation",
    "Annalized St. Deviation",
    "Volatility",
    "Excess Kurtosis",
    "Skewness",
    "VaR at 99 % normal distribution",
    "CVar at 99 % normal distribution",
    "VaR at 99 % t distribution",
    "CVar at 99 % t distribution",
    "Worst Draw-down",
    "Days to Recovery from DD",
    "Worst Draw-down length",
    "Sharpe Ratio",
    # 'Correlation with Bitcoin'
]

# ---------------------------------------------------------
# YAHOO HISTORICAL SERIES DOWNLOAD FOR ANALYSIS

YAHOO_TO_DOWNLOAD_NAME = [
    "S&P500",
    "DOWJONES",
    "GOLD",
    "SILVER",
    "COPPER",
    "NATURAL_GAS",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "EUROSTOXX50",
    "VIX",
    "NASDAQ",
    "US TREASURY",
    "EUR Aggregate Bond",
    "US Aggregate Bond",
    "US index",
    "TESLA",
    "AMAZON",
    "APPLE",
    "NETFLIX",
    "NVIDIA",
]

YAHOO_TO_DOWNLOAD_CODE = [
    "^GSPC",
    "^DJI",
    "GC=F",
    "SI=F",
    "HG=F",
    "NG=F",
    "CL=F",
    "ZC=F",
    "EURUSD=X",
    "GBPUSD=X",
    "JPYUSD=X",
    "CHFUSD=X",
    "^STOXX50E",
    "^VIX",
    "^IXIC",
    "ZB=F",
    "EAGG.PA",
    "SCHZ",
    "DX-Y.NYB",
    "TSLA",
    "AMZN",
    "AAPL",
    "NFLX",
    "NVDA",
]

YAHOO_TO_DOWNLOAD_SERV = [
    "GBTC",
    "QBTC.TO",
    "DE000A28M8D0.SG",
    "ABBA.SW",
    "ABCH.SW",
    "CH0454664001.SG",
    "BTCW.SW",
    "DE000A27Z304.SG",
    "CH0445689208.SG",
]

YAHOO_NAME_SERV = [
    "GBTC",
    "The Bitcoin Fund",
    "VANECK",
    "21Shares Bitcoin Suisse",
    "21Shares Bitcoin Cash ETP",
    "21Shares Bitcoin (ABTC) ETP",
    "WisdomTree Bitcoin",
    "BTCetc Bitcoin Exchange Traded",
    "21Shares Crypto Basket Index ET",
]


# ##############

BEST_PERFORMING_LIST = ["BTC", "APPLE", "NETFLIX", "TESLA", "AMAZON", "NVIDIA"]


BEST_PERFORMING_LIST_VOL = ["BTC", "APPLE", "NETFLIX", "TESLA", "AMAZON", "NVIDIA"]

YAHOO_DASH_LIST = [
    "S&P500",
    "DOWJONES",
    "GOLD",
    "SILVER",
    "COPPER",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "EUROSTOXX50",
    "VIX",
    "NASDAQ",
    "US TREASURY",
    "EUR Aggregate Bond",
    "US Aggregate Bond",
    "US index",
]

YAHOO_DASH_LIST_W_BTC = [
    "BTC",
    "S&P500",
    "DOWJONES",
    "GOLD",
    "SILVER",
    "COPPER",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "EUROSTOXX50",
    "VIX",
    "NASDAQ",
    "US TREASURY",
    "EUR Aggregate Bond",
    "US Aggregate Bond",
    "US index",
]

STATIC_COLORSCALE = [
    [0.0, "rgb(49,54,149)"],
    [0.1111111111111111, "rgb(69,117,180)"],
    [0.2222222222222222, "rgb(116,173,209)"],
    [0.3333333333333333, "rgb(171,217,233)"],
    [0.4444444444444444, "rgb(224,243,248)"],
    [0.5555555555555556, "rgb(254,224,144)"],
    [0.6666666666666666, "rgb(253,174,97)"],
    [0.7777777777777778, "rgb(244,109,67)"],
    [0.8888888888888888, "rgb(215,48,39)"],
    [1.0, "rgb(165,0,38)"],
]

# ---------------------
# MARKET CAP VARIABLES
# ----------------------

TICKERS_FOR_MKT_CAP = [
    "AAPL",
    "GOOG",
    "2222.SR",
    "MSFT",
    "AMZN",
    "TSLA",
    "NFLX",
    "PYPL",
    "MA",
    "TCEHY",
    "V",
    "HKXCF",
    "COIN",
    "CME",
    "ICE",
    "LNSTY",
    "DBOEF",
    "NDAQ",
    "CBOE",
]

NAME_FOR_MKT_CAP = [
    "Apple",
    "Google",
    "Saudi Aramco",
    "Microsoft",
    "Amazon",
    "Tesla",
    "Netflix",
    "Paypal",
    "MasterCard",
    "Tencent",
    "Visa",
    "HK Exchanges",
    "Coinbase",
    "CME",
    "Int Exchange",
    "London Stock Exchange",
    "Deutsche Borse",
    "Nasdaq",
    "CBOE",
]

COMPLETE_MKT_CAP = [
    "Apple",
    "Google",
    "Saudi Aramco",
    "Microsoft",
    "Amazon",
    "Tesla",
    "Netflix",
    "Paypal",
    "MasterCard",
    "Tencent",
    "Visa",
    "USD",
    "Gold",
    "Silver",
    "BTC",
]

COMPARED_MKT_CAP = [
    "HK Exchanges",
    "CME",
    "Int Exchange",
    "Coinbase",
    "London Stock Exchange",
    "Deutsche Borse",
    "Nasdaq",
    "CBOE",
]

BEST_MKT_CAP = [
    "Apple",
    "Microsoft",
    "Amazon",
    "Google",
    "BTC",
    "Tesla",
    "Netflix",
]

USD_SUPPLY = 19632088542000

GOLD_OUNCES_SUPPLY = 2500000000

SILVER_OUNCES_SUPPLY = 4000000000


# --------------------------------
# MARKOVITZ
# ------------------------------

YAHOO_TO_CAPM = [
    "S&P500",
    "DOWJONES",
    "BTC",
    "GOLD",
    "CRUDE OIL",
    "EUROSTOXX50",
    "US TREASURY",
    "EUR",
    "GBP",
    "VIX",
    "EUR Aggregate Bond",
    "APPLE",
]


# -------------------
# STOCK2FLOW
# -------------------

HALVING_DATE = ["28-11-2012", "09-07-2016", "11-05-2020", "13-03-2024", "15-01-2028"]

MINING_REWARD = [50, 25, 12.5, 6.25, 3.125, 1.5625]

HALVING_BLOCK_HEIGHT = 210000

CORRECTION_FACTOR = 1.04

MKT_CAP_LOG_VAL = [
    1000,
    10000,
    100000,
    1000000,
    10000000,
    100000000,
    1000000000,
    10000000000,
    100000000000,
    1000000000000,
    10000000000000,
    100000000000000,
]

SILVER_STOCK_TONS = 900000
SIVER_FLOW_TONS = 27000

GOLD_STOCK_TONS = 190000
GOLD_FLOW_TONS = 3260

# -----------
# STATIC CORRELATION MATRIX COMPUTATION VARIABLES

CORR_MATRIX_LIST = [
    "BTC",
    "ETH",
    "XRP",
    "ADA",
    "DOGE",
    "MATIC",
    "AVAX",
    "GOLD",
    "COPPER",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "NASDAQ",
    "S&P500",
    "EUROSTOXX50",
    "VIX",
    "US TREASURY",
    "PAN EUR",
]

CORR_MATRIX_LIST_ASSET = [
    "BTC",
    "GOLD",
    "COPPER",
    "CRUDE OIL",
    "CORN",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "NASDAQ",
    "S&P500",
    "EUROSTOXX50",
    "VIX",
    "US TREASURY",
    "PAN EUR",
]

CORR_MATRIX_LIST_CRYPTO = [
    "BTC",
    "ETH",
    "XRP",
    "ADA",
    "DOGE",
    "MATIC",
    "AVAX",
]

# STABLECOIN

STABLECOIN_TICKER = ["USDT-USD", "USDC-USD"]

STABLECOIN_NAME = ["USDT", "USDC"]

#

BTC_FUT_TICKER = ["BTC=F", "BTM=F"]

BTC_FUT_NAME = ["CME Future", "Bakkt Future"]
