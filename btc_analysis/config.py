DB_NAME = "btc_analysis"

START_DATE = "2012-12-31"

INDEX_START_DATE = "2016-01-01"

INDEX_DB_NAME = "index"

REF_CRYPTO = "BTC"

REF_VARIOUS = "BITCOIN"

REF_SP500 = "S&P500"

TIME_WINDOW = ['All', '3Y', '1Y', '1Q', '1M']

ASSET_CATEGORY = ['Crypto-currency', 'Commodity',
                  'Currency', 'Equity', 'Volatility', 'Bond']

CRYPTO_LIST = ['BTC', 'ETH', 'XRP', 'LTC',
               'BCH', 'EOS', 'ETC', 'ZEC',
               'ADA', 'XLM', 'XMR', 'BSV']

METAL_LIST = ["Gold", "Silver", "Copper"]

CRYPTO_STATIC_LIST = ['BTC', 'ETH', 'XRP', 'LTC',
                      'BCH', 'EOS', 'ETC', 'ZEC',
                      'ADA', 'XLM', 'XMR', 'BSV']

VARIOUS_LIST = ["BITCOIN", "ETH", "LTC", "XRP", "GOLD", "IND_METALS", "WTI",
                "GRAIN", "EUR", "CHF", "GBP", "JPY",
                "NASDAQ", "EUROSTOXX50", "S&P500",
                "MSCI BRIC ", "VIX Index",
                "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
                "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

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
                  'US Aggregate Bond']

EQUITY = ["NASDAQ", "EUROSTOXX50", "S&P500",
          "MSCI BRIC ", "VIX Index"]

EQUITY_YAHOO = ['NASDAQ',
                'DOWJONES',
                'S&P500',
                'EUROSTOXX50',
                'VIX']

BOND = ["Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
        "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

BOND_YAHOO = ['US_TREASURY',
              'BBG Barclays PAN EURO Aggregate',
              'US Aggregate Bond']

CURRENCY = ["EUR", "CHF", "GBP", "JPY"]

COMMODITY = ["GOLD", "IND_METALS", "WTI",
             "GRAIN"]

COMMODITY_YAHOO = ['GOLD',
                   'COPPER',
                   'NATURAL_GAS',
                   'PETROL',
                   'CORN', ]

CRYPTO_FOR_STATIC = ["BITCOIN", "ETH",
                     "LTC", "XRP"]

CRYPTO_FOR_STATIC_YAHOO = ["BTC", "ETH",
                           "LTC", "XRP"]

CRYPTO = ["BITCOIN", "BTC", "ETH",
          "LTC", "XRP", 'BCH',
          'EOS', 'ETC', 'ZEC',
          'ADA', 'XLM', 'XMR', 'BSV']

VS_SP500_LIST = ["BITCOIN", "GOLD", "IND_METALS", "WTI",
                 "GRAIN", "EUR", "CHF", "GBP", "JPY",
                 "NASDAQ", "EUROSTOXX50",
                 "MSCI BRIC ", "VIX Index",
                 "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
                 "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

SP500_GRAPH_LIST = ["BITCOIN", "GOLD", "GRAIN", "EUR", "JPY",
                    "EUROSTOXX50", "VIX Index",
                    "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

VAR_GRAPH_LIST = ['ETH', 'XRP', 'LTC', "GOLD", "GRAIN", "EUR", "JPY",
                  "EUROSTOXX50", "S&P500", "VIX Index", "NASDAQ", "PETROL"
                  "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate",
                  "CORN", 'US_TREASURY', 'BBG Barclays PAN EURO Aggregate']


CRYPTO_GRAPH_LIST = ['ETH', 'XRP', 'LTC',
                     'BCH', 'EOS', 'ETC', 'ZEC',
                     'ADA', 'XLM', 'XMR', 'BSV']

METAL_GRAPH_LIST = ["Gold", "Silver", "Copper"]

VAR_STATIC_LIST = ["Date", "BITCOIN", "ETH", "LTC", "XRP",
                   "GOLD", "IND_METALS", "WTI",
                   "GRAIN", "EUR", "CHF", "GBP", "JPY",
                   "NASDAQ", "EUROSTOXX50", "S&P500",
                   "MSCI BRIC ", "VIX Index",
                   "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
                   "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

VAR_STATIC_LIST_Y = ["Date",
                     "BTC",
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
                     'US Aggregate Bond']

GRAPH_LINE_WIDTH = 2

GRAPH_COLOR = {

    # commodity color
    "GRAIN":  {'color': '#01A801',
               'width': GRAPH_LINE_WIDTH,
               },
    "CORN":  {'color': '#01A801',
              'width': GRAPH_LINE_WIDTH,
              },
    "PETROL":  {'color': '#CCCCCC',
                'width': GRAPH_LINE_WIDTH,
                },
    "NATURAL_GAS":  {'color': '#01A801',
                     'width': GRAPH_LINE_WIDTH,
                     },

    # metal colors
    'Gold': {'color': '#00FF00',
             'width': GRAPH_LINE_WIDTH},
    "GOLD": {'color': '#00FF00',
             'width': GRAPH_LINE_WIDTH},
    'Silver': {'color': '#CCCCCC',
               'width': GRAPH_LINE_WIDTH},
    'SILVER': {'color': '#CCCCCC',
               'width': GRAPH_LINE_WIDTH},
    'Copper': {'color': '#B45F06',
               'width': GRAPH_LINE_WIDTH},
    'COPPER': {'color': '#B45F06',
               'width': GRAPH_LINE_WIDTH},

    # currency color
    "EUR":  {'color': '#0000FF',
             'width': GRAPH_LINE_WIDTH},
    "JPY": {'color': '#0404B2',
            'width': GRAPH_LINE_WIDTH,
            },
    "GBP": {'color': '#3D85C6',
            'width': GRAPH_LINE_WIDTH,
            },
    "CHF": {'color': '#CC0000',
            'width': GRAPH_LINE_WIDTH,
            },

    # index color
    "EUROSTOXX50":  {'color': '#444444',
                     'width': GRAPH_LINE_WIDTH,
                     },
    "S&P500": {'color': '#666666',
               'width': GRAPH_LINE_WIDTH
               },
    "VIX Index": {'color': '#6E6D6D',
                  'width': GRAPH_LINE_WIDTH,
                  },
    "VIX": {'color': '#6E6D6D',
            'width': GRAPH_LINE_WIDTH,
            },

    # treasury and bond color
    "BBG Barclays PAN EURO Aggregate": {'color': '#999999',
                                        'width': GRAPH_LINE_WIDTH,
                                        # 'dash_type': 'long_dash'
                                        },
    "BBG Barclays PAN US Aggregate": {'color': '#CCCCCC',
                                      'width': GRAPH_LINE_WIDTH,
                                      },
    "US_TREASURY": {'color': '#999999',
                    'width': GRAPH_LINE_WIDTH,
                    # 'dash_type': 'long_dash'
                    },
    "BBG Barclays PAN EURO Aggregate": {'color': '#CCCCCC',
                                        'width': GRAPH_LINE_WIDTH,
                                        },
    # crytpo color
    "BITCOIN": {'color': '#FF9900',
                'width': GRAPH_LINE_WIDTH},
    "BTC": {'color': '#FF9900',
            'width': GRAPH_LINE_WIDTH},
    'ETH':  {'color': '#0000FF',
             'width': GRAPH_LINE_WIDTH},
    'XRP':  {'color': '#CC0000',
             'width': GRAPH_LINE_WIDTH},
    'LTC':  {'color': '#CCCCCC',
             'width': GRAPH_LINE_WIDTH},
    'BCH':  {'color': '#01A801',
             'width': GRAPH_LINE_WIDTH},
    'EOS':  {'color': '#FFFF00',
             'width': GRAPH_LINE_WIDTH},
    'ETC':  {'color': '#0B5394',
             'width': GRAPH_LINE_WIDTH},
    'ZEC':  {'color': '#444444',
             'width': GRAPH_LINE_WIDTH},
    'ADA':  {'color': '#674EA7',
             'width': GRAPH_LINE_WIDTH},
    'XLM':  {'color': '#660000',
             'width': GRAPH_LINE_WIDTH},
    'XMR': {'color': '#0000FF',
            'width': GRAPH_LINE_WIDTH},
    'BSV':  {'color': '#FF9900',
             'width': GRAPH_LINE_WIDTH},



    'Volatility w BTC': {'color': '#FF9900',
                         'width': GRAPH_LINE_WIDTH},
    'Volatility w_o BTC': {'color': '#666666',
                           'width': GRAPH_LINE_WIDTH},
    'Return w BTC': {'color': '#FF9900',
                     'width': GRAPH_LINE_WIDTH},
    'Return w_o BTC': {'color': '#666666',
                       'width': GRAPH_LINE_WIDTH},


}


FORMAT_DICT = {

    'white': {'bg_color': '#FFFFFF'},
    'light_grey': {'bg_color': '#F3F3F3',
                   'num_format': '0.00%'},
    'lighter_blue': {'bg_color': '#CFE2F3',
                     'num_format': '0.00%'},
    'light_blue': {'bg_color': '#9FC5E8',
                   'num_format': '0.00%'},
    'sky_blue': {'bg_color': '#6FA8DC',
                 'num_format': '0.00%'},
    'blue': {'bg_color': '#3D85C6',
             'num_format': '0.00%'},
    'lighter_orange': {'bg_color': '#FFF2CC',
                       'num_format': '0.00%'},
    'light_orange': {'bg_color': '#FFE599',
                     'num_format': '0.00%'},
    'orange': {'bg_color': '#FFD966',
               'num_format': '0.00%'},
    'dark_orange': {'bg_color': '#F1C232',
                    'num_format': '0.00%'},

    'crypto_orange': {'bg_color': '#FF9900',
                      'font_color': '#FFFFFF',
                      'align': 'center',
                      'valign': 'vcenter',
                      'bold': True,
                      'border': 1},

    'crypto_orange_v': {'bg_color': '#FF9900',
                        'font_color': '#FFFFFF',
                        'bold': True,
                        'border': 1},

    'commodity_green': {'bg_color': '#6AA84F',
                        'font_color': '#FFFFFF',
                        'align': 'center',
                        'valign': 'vcenter',
                        'bold': True,
                        'border': 1},

    'commodity_green_v': {'bg_color': '#6AA84F',
                          'font_color': '#FFFFFF',
                          'bold': True,
                          'border': 1},

    'equity_grey': {'bg_color': '#444444',
                    'font_color': '#FFFFFF',
                    'align': 'center',
                    'valign': 'vcenter',
                    'bold': True,
                    'border': 1},

    'equity_grey_v': {'bg_color': '#444444',
                      'font_color': '#FFFFFF',
                      'bold': True,
                      'border': 1},

    'bond_grey': {'bg_color': '#999999',
                  'font_color': '#FFFFFF',
                  'align': 'center',
                  'valign': 'vcenter',
                  'bold': True,
                  'border': 1},

    'bond_grey_v': {'bg_color': '#999999',
                    'font_color': '#FFFFFF',
                    'bold': True,
                    'border': 1},

    'currency_blue': {'bg_color': '#0000FF',
                      'font_color': '#FFFFFF',
                      'align': 'center',
                      'valign': 'vcenter',
                      'bold': True,
                      'border': 1},

    'currency_blue_v': {'bg_color': '#0000FF',
                        'font_color': '#FFFFFF',
                        'bold': True,
                        'border': 1}
}


Y_FINANCE_DICT = {

    'S&P500': '^GSPC',
    'DOWJONES': '^DJI',
    'BTC': 'BTC-USD',
    'GOLD': 'GC=F',
    'SILVER': 'SI=F',
    'COPPER': 'HG=F',
    'NATURAL_GAS': 'NG=F',
    'PETROL': "CL=F",
    'CORN': "ZC=F",
    'EUR': 'EURUSD=X',
    'GBP': 'GBPUSD=X',
    'JPY': 'JPYUSD=X',
    'CHF': 'CHFUSD=X',
    'EUROSTOXX50': '^STOXX50E',
    'VIX': '^VIX',
    'NASDAQ': '^IXIC',
    'TESLA': 'TSLA',
    'AMAZON': 'AMZN',
    'APPLE': 'AAPL',
    'NETFLIX': 'NFLX',
    'US_TREASURY': 'ZB=F',
    'BBG Barclays PAN EURO Aggregate': 'EAGG.PA',
    'US Aggregate Bond': 'SCHZ',
    'USD index': 'DX-Y.NYB'

}


STATISTICS = ['Mean Return',
              'Annualized Mean Return',
              'Mimimum Return',
              'Maximum Return',
              'Standard Deviation',
              'Annalized St. Deviation',
              'Volatility',
              'Excess Kurtosis',
              'Skewness',
              'VaR at 99 % normal distribution',
              'CVar at 99 % normal distribution',
              'VaR at 99 % t distribution',
              'CVar at 99 % t distribution',
              'Worst Draw-down',
              'Days to Recovery from DD',
              'Worst Draw-down length',
              'Sharpe Ratio',
              # 'Correlation with Bitcoin'
              ]

# ---------------------------------------------------------
# YAHOO HISTORICAL SERIRES DOWNLOAD FOR ANALYSIS

YAHOO_TO_DOWNLOAD_NAME = ['S&P500',
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
                          'AMAZON',
                          'APPLE',
                          'NETFLIX']

YAHOO_TO_DOWNLOAD_CODE = ['^GSPC',
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
                          'AMZN',
                          'AAPL',
                          'NFLX']


YAHOO_TO_RETURN = ["BTC",
                   "ETH",
                   "LTC",
                   "XRP",
                   'S&P500',
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
                   'AMAZON',
                   'APPLE',
                   'NETFLIX'
                   ]


# ##############

ASSET_ANALYSIS_LIST = ["BTC",
                       "APPLE",
                       "NETFLIX",
                       "TESLA",
                       "AMAZON"]

YAHOO_DASH_LIST = ['S&P500',
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
                   'EUR Aggregate Bond',
                   'US Aggregate Bond',
                   'US index',
                   'TESLA',
                   'AMAZON',
                   'APPLE',
                   'NETFLIX']

# STATIC_COLORSCALE = [[-1.0, '#0066ff'],  # cmap = sns.diverging_palette(220, 10, as_cmap = True)
#                      [-0.75, '#3385ff'],
#                      [-0.5, '#80b3ff'],
#                      [-0.25, '#cce0ff'],
#                      [0.0, '#ffffff'],
#                      # [0.05, '#fffae6'],
#                      [0.25, '#fff5cc'],
#                      [0.5, '#ffeb99'],
#                      [0.75, '#ffdb4d'],
#                      [1.0, '#ffcc00']]


STATIC_COLORSCALE = [[0.0, "rgb(49,54,149)"],
                     [0.1111111111111111, "rgb(69,117,180)"],
                     [0.2222222222222222, "rgb(116,173,209)"],
                     [0.3333333333333333, "rgb(171,217,233)"],
                     [0.4444444444444444, "rgb(224,243,248)"],
                     [0.5555555555555556, "rgb(254,224,144)"],
                     [0.6666666666666666, "rgb(253,174,97)"],
                     [0.7777777777777778, "rgb(244,109,67)"],
                     [0.8888888888888888, "rgb(215,48,39)"],
                     [1.0, "rgb(165,0,38)"]]
