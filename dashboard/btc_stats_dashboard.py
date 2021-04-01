from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output

# start app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

# app.css.append_css(
#     {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server


last_h_date = datetime.strptime("11-05-2020", "%d-%m-%Y")
S2F_list = ["S2F price 365d average", "S2F price"]
# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Bitcoin & Blockchain Statistics",
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


                                        dcc.Graph(id="supply", figure={},
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


@ app.callback(
    Output('supply', 'figure'),
    Input('df-update', 'n_intervals')
)
def update_supply(n):

    supply_df = query_mongo("btc_analysis", "btc_total_supply")
    supply_dff = supply_df.copy()

    try:

        supply_dff["Date"] = [datetime.strptime(
            date, "%d-%m-%Y") for date in supply_dff["Date"]]

    except TypeError:
        pass

    supply_graph = go.Figure()

    supply_graph.add_trace(
        go.Scatter(
            x=supply_dff["Date"],
            y=supply_dff["Supply"],
            name="BTC Effective Supply",
            mode='lines',
            line_color='#FFFFFF',
        ))

    supply_graph.add_trace(
        go.Scatter(
            x=supply_dff["Date"],
            y=supply_dff["Theoretical Supply"],
            name="BTC Theoretical Supply",
            mode='lines',
            line_color='#028A0F',
        ))

    supply_graph.update_layout(
        title_text="Bitcoin Supply",
        template='plotly_dark'
    )

    supply_graph.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    supply_graph.update_yaxes(
        title_text="Number of Bitcoin",
    )
    supply_graph.update_xaxes(nticks=20,
                              title_text="Date"
                              )

    return supply_graph


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')
