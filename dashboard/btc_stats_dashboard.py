import urllib.parse
from datetime import datetime, date

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output
from btc_analysis.market_data import yesterday_str
from btc_analysis.dashboard_func import date_elements

# start app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

# app.css.append_css(
#     {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

server = app.server

# ----------
# Date variables

# yesterday = yesterday_str()
# max_year = int(datetime.strptime(yesterday, "%Y-%m-%d").year)
# max_month = int(datetime.strptime(yesterday, "%Y-%m-%d").month)
# max_day = int(datetime.strptime(yesterday, "%Y-%m-%d").day)

# last_h_date = datetime.strptime("11-05-2020", "%d-%m-%Y")
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

                                            dcc.Graph(id="price_indicator", figure={},
                                                      config={'displayModeBar': False}),

                                            html.Hr(),

                                            html.Label(['Date Range:']),

                                            html.Br(),

                                            dcc.DatePickerRange(
                                                id='date_range_price',
                                                min_date_allowed=date(
                                                    2011, 2, 1),
                                                initial_visible_month=date(
                                                    max_year, max_month, 1),
                                                start_date=date(2011, 2, 1),
                                            ),

                                        ])
                                    ]),

                                html.Hr(),

                                dbc.Row(
                                    [
                                        dbc.Col([


                                            dcc.Graph(id="btc_price", figure={},
                                                      config={'displayModeBar': False}),

                                            html.A(
                                                'Download Data',
                                                id='download-link_price',
                                                download="btc_price.csv",
                                                href='',
                                                target="_blank"
                                            ),

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

                            html.Hr(),

                            dbc.Row(
                                [
                                    dbc.Col([

                                        dcc.Graph(id="btc_price_log", figure={},
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

# bitcoin price

@app.callback(
    Output(component_id="date_range_price",
           component_property="max_date_allowed"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_max_date(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@app.callback(
    Output(component_id="date_range_price",
           component_property="end_date"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_end_date(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_

@app.callback(
    [
        Output(component_id='btc_price', component_property='figure'),
        Output(component_id='download-link_price', component_property='href')
    ],
    [
        Input(component_id='date_range_price',
              component_property='start_date'),
        Input(component_id='date_range_price', component_property='end_date'),
        Input(component_id='df-update', component_property='n_intervals'),
    ]
)
def update_index_df(start, stop, n):

    df_price = query_mongo("btc_analysis", "S2F_BTC_price")
    df_price = df_price.drop(columns=["Days to Halving"])

    dff = df_price.copy()
    df_to_download = df_price.copy()

    dff_range = dff.loc[dff.Datetime.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)

    price_ = go.Figure()

    price_.add_trace(
        go.Scatter(
            x=dff_range["Datetime"],
            y=dff_range["BTC Price"],
            name="BTC Price",
            mode='lines',
            line_color="#FEAF16",
        ))

    price_.update_layout(
        title_text="Bitcoin Price",
        template='plotly_dark'
    )

    price_.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    price_.update_yaxes(
        tickprefix="$",
        title_text="BTC Price (USD)",
        fixedrange=True
    )

    price_.update_xaxes(
        title_text="Date",
    )

    csv_string_price = df_to_download.to_csv(index=False, encoding='utf-8')
    csv_string_price = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_price)

    return price_, csv_string_price


@ app.callback(
    Output('price_indicator', 'figure'),
    Input('update', 'n_intervals')
)
def update_indicator(timer):

    df_price = query_mongo("btc_analysis", "S2F_BTC_price")
    dff_p = df_price.copy()
    dff_p = dff_p.drop(columns=["Days to Halving"])

    dff_last_p = dff_p.tail(2)
    dff_ind_y = dff_last_p[dff_last_p['Datetime']
                           == dff_last_p['Datetime'].min()]['BTC Price'].values[0]
    dff_ind_t = dff_last_p[dff_last_p['Datetime']
                           == dff_last_p['Datetime'].max()]['BTC Price'].values[0]

    fig_indicator = go.Figure(go.Indicator(
        mode="delta",
        value=dff_ind_t,
        delta={'reference': dff_ind_y, 'relative': True, 'valueformat': '.2%'}))

    fig_indicator.update_traces(delta_font={'size': 18})

    fig_indicator.update_layout(height=50, width=100)

    if dff_ind_t >= dff_ind_y:
        fig_indicator.update_traces(delta_increasing_color='green')
    elif dff_ind_t < dff_ind_y:
        fig_indicator.update_traces(delta_decreasing_color='red')

    return fig_indicator


# btc price log scale

@ app.callback(
    Output(component_id='btc_price_log', component_property='figure'),
    Input(component_id='df-update', component_property='n_intervals')

)
def update_log_price(n):

    df_price = query_mongo("btc_analysis", "S2F_BTC_price")
    df_price = df_price.drop(columns=["Days to Halving"])

    dff = df_price.copy()

    model_cap = go.Figure()

    model_cap.add_trace(
        go.Scatter(
            x=dff["Datetime"],
            y=dff["BTC Price"],
            name="BTC Price Log Scale",
            mode='lines',
            line_color="#FEAF16",
        ))

    model_cap.update_layout(
        title_text="Bitcoin Price Log Scale",
        template='plotly_dark'
    )

    model_cap.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    model_cap.update_yaxes(
        tickvals=[1, 10, 100, 1000, 10000, 100000, 1000000],
        tickprefix="$",
        title_text="BTC Price (USD)",
        type="log",
        fixedrange=True
    )

    model_cap.update_xaxes(
        title_text="Date",
    )

    return model_cap

# bitcoin supply


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
    app.run_server(debug=True, port=3500, host='0.0.0.0')
