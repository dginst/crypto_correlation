import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output
from datetime import datetime


# start app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server


last_h_date = datetime.strptime("11-05-2020", "%d-%m-%Y")

# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Stock to Flow Model",
                        className='text-center text-primary, mb-4'),
                width=12)
    ]),

    dbc.Row([
        dbc.Col([

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([


                                        dcc.Graph(id="S2F_model", figure={},
                                                  config={'displayModeBar': False}),


                                    ])
                                ]),

                        ]),
                ],
                style={"width": "70rem"},
                className="mt-3"
            )

        ]),

    ], justify='center'),


    dbc.Row([
        dbc.Col([

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([


                                        dcc.Graph(id="S2F_performance", figure={},
                                                  config={'displayModeBar': True}),


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

    dcc.Interval(id='df-update', interval=100000, n_intervals=0)

])

# --------------------------
# Callbacks part


@app.callback(
    Output('S2F_model', 'figure'),
    Input('df-update', 'n_intervals')
)
def update_S2F(n):

    df = query_mongo("btc_analysis", "S2F_model")
    price_df = query_mongo("btc_analysis", "S2F_BTC_price")

    dff = df.copy()
    price_dff = price_df.copy()

    dff = dff.tail(len(dff.index) - 400)

    dff["Date"] = [datetime.strptime(
        x, "%d-%m-%Y") for x in dff["Date"]]

    model_price = go.Figure()

    model_price.add_trace(
        go.Scatter(
            x=dff["Date"],
            y=dff["S2F price 365d average"],
            name="S2F price 365d average",
            mode='lines',
            line_color='#FFFFFF',
        ))

    model_price.add_trace(
        go.Scatter(
            x=price_dff["Datetime"],
            y=price_dff["BTC Price"],
            name="BTC Price",
            mode='markers',
            marker=dict(color=price_dff["Days to Halving"],
                        # colorscale='Viridis',
                        colorscale='RdBu',
                        size=5,
                        colorbar=dict(thickness=20,
                                      # title='Days until next halving'
                                      ),
                        ),

        ))

    model_price.update_layout(
        title_text="Stock to Flow model",
        template='plotly_dark'
    )

    model_price.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    model_price.update_layout(
        annotations=[dict(
            # Don't specify y position, because yanchor="middle" should do it
            x=1.22,
            align="right",
            valign="top",
            text='Days until next halving',
            showarrow=False,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="middle",
            # Parameter textangle allow you to rotate annotation how you want
            textangle=-90
        )
        ]
    )

    model_price.update_yaxes(
        tickvals=[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000],
        tickprefix="$",
        title_text="BTC Price(USD)",
        type="log",
    )
    model_price.update_xaxes(nticks=20)
    # model_price.update_layout(xaxis=dict(tickformat="%Y"))

    return model_price


@app.callback(
    Output('S2F_performance', 'figure'),
    Input('df-update', 'n_intervals')
)
def update_S2F_perf(n):

    price_df = query_mongo("btc_analysis", "S2F_BTC_price")
    perf_df = query_mongo("btc_analysis", "S2F_halving_performance")

    perf_dff = perf_df.copy()
    price_dff = price_df.copy()

    price_dff = price_dff.loc[price_dff.Datetime >= last_h_date]

    performance = go.Figure()

    performance.add_trace(
        go.Scatter(
            x=perf_dff["Datetime"],
            y=perf_dff["halving 2012"],
            name="Halving 2012-2016 performance",
            mode='lines',
            line_color='#FFFFFF',
        ))

    performance.add_trace(
        go.Scatter(
            x=perf_dff["Datetime"],
            y=perf_dff["halving 2016"],
            name="Halving 2016-2020 performance",
            mode='lines',
            line_color='#028A0F',
        ))

    performance.add_trace(
        go.Scatter(
            x=price_dff["Datetime"],
            y=price_dff["BTC Price"],
            name="Current Halving performance",
            mode='lines',
            line_color='#E56717',
        ))

    performance.update_layout(
        title_text="Post Halving Performances",
        template='plotly_dark'
    )

    performance.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    performance.update_yaxes(
        tickvals=[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000],
        tickprefix="$",
        title_text="BTC Price(USD)",
        type="log",
    )
    performance.update_xaxes(nticks=20)

    return performance


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=7000, host='0.0.0.0')
