DB_NAME = "btc_analysis"

REF_CRYPTO = "BTC"

REF_VARIOUS = "BITCOIN"

REF_SP500 = "S&P500"

TIME_WINDOW = ['All', '3Y', '1Y', '1Q', '1M']

ASSET_CATEGORY = ['Crypto-currency', 'Commodity',
                  'Currency', 'Equity', 'Volatility', 'Bond']

CRYPTO_LIST = ['ETH', 'XRP', 'LTC',
               'BCH', 'EOS', 'ETC', 'ZEC',
               'ADA', 'XLM', 'XMR', 'BSV']

METAL_LIST = ["Gold", "Silver", "Copper"]

CRYPTO_STATIC_LIST = ['BTC', 'ETH', 'XRP', 'LTC',
                      'BCH', 'EOS', 'ETC', 'ZEC',
                      'ADA', 'XLM', 'XMR', 'BSV']

VARIOUS_LIST = ["GOLD", "IND_METALS", "WTI",
                "GRAIN", "EUR", "CHF", "GBP", "JPY",
                "NASDAQ", "EUROSTOXX50", "S&P500",
                "MSCI BRIC ", "VIX Index",
                "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
                "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

EQUITY = ["NASDAQ", "EUROSTOXX50", "S&P500",
          "MSCI BRIC ", "VIX Index"]

BOND = ["Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
        "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

CURRENCY = ["EUR", "CHF", "GBP", "JPY"]

COMMODITY = ["GOLD", "IND_METALS", "WTI",
             "GRAIN"]

CRYPTO_FOR_STATIC = ["BITCOIN", "ETH",
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

VAR_GRAPH_LIST = ["GOLD", "GRAIN", "EUR", "JPY",
                  "EUROSTOXX50", "S&P500", "VIX Index",
                  "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

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

GRAPH_LINE_WIDTH = 2

GRAPH_COLOR = {

    "BITCOIN": {'color': '#FF9900',
                'width': GRAPH_LINE_WIDTH},

    "GOLD": {'color': '#00FF00',
             'width': GRAPH_LINE_WIDTH},

    "GRAIN":  {'color': '#01A801',
               'width': GRAPH_LINE_WIDTH,
               # 'dash_type': 'long_dash'
               },
    "EUR":  {'color': '#0000FF',
             'width': GRAPH_LINE_WIDTH},
    "JPY": {'color': '#0404B2',
            'width': GRAPH_LINE_WIDTH,
            # 'dash_type': 'long_dash'
            },
    "EUROSTOXX50":  {'color': '#444444',
                     'width': GRAPH_LINE_WIDTH,
                     # 'dash_type': 'dash_dot'
                     },

    "S&P500": {'color': '#666666',
               'width': GRAPH_LINE_WIDTH
               },
    "VIX Index": {'color': '#6E6D6D',
                  'width': GRAPH_LINE_WIDTH,
                  # 'dash_type': 'long_dash'
                  },

    "BBG Barclays PAN EURO Aggregate": {'color': '#999999',
                                        'width': GRAPH_LINE_WIDTH,
                                        # 'dash_type': 'long_dash'
                                        },
    "BBG Barclays PAN US Aggregate": {'color': '#CCCCCC',
                                      'width': GRAPH_LINE_WIDTH,
                                      },

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

    'Gold': {'color': '#00FF00',
             'width': GRAPH_LINE_WIDTH},
    'Silver': {'color': '#CCCCCC',
               'width': GRAPH_LINE_WIDTH},
    'Copper': {'color': '#B45F06',
               'width': GRAPH_LINE_WIDTH}
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
    'GOLD': 'GC=F',
    'EUR': 'EURUSD=X',
    'GBP': 'GBPUSD=X',
    'JPY': 'JPYUSD=X',
    'CHF': 'CHFUSD=X',
    'EUROSTOXX50': '^STOXX50E',
    'VIX Index': '^VIX',
    'NASDAQ': '^IXIC',
    'BBG Barclays PAN EURO Aggregate': 'EAGG.PA',


}
