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
from btc_analysis.dashboard_func import (
    date_elements, btc_price_min, btc_yearly_perf)

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

                                        ], width=7),

                                        dbc.Col([

                                            dcc.Graph(
                                                id='btc_perf', figure={}),

                                        ], width=5)

                                    ], no_gutters=True),

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


                                    ], width=8),

                                    dbc.Col([

                                        dcc.Graph(
                                            id='btc_log_perf', figure={}),

                                    ], width=4)
                                ], no_gutters=True),

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

    dbc.Row([
            dbc.Col([

                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col([

                                            html.Hr(),

                                            html.Label(['Date Range:']),

                                            html.Br(),

                                            dcc.DatePickerRange(
                                                id='date_range_hash',
                                                min_date_allowed=date(
                                                    2011, 2, 1),
                                                start_date=date(2020, 1, 1),
                                            ),



                                            dcc.Graph(id="hash_rate", figure={},
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
           component_property="initial_visible_month"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_initial_date(n):

    max_y, max_m, _ = date_elements()

    initial_visible_month_ = date(max_y, max_m, 1)

    return initial_visible_month_


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
        Output(component_id='btc_perf', component_property='figure'),
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
    dff_for_perf = df_price.copy()
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
        x=1,
    ),
        height=600
    )

    price_.update_yaxes(
        tickprefix="$",
        title_text="BTC Price (USD)",
        fixedrange=True
    )

    price_.update_xaxes(
        title_text="Date",
    )

    # table

    perf_df = btc_yearly_perf(dff_for_perf)
    print(perf_df)

    table_perf = go.Figure(data=[go.Table(
        columnwidth=[100, 80, 100],
        header=dict(values=list(perf_df.columns),
                    line_color='white',
                    fill_color='black',
                    align='center',
                    font=dict(color='white', size=12),
                    height=35),
        cells=dict(values=[perf_df.Date, perf_df.Price, perf_df["Yearly Performance"]],
                   line_color='white',
                   fill_color='black',
                   align=['center', 'right', 'right'],
                   font=dict(color='white', size=11),
                   format=[None, None, ",.2f%"],
                   suffix=[None, '$', '%'],
                   height=25)
    )
    ])

    table_perf.update_layout(
        title_text="Bitcoin Yearly Performances",
        template='plotly_dark',
        height=600,
    )

    csv_string_price = df_to_download.to_csv(index=False, encoding='utf-8')
    csv_string_price = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_price)

    return price_, table_perf, csv_string_price


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
    [Output(component_id='btc_price_log', component_property='figure'),
     Output(component_id='btc_log_perf', component_property='figure'),
     ],
    Input(component_id='df-update', component_property='n_intervals')

)
def update_log_price(n):

    df_price = query_mongo("btc_analysis", "S2F_BTC_price")
    df_price = df_price.drop(columns=["Days to Halving"])

    dff = df_price.copy()

    min_point = btc_price_min(dff)

    model_cap = go.Figure()

    model_cap.add_trace(
        go.Scatter(
            x=dff["Datetime"],
            y=dff["BTC Price"],
            name="BTC Price Log Scale",
            mode='lines',
            line_color="#FEAF16",
        ))

    model_cap.add_trace(
        go.Scatter(
            x=min_point["Datetime"],
            y=min_point["BTC Price"],
            name="BTC Price Minimum",
            text=min_point["BTC Price"],
            textposition="bottom center",
            # mode='markers+text',
            mode='markers',
            marker=dict(color="#C0C0C0",
                        size=10
                        ),
        ))

    model_cap.update_layout(
        title_text="Bitcoin Price Log Scale",
        template='plotly_dark'
    )

    # model_cap.add_annotation(x=min_point["Datetime"],
    #                          y=min_point["BTC Price"],
    #                          text=min_point["BTC Price"],
    #                          showarrow=True,
    #                          arrowhead=1)

    model_cap.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
        height=500,
    )

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

    # table

    min_point_dff = min_point.copy()
    min_point_dff["Year"] = [int(d.year) for d in min_point_dff["Datetime"]]
    min_point_dff = min_point_dff.drop(columns=["Datetime", "Date"])

    table_log_perf = go.Figure(data=[go.Table(
        columnwidth=[60, 150],
        header=dict(values=["Year", "Min Price"],
                    line_color='white',
                    fill_color='black',
                    align='center',
                    font=dict(color='white', size=12),
                    height=35),
        cells=dict(values=[min_point_dff["Year"], min_point_dff["BTC Price"]],
                   line_color='white',
                   fill_color='black',
                   align=['center', 'left'],
                   font=dict(color='white', size=11),
                   height=25)
    )
    ])

    table_log_perf.update_layout(
        title_text="Bitcoin Minimum Prices",
        template='plotly_dark',
        height=500,
    )

    return model_cap, table_log_perf

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
            date, "%Y-%m-%d") for date in supply_dff["Date"]]

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


# hash rate

@app.callback(
    Output(component_id="date_range_hash",
           component_property="end_date"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_end_date_hash(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@app.callback(
    Output(component_id="date_range_hash",
           component_property="initial_visible_month"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_initial_date_hash(n):

    max_y, max_m, _ = date_elements()

    initial_visible_month_ = date(max_y, max_m, 1)

    return initial_visible_month_


@app.callback(
    Output(component_id="date_range_hash",
           component_property="max_date_allowed"),
    Input(component_id="df-update", component_property="n_intervals")
)
def set_max_date_hash(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id='hash_rate', component_property='figure'),
    [
        Input(component_id='date_range_price',
              component_property='start_date'),
        Input(component_id="date_range_hash",
              component_property="end_date"),
        Input(component_id='df-update', component_property='n_intervals')]
)
def update_hash_rate(start, stop, n):

    hr_df = query_mongo("btc_analysis", "hash_rate")
    hr_dff = hr_df.copy()

    try:

        hr_dff["Date"] = [datetime.strptime(
            date, "%Y-%m-%d") for date in hr_dff["Date"]]

    except TypeError:
        pass

    hr_dff_range = hr_dff.loc[hr_dff.Date.between(
        start, stop, inclusive=True)]
    hr_dff_range.reset_index(drop=True, inplace=True)

    hr_graph = go.Figure()

    hr_graph.add_trace(
        go.Scatter(
            x=hr_dff_range["Date"],
            y=hr_dff_range["Hash Rate"],
            name="BTC Hash Rate",
            mode='lines',
            line_color='#FFFFFF',
        ))

    hr_graph.update_layout(
        title_text="Bitcoin Hash Rate",
        template='plotly_dark'
    )

    hr_graph.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    hr_graph.update_yaxes(
        title_text="Hash",
    )
    hr_graph.update_xaxes(nticks=20,
                          title_text="Date"
                          )

    return hr_graph


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=3500, host='0.0.0.0')
