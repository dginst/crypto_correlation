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


# start app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server


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

    dff = df.copy()

    dff = dff.tail(len(dff.index) - 720)

    dff["Year"] = dff["Date"].str.slice(start=-4)

    model_price = px.line(
        data_frame=dff,
        x="Year",
        y="S2F price",
        template='plotly_dark',
        title='Stock to Flow model',
        log_y=True,
    )

    model_price.update_yaxes(
        tickvals=[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000],
        tickprefix="$"
    )

    # model_price.update_xaxes(
    #     tickvals=[20],
    #     tickprefix="$"
    # )
    # index_area.update_layout(showlegend=False)

    return model_price


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=7000, host='0.0.0.0')
