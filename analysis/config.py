DB_NAME = "btc_analysis"

REF_CRYPTO = "BTC"

REF_VARIOUS = "BITCOIN"

REF_SP500 = "S&P500"


CRYPTO_LIST = ['BTC', 'ETH', 'XRP', 'LTC',
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

CRYPTO = ["BITCOIN", "ETH", "LTC", "XRP"]

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

VAR_STATIC_LIST = ["Date", "BITCOIN", "ETH", "LTC", "XRP",
                   "GOLD", "IND_METALS", "WTI",
                   "GRAIN", "EUR", "CHF", "GBP", "JPY",
                   "NASDAQ", "EUROSTOXX50", "S&P500",
                   "MSCI BRIC ", "VIX Index",
                   "Bloomberg Barclays EuroAgg Total Return Index Value Unhedged EUR",
                   "BBG Barclays PAN EURO Aggregate", "BBG Barclays PAN US Aggregate"]

GRAPH_LINE_WIDTH = 1.5

GRAPH_COLOR = {

    "BITCOIN": {'color': '#FF9900'},

    "GOLD": {'color': 'green',
             'width': GRAPH_LINE_WIDTH},

    "GRAIN":  {'color': 'green',
               'width': GRAPH_LINE_WIDTH,
               'dash_type': 'long_dash'},
    "EUR":  {'color': 'blue',
             'width': GRAPH_LINE_WIDTH},
    "JPY": {'color': 'blue',
            'width': GRAPH_LINE_WIDTH,
            'dash_type': 'long_dash'},
    "EUROSTOXX50":  {'color': 'black',
                     'width': GRAPH_LINE_WIDTH,
                     'dash_type': 'dash_dot'},
    "S&P500": {'color': 'black',
               'width': GRAPH_LINE_WIDTH
               },
    "VIX Index": {'color': 'black',
                  'width': GRAPH_LINE_WIDTH,
                  'dash_type': 'long_dash'},

    "BBG Barclays PAN EURO Aggregate": {'color': 'gray',
                                        'width': GRAPH_LINE_WIDTH,
                                        'dash_type': 'long_dash'},
    "BBG Barclays PAN US Aggregate": {'color': 'gray',
                                      'width': GRAPH_LINE_WIDTH,
                                      }
}


FORMAT_DICT = {

    'light_grey': {'bg_color': '#F3F3F3'},
    'lighter_blue': {'bg_color': '#CFE2F3'},
    'light_blue': {'bg_color': '#9FC5E8'},
    'sky_blue': {'bg_color': '#6FA8DC'},
    'blue': {'bg_color': '#3D85C6'},
    'lighter_orange': {'bg_color': '#FFF2CC'},
    'light_orange': {'bg_color': '#FFE599'},
    'orange': {'bg_color': '#FFD966'},
    'dark_orange': {'bg_color': '#F1C232'},
    'crypto_orange': {'bg_color': '#FF9900',
                      'font_color': '#FFFFFF'},
    'commodity_green': {'bg_color': '#6AA84F',
                        'font_color': '#FFFFFF',
                        'bold': True,
                        'border': 1},
    'equity_grey': {'bg_color': '#444444',
                    'font_color': '#FFFFFF',
                    'bold': True,
                    'border': 1},
    'bond_grey': {'bg_color': '#999999',
                  'font_color': '#FFFFFF',
                  'bold': True,
                  'border': 1},

    'currency_blue': {'bg_color': '#0000FF',
                      'font_color': '#FFFFFF',
                      'bold': True,
                      'border': 1}
}
