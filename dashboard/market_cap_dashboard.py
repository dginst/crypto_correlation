import urllib.parse
from datetime import date, datetime
import numpy as np

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.calc import last_quarter_end, window_period_back
from btc_analysis.config import (BEST_PERFORMING_LIST,
                                 BEST_PERFORMING_LIST_VOL, COMPARED_MKT_CAP,
                                 COMPLETE_MKT_CAP, CRYPTO_LIST, DB_NAME,
                                 YAHOO_DASH_LIST, YAHOO_DASH_LIST_W_BTC)
from btc_analysis.dashboard_func import (btc_total_dfs, date_elements,
                                         usd_den_total_df, vola_total_df)
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
# Data

# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Market Capitalization",
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

                                        # dcc.Checklist(
                                        #     id='mkt_cap_check',
                                        #     options=[
                                        #         {'label': x, 'value': x} for x in COMPARED_MKT_CAP
                                        #     ],
                                        #     value=COMPARED_MKT_CAP,
                                        #     labelStyle={
                                        #         'display': 'inline-block'},
                                        #     inputStyle={"margin-right": "10px",
                                        #                 "margin-left": "10px"}
                                        # ),

                                        dcc.Graph(
                                            id='mkt_cap_graph', figure={}),

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


@ app.callback(
    Output(component_id="mkt_cap_graph", component_property="figure"),
    #Input(component_id="mkt_cap_check", component_property="value"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def update_graph_bar(n):

    df_mkt_cap = query_mongo(DB_NAME, "market_cap")
    dff_mkt_cap = df_mkt_cap.copy()

    mkt_cap_df = pd.DataFrame(columns=["Name", "Market Cap"])
    mkt_cap_df["Name"] = np.array(COMPARED_MKT_CAP)
    print(mkt_cap_df)
    mkt_cap_df["Market Cap"] = np.array(dff_mkt_cap).T
    print(mkt_cap_df)

    fig_mkt_cap = px.bar(
        data_frame=mkt_cap_df,
        x="Name",
        y="Market Cap",
        template='plotly_dark',
        title='Market Capitalization',
        color_discrete_map={
            "BTC": "#FEAF16",
        }
    )

    return fig_mkt_cap


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8500, host='0.0.0.0')
