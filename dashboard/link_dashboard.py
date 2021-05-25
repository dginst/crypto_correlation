import urllib.parse
from datetime import datetime, date

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.calc import last_quarter_end, window_period_back
from btc_analysis.config import (BEST_PERFORMING_LIST,
                                 BEST_PERFORMING_LIST_VOL, COMPLETE_MKT_CAP,
                                 CRYPTO_LIST, DB_NAME, YAHOO_DASH_LIST,
                                 YAHOO_DASH_LIST_W_BTC)
from btc_analysis.dashboard_func import (btc_total_dfs, usd_den_total_df,
                                         vola_total_df, date_elements)
from btc_analysis.market_data import yesterday_str
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# ------------------------------
# start app


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# -------------------

font_size = "25px"
# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Dashboard Links",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),


    # asset classes performance

    dbc.Row([
            dbc.Col([

                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.Row([
                                    dbc.Col([

                                        dcc.Location(id='url', refresh=False),

                                        dcc.Link(
                                            'Navigate to "Crypto-Index" dashboard', href='http://http://18.116.30.116:3000/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Bitcoin & Blockchain Statistics" dashboard', href='http://http://18.116.30.116:3500/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Crypto-Assets Analysis" dashboard', href='http://http://18.116.30.116:4000/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Asset Classes Analysis" dashboard', href='http://http://18.116.30.116:4500/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Best Performing Asset Analysis" dashboard', href='http://http://18.116.30.116:5000/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Capital Asset Pricing Model" dashboard', href='http://http://18.116.30.116:5500/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Stock to Flow" dashboard', href='http://http://18.116.30.116:7000/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Market Capitalization" dashboard', href='http://http://18.116.30.116:8500/', style={'font-size': font_size}),
                                        html.Br(),

                                        dcc.Link(
                                            'Navigate to "Static Correlation" dashboard', href='http://http://18.116.30.116:9000/', style={'font-size': font_size}),
                                        html.Br(),

                                    ])

                                ]),
                            ]),
                    ],
                    style={"width": "70rem"},
                    className="mt-3"
                )

            ]),

            ], justify='center'),



    dcc.Interval(id='update', n_intervals=0, interval=1000 * 5),

    dcc.Interval(id='yahoo-update', interval=100000, n_intervals=0)
])

# --------------------------
# Callbacks part

# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=10000, host='0.0.0.0')
