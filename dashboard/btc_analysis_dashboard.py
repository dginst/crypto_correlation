import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from btc_analysis.config import (ASSET_ANALYSIS_LIST, ASSET_ANALYSIS_LIST_VOL,
                                 COMPLETE_MKT_CAP, CRYPTO_LIST, DB_NAME,
                                 YAHOO_DASH_LIST)
from btc_analysis.dashboard_func import (btc_total_dfs, usd_den_total_df,
                                         vola_total_df)
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output

# ------------------------------
# start app


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# -------------------
# Data

window_list = ["5Y", "3Y", "2Y", "1Y", "6M", "3M", "1M", "YTD"]
vola_days_list = ["252", "90", "30"]


# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("BTC analysis Dashboard",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),


    dbc.Row([
        dbc.Col([

            html.Label(['Time Window']),

            dcc.Dropdown(
                id='my_alt_dropdown',
                options=[
                    {'label': w, 'value': w} for w in window_list
                ],
                multi=False,
                value="3Y",
                style={"width": "50%"},
                clearable=False
            ),

            html.Label(['Crypto Assets']),
            dcc.Checklist(
                id='my_alt_check',
                options=[
                    {'label': x, 'value': x} for x in CRYPTO_LIST
                ],
                value=["BTC", "ETH", "XRP", "LTC", "BCH"],
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-right": "10px",
                            "margin-left": "10px"}
            ),


            dcc.Graph(id='my_multi_line', figure={}),

            html.A(
                'Download Data',
                id='download-link_alt',
                download="altcoin_rawdata.csv",
                href="",
                target="_blank"
            )
        ])

    ]),

    dbc.Row([
        dbc.Col([


            html.Label(['Time Window']),

            dcc.Dropdown(
                id='my_yahoo_dropdown',
                options=[
                    {'label': w, 'value': w} for w in window_list
                ],
                multi=False,
                value="3Y",
                style={"width": "50%"},
                clearable=False
            ),

            html.Label(['Assets']),

            dcc.Checklist(
                id='my_yahoo_check',
                options=[
                    {'label': x, 'value': x} for x in YAHOO_DASH_LIST
                ],
                value=["BTC", "GOLD", "AMAZON", "TESLA", "APPLE", "NETFLIX"],
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-right": "10px",
                            "margin-left": "10px"}
            ),


            dcc.Graph(id='my_multi_line_2', figure={}),

            html.A(
                'Download Data',
                id='download-link_yahoo',
                download="yahoo_rawdata.csv",
                href="",
                target="_blank"
            )
        ])

    ]),

    dbc.Row([
            dbc.Col([

                html.Label(['Time Window']),

                dcc.Dropdown(
                    id='my_norm_dropdown',
                    options=[
                        {'label': w, 'value': w} for w in window_list
                    ],
                    multi=False,
                    value="3Y",
                    style={"width": "50%"},
                    clearable=False
                ),

                html.Label(['Assets']),

                dcc.Checklist(
                    id='my_yahoo_norm',
                    options=[
                        {'label': x, 'value': x} for x in ASSET_ANALYSIS_LIST
                    ],
                    value=["BTC", "AMAZON",
                           "TESLA", "APPLE", "NETFLIX"],
                    labelStyle={'display': 'inline-block'},
                    inputStyle={"margin-right": "10px",
                                "margin-left": "10px"}
                ),

                dcc.Graph(id='my_multi_line_3', figure={}),

                html.A(
                    'Download Data',
                    id='download-link_yahoo_norm',
                    download="yahoo_normalized.csv",
                    href='',
                    target="_blank"
                )
            ])

            ]),

    dbc.Row([
        dbc.Col([

            html.Label(['Days']),

            dcc.Dropdown(
                id='my_vola_dropdown',
                options=[
                    {'label': w, 'value': w} for w in vola_days_list
                ],
                multi=False,
                value="252",
                style={"width": "50%"},
                clearable=False
            ),

            html.Label(['Assets']),

            dcc.Checklist(
                id='my_yahoo_vola',
                options=[
                    {'label': x, 'value': x} for x in ASSET_ANALYSIS_LIST
                ],
                value=["BTC", "AMAZON",
                       "TESLA", "APPLE", "NETFLIX"],
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-right": "10px",
                            "margin-left": "10px"}
            ),

            dcc.Graph(id='my_multi_line_4', figure={}),

            html.A(
                'Download Data',
                id='download-link_yahoo_vola',
                download="yahoo_vola.csv",
                href='',
                target="_blank"
            )
        ])

    ]),

    dbc.Row([
        dbc.Col([

            html.Label(['Yahoo Price Data: ']),

            html.A(
                'Download Data',
                id='download-link_yahoo_price',
                download="yahoo_price.csv",
                href='',
                target="_blank"
            )
        ])

    ]),

    dbc.Row([
            dbc.Col([


                html.Label(['Assets']),

                dcc.Checklist(
                    id='my_yahoo_volume',
                    options=[
                        {'label': x, 'value': x} for x in ASSET_ANALYSIS_LIST_VOL
                    ],
                    value=["BTC", "BTC no stable", "AMAZON",
                           "TESLA", "APPLE", "NETFLIX"],
                    labelStyle={'display': 'inline-block'},
                    inputStyle={"margin-right": "10px",
                                "margin-left": "10px"}
                ),

                dcc.Graph(id='my_multi_line_5', figure={}),

                html.A(
                    'Download Data',
                    id='download-link_yahoo_volume',
                    download="yahoo_volume.csv",
                    href='',
                    target="_blank"
                )
            ])

            ]),

    # dbc.Row([
    #     dbc.Col([


    #         dcc.Graph(id='my_bar_graph', figure={}),

    #     ])

    # ]),

    dcc.Interval(id='update', n_intervals=0, interval=1000 * 5),

    dcc.Interval(id='yahoo-update', interval=100000, n_intervals=0)
])

# --------------------------
# Callbacks part


# btc denominated altcoin callback

# dropdown can be unified putting the same ID into the Input of each callback,
# NB: the dropdpwn display should be, at that point, disabled except for the
# first one
# naming has to be commented in the layout part for the second and third graph

@app.callback(
    Output(component_id='download-link_yahoo_price', component_property='href'),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def update_price_yahoo(n):

    df_yahoo_price = query_mongo(DB_NAME, "all_prices_y")
    dff_yahoo_price = df_yahoo_price.copy()

    csv_string_yahoo_price = dff_yahoo_price.to_csv(
        index=False, encoding='utf-8')
    csv_string_yahoo_price = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_yahoo_price)

    return csv_string_yahoo_price


@ app.callback(
    [Output(component_id="my_multi_line", component_property="figure"),
     Output(component_id='download-link_alt', component_property='href')],
    [Input(component_id="my_alt_dropdown", component_property="value"),
     Input(component_id="my_alt_check", component_property="value")
     ]
)
def update_graph_alt(window_selection, asset_selection):

    df_alt, _ = btc_total_dfs(window_list, "btc_denominated")

    dff_alt = df_alt.copy()
    dff_alt_w = dff_alt.loc[dff_alt.Window == window_selection]
    dff_alt_w = dff_alt_w.drop(columns=["Window"])
    dff_date_alt = dff_alt_w["Date"]
    dff_alt_filtered = dff_alt_w[asset_selection]
    dff_alt_filtered["Date"] = dff_date_alt

    fig_alt = px.line(
        data_frame=dff_alt_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Altcoin performances BTC denominated',
        color_discrete_map={
            "BTC": "#FEAF16",
            "ETH": "#511CFB",
            "XRP": "#F6222E",
            "LTC": "#E2E2E2",
            "BCH": "#86CE00",
            "EOS": "#FBE426",
            "ETC": "#DA16FF",
            "ZEC": "#B68100",
            "ADA": "#00B5F7",
            "XLM": "#750D86",
            "XMR": "#A777F1",
            "BSV": "#F58518"
        }
    )

    csv_string_alt = dff_alt_w.to_csv(index=False, encoding='utf-8')
    csv_string_alt = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_alt)

    return fig_alt, csv_string_alt


# @app.callback(
#     Output(component_id='download-link_alt', component_property='href'),
#     Input(component_id='my_alt_dropdown', component_property='value')
# )
# def update_download_link_alt(window_selection):

#     dff_alt_d = df_alt.copy()
#     dff_w = dff_alt_d.loc[dff_alt_d.Window == window_selection]

#     csv_string = dff_w.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + \
#         urllib.parse.quote(csv_string)

#     return csv_string

# various asset btc den


@ app.callback(
    [Output(component_id="my_multi_line_2", component_property="figure"),
     Output(component_id='download-link_yahoo', component_property='href')],
    [Input(component_id="my_yahoo_dropdown", component_property="value"),
     Input(component_id="my_yahoo_check", component_property="value")]
)
def update_graph_yahoo(window_selection, asset_selection):

    _, df_yahoo = btc_total_dfs(window_list, "btc_denominated")

    df_yahoo = df_yahoo.drop(columns=["ETH", "XRP", "LTC", "BCH"])
    df_yahoo = df_yahoo.rename(
        columns={'BBG Barclays PAN EURO Aggregate': 'EUR Aggregate Bond',
                 'PETROL': 'CRUDE OIL'})

    dff_yahoo = df_yahoo.copy()
    dff_y_w = dff_yahoo.loc[dff_yahoo.Window == window_selection]
    dff_y_w = dff_y_w.drop(columns=["Window"])
    dff_date_y = dff_y_w["Date"]
    dff_y_filtered = dff_y_w[asset_selection]
    dff_y_filtered["Date"] = dff_date_y

    fig_yahoo = px.line(
        data_frame=dff_y_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Asset Class performances BTC denominated',
        color_discrete_map={
            "BTC": "#FEAF16",
            "S&P500": "#511CFB",
            "CRUDE OIL": "#222A2A",
            "SILVER": "#E2E2E2",
            "TESLA": "#86CE00",
            "US index": "#FBE426",
            "CORN": "#DA16FF",
            "NASDAQ": "#B68100",
            "VIX": "#00B5F7",
            "DOWJONES": "#750D86",
            "US_TREASURY": "#A777F1",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    csv_string_yahoo = dff_y_w.to_csv(index=False, encoding='utf-8')
    csv_string_yahoo = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_yahoo)

    return fig_yahoo, csv_string_yahoo


# @app.callback(
#     Output(component_id='download-link_yahoo', component_property='href'),
#     Input(component_id='my_yahoo_dropdown', component_property='value')
# )
# def update_download_link_yahoo(window_selection):

#     dff_y_d = df_yahoo.copy()
#     dff_w = dff_y_d.loc[dff_y_d.Window == window_selection]

#     csv_string = dff_w.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + \
#         urllib.parse.quote(csv_string)

#     return csv_string

# ------------
# normalized prices


@ app.callback(
    [Output(component_id="my_multi_line_3", component_property="figure"),
     Output(component_id='download-link_yahoo_norm', component_property='href')],
    [Input(component_id="my_norm_dropdown", component_property="value"),
     Input(component_id="my_yahoo_norm", component_property="value")]
)
def update_graph_norm(window_selection, asset_selection):

    df_usd_norm = usd_den_total_df(window_list)

    dff_norm = df_usd_norm.copy()
    dff_norm_w = dff_norm.loc[dff_norm.Window == window_selection]
    dff_norm_w = dff_norm_w.drop(columns=["Window"])

    dff_date_n = dff_norm_w["Date"]

    dff_filtered_norm = dff_norm_w[asset_selection]
    dff_filtered_norm["Date"] = dff_date_n

    fig_yahoo_norm = px.line(
        data_frame=dff_filtered_norm,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Performances denominated in USD',
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    csv_string_norm = dff_norm_w.to_csv(index=False, encoding='utf-8')
    csv_string_norm = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_norm)

    return fig_yahoo_norm, csv_string_norm


@ app.callback(
    [Output(component_id="my_multi_line_4", component_property="figure"),
     Output(component_id='download-link_yahoo_vola', component_property='href')],
    [Input(component_id="my_vola_dropdown", component_property="value"),
     Input(component_id="my_yahoo_vola", component_property="value")]
)
def update_graph_vola(days_selection, asset_selection):

    df_vola = vola_total_df(vola_days_list)

    dff_vola = df_vola.copy()

    dff_days = dff_vola.loc[dff_vola.Days == days_selection]
    dff_days = dff_days.drop(columns=["Days"])

    dff_v_date = dff_days["Date"]

    dff_vola_filtered = dff_days[asset_selection]
    dff_vola_filtered["Date"] = dff_v_date

    fig_yahoo_vola = px.line(
        data_frame=dff_vola_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Annualized Volatility',
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    csv_string_vola = dff_days.to_csv(index=False, encoding='utf-8')
    csv_string_vola = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_vola)

    return fig_yahoo_vola, csv_string_vola


@ app.callback(
    [Output(component_id="my_multi_line_5", component_property="figure"),
     Output(component_id='download-link_yahoo_volume', component_property='href')],
    Input(component_id="my_yahoo_volume", component_property="value")
)
def update_graph_volume(asset_selection):

    df_volume = query_mongo(DB_NAME, "all_volume_y")

    dff_volume = df_volume.copy()
    dff_vol_date = dff_volume["Date"]

    dff_vol_filtered = dff_volume[asset_selection]
    dff_vol_filtered["Date"] = dff_vol_date

    fig_yahoo_volume = px.line(
        data_frame=dff_vol_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Volume in USD',
        color_discrete_map={
            "BTC": "#FEAF16",
            "BTC no stable": "#8e16fe",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    csv_string_volume = dff_vol_filtered.to_csv(index=False, encoding='utf-8')
    csv_string_volume = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_volume)

    return fig_yahoo_volume, csv_string_volume


# @ app.callback(
#     Output(component_id="my_bar_graph", component_property="figure"),
#     Input(component_id="yahoo-update", component_property="n_intervals")
# )
# def update_graph_bar(n):

#     df_mkt_cap = query_mongo(DB_NAME, "market_cap")

#     dff_mkt_cap = df_mkt_cap.copy()

#     mkt_cap_df = pd.DataFrame(columns=["Name", "Market Cap"])
#     mkt_cap_df["Name"] = np.array(COMPLETE_MKT_CAP)
#     print(mkt_cap_df)
#     mkt_cap_df["Market Cap"] = np.array(dff_mkt_cap).T
#     print(mkt_cap_df)

#     fig_mkt_cap = px.bar(
#         data_frame=mkt_cap_df,
#         x="Name",
#         y="Market Cap",
#         template='plotly_dark',
#         title='Market Capitalization',
#         color_discrete_map={
#             "BTC": "#FEAF16",
#             "BTC no stable": "#8e16fe",
#             "TESLA": "#86CE00",
#             "AMAZON": "#F58518",
#             "APPLE": "#BAB0AC",
#             "NETFLIX": "#FD3216",
#         }
#     )

#     return fig_mkt_cap


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=4000, host='0.0.0.0')
