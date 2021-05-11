import urllib.parse
from datetime import datetime, date

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.calc import last_quarter_end
from btc_analysis.config import (BEST_PERFORMING_LIST,
                                 BEST_PERFORMING_LIST_VOL, COMPLETE_MKT_CAP,
                                 CRYPTO_LIST, DB_NAME, YAHOO_DASH_LIST)
from btc_analysis.dashboard_func import (btc_total_dfs, usd_den_total_df,
                                         vola_total_df, date_elements,
                                         perf_df_creator)
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
# btc denominated initial variables

yesterday = yesterday_str()
max_year = int(datetime.strptime(yesterday, "%Y-%m-%d").year)
max_month = int(datetime.strptime(yesterday, "%Y-%m-%d").month)
max_day = int(datetime.strptime(yesterday, "%Y-%m-%d").day)

last_quarter_ = last_quarter_end()
last_quarter = datetime.strptime(
    last_quarter_, "%d-%m-%Y").strftime("%Y-%m-%d")


window_list = ["5Y", "3Y", "2Y", "1Y", "6M", "3M", "1M", "1W", "YTD"]
vola_days_list = ["252", "90", "30"]
as_of_list = [yesterday, last_quarter_]

all_options = {
    '5Y': [yesterday, last_quarter_],
    '3Y': [yesterday, last_quarter_],
    '2Y': [yesterday, last_quarter_],
    '1Y': [yesterday, last_quarter_],
    '6M': [yesterday, last_quarter_],
    '3M': [yesterday, last_quarter_],
    '1M': [yesterday, last_quarter_],
    '1W': [yesterday, last_quarter_],
    'YTD': [yesterday, last_quarter_],
}

# btc correlation initial variables

corr_window_list = ["3Y", "1Y", "1Q", "1M", "YTD"]

df_alt = query_mongo(DB_NAME, "dash_corr_crypto")

df_alt_col = list(df_alt.columns)
df_alt_col.remove('Date')
df_alt_col.remove('Window')
df_alt_col.remove('As Of')

# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Crypto-Assets Analysis",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),

    # btc denominated crypto-assets
    dbc.Row([
            dbc.Col([

                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.Row([

                                    dbc.Col([

                                        html.Label(['Time Window:']),

                                        dcc.Dropdown(
                                            id='time_window_dropdown',
                                            options=[{'label': k, 'value': k}
                                                     for k in all_options.keys()],
                                            multi=False,
                                            value="1W",
                                            style={"width": "50%"},
                                            clearable=False
                                        ),

                                        html.Hr(),

                                        html.Label(['As of:']),

                                        dcc.Dropdown(id='as_of_dropdown',
                                                     style={"width": "50%"},
                                                     ),

                                        html.Hr(),

                                        dcc.Checklist(
                                            id='crypto_checklist',
                                            options=[
                                                {'label': x, 'value': x} for x in CRYPTO_LIST
                                            ],
                                            value=["BTC", "ETH",
                                                   "XRP", "LTC", "BCH"],
                                            labelStyle={
                                                'display': 'inline-block'},
                                            inputStyle={"margin-right": "10px",
                                                        "margin-left": "10px"}
                                        ),
                                    ]),
                                ]),

                                dbc.Row([

                                    dbc.Col([

                                        dcc.Graph(
                                            id='crypto_line', figure={}),

                                        html.A(
                                            'Download Data',
                                            id='download-link_alt',
                                            download="altcoin_rawdata.csv",
                                            href="",
                                            target="_blank"
                                        )
                                    ], width=8),

                                    dbc.Col([

                                            dcc.Graph(
                                                id='crypto_perf', figure={}),

                                            ], width=4)

                                ], no_gutters=True),
                            ]),
                    ],
                    style={"width": "70rem"},
                    className="mt-3"
                )

            ]),

            ], justify='center'),

    # crypto-assets correlation with bitcoin

    dbc.Row([
        dbc.Col([

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col([

                                    html.Label(['Time Window']),

                                    dcc.Dropdown(
                                        id='my_alt_dropdown',
                                        options=[
                                            {'label': w, 'value': w} for w in corr_window_list
                                        ],
                                        multi=False,
                                        value="1Y",
                                        style={"width": "50%"},
                                        clearable=False
                                    ),

                                    html.Hr(),

                                    html.Label(['Date Range:']),

                                    html.Br(),

                                    dcc.DatePickerRange(
                                        id='date_range_corr',
                                        min_date_allowed=date(2017, 1, 1),
                                        initial_visible_month=date(
                                            max_year, max_month, 1),
                                        start_date=date(max_year, 1, 1)
                                    ),

                                    html.Hr(),

                                    dcc.Checklist(
                                        id='my_alt_check',
                                        options=[
                                            {'label': x, 'value': x} for x in df_alt_col
                                        ],
                                        value=["ETH", "XRP", "LTC", "BCH"],
                                        labelStyle={
                                            'display': 'inline-block'},
                                        inputStyle={"margin-right": "10px",
                                                    "margin-left": "10px"}
                                    ),


                                    dcc.Graph(
                                        id='btc_corr_line', figure={}),

                                    html.A(
                                        'Download Data',
                                        id='download-link_alt_corr',
                                        download="altcoin_rawdata.csv",
                                        href="",
                                        target="_blank"
                                    )
                                ])

                            ]),
                        ]),
                ],
                style={"width": "70rem"},
                className="mt-3"
            )

        ]),

    ], justify='center'),


    # stablecoin supply

    dbc.Row([
        dbc.Col([

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col([


                                    html.Hr(),

                                    html.Label(['Date Range:']),

                                    html.Br(),

                                    dcc.DatePickerRange(
                                        id='date_range_stable',
                                        min_date_allowed=date(2017, 1, 1),
                                        initial_visible_month=date(
                                            max_year - 1, max_month, 1),
                                        start_date=date(max_year - 1, 1, 1)
                                    ),

                                    # html.Hr(),

                                    # dcc.Checklist(
                                    #     id='my_alt_check',
                                    #     options=[
                                    #         {'label': x, 'value': x} for x in df_alt_col
                                    #     ],
                                    #     value=["ETH", "XRP", "LTC", "BCH"],
                                    #     labelStyle={
                                    #         'display': 'inline-block'},
                                    #     inputStyle={"margin-right": "10px",
                                    #                 "margin-left": "10px"}
                                    # ),


                                    dcc.Graph(
                                        id='stable_supply_line', figure={}),

                                    # html.A(
                                    #     'Download Data',
                                    #     id='download-link_alt_corr',
                                    #     download="altcoin_rawdata.csv",
                                    #     href="",
                                    #     target="_blank"
                                    # )
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

# dropdown can be unified putting the same ID into the Input of each callback,
# NB: the dropdpwn display should be, at that point, disabled except for the
# first one
# naming has to be commented in the layout part for the second and third graph

# btc denominated crypto-assets callbacks


@ app.callback(
    Output(component_id='as_of_dropdown', component_property='options'),
    Input(component_id="time_window_dropdown", component_property="value")
)
def set_as_of_option(selected_time_window):

    yesterday = yesterday_str()
    last_quarter_ = last_quarter_end()

    all_options = {
        '5Y': [yesterday, last_quarter_],
        '3Y': [yesterday, last_quarter_],
        '2Y': [yesterday, last_quarter_],
        '1Y': [yesterday, last_quarter_],
        '6M': [yesterday, last_quarter_],
        '3M': [yesterday, last_quarter_],
        '1M': [yesterday, last_quarter_],
        '1W': [yesterday, last_quarter_],
        'YTD': [yesterday, last_quarter_],
    }

    return [{'label': i, 'value': i} for i in all_options[selected_time_window]]


@ app.callback(
    Output(component_id="as_of_dropdown", component_property="value"),
    Input(component_id="as_of_dropdown", component_property="options")
)
def set_as_of_value(available_options):

    return available_options[0]['value']


@ app.callback(
    [Output(component_id="crypto_line", component_property="figure"),
     Output(component_id="crypto_perf", component_property="figure"),
     Output(component_id='download-link_alt', component_property='href')],
    [Input(component_id="time_window_dropdown", component_property="value"),
        Input(component_id="as_of_dropdown", component_property="value"),
     Input(component_id="crypto_checklist", component_property="value")]
)
def update_graph_btc_den(window_selection, as_of_selection, asset_selection):

    df_alt = query_mongo(DB_NAME, "dash_btc_den_crypto")
    dff_alt = df_alt.copy()

    # window selection
    dff_alt_w = dff_alt.loc[dff_alt.Window == window_selection]
    dff_alt_w = dff_alt_w.drop(columns=["Window"])

    # as of selection
    dff_alt_as_of = dff_alt_w.loc[dff_alt_w["As Of"] == as_of_selection]
    dff_alt_as_of = dff_alt_as_of.drop(columns=["As Of"])

    # crypto checklist
    dff_date_alt = dff_alt_as_of["Date"]
    dff_alt_filtered = dff_alt_as_of[asset_selection]
    dff_alt_filtered["Date"] = dff_date_alt

    # perf graph
    fig_alt = px.line(
        data_frame=dff_alt_filtered,
        x="Date",
        y=asset_selection,
        #template='plotly_dark',
        template='plotly_white',
        labels={"value": "Performance",
                "variable": ""
                },
        title='Crypto-Assets: BTC denominated performances',
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

    fig_alt.update_layout(
        height=500,
    )

    # performances table
    dff_for_table = dff_alt_filtered.copy()
    dff_for_table = dff_for_table.drop(columns="Date")

    perf_df = perf_df_creator(dff_for_table)
    perf_df = perf_df.loc[perf_df["Crypto-Asset"] != "BTC"]

    table_perf = go.Figure(data=[go.Table(
        columnwidth=[60, 80],
        header=dict(values=["Crypto-Asset", "Performance"],
                    line_color='white',
                    fill_color='black',
                    align='center',
                    font=dict(color='white', size=12),
                    height=35),
        cells=dict(values=[perf_df["Crypto-Asset"], perf_df["Performance"]],
                   line_color='white',
                   fill_color='black',
                   format=[None, ",.2f"],
                   suffix=[None, '%'],
                   align=['center', 'right'],
                   font=dict(color='white', size=11),
                   height=25)
    )
    ])

    table_perf.update_layout(
        title_text="Crypto-Assets Performances",
        # template='plotly_dark',
        template='plotly_white',
        height=500,
    )

    csv_string_alt = dff_alt_w.to_csv(index=False, encoding='utf-8')
    csv_string_alt = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_alt)

    return fig_alt, table_perf, csv_string_alt


# crypto-assets correlation with bictoin


@ app.callback(
    Output(component_id="date_range_corr",
           component_property="max_date_allowed"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_max_date(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id="date_range_corr",
           component_property="end_date"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_end_date(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@ app.callback(
    [
        Output(component_id="btc_corr_line", component_property="figure"),
        Output(component_id='download-link_alt_corr', component_property='href')
    ],
    [
        Input(component_id="my_alt_dropdown", component_property="value"),
        Input(component_id='date_range_corr',
              component_property='start_date'),
        Input(component_id='date_range_corr', component_property='end_date'),
        Input(component_id="my_alt_check", component_property="value"),
        Input(component_id="yahoo-update", component_property="n_intervals")
    ]
)
def update_graph_corr(window_selection, start, stop, asset_selection, n):

    df_alt = query_mongo(DB_NAME, "dash_corr_crypto")
    dff_alt = df_alt.copy()

    dff_w_alt = dff_alt.loc[dff_alt.Window == window_selection]
    dff_w_alt = dff_w_alt.drop(columns=["Window", "As Of"])

    dff_range = dff_w_alt.loc[dff_w_alt.Date.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)

    dff_date = dff_range["Date"]

    dff_alt_filtered = dff_range[asset_selection]
    dff_alt_filtered["Date"] = dff_date

    fig_corr = px.line(
        data_frame=dff_alt_filtered,
        x="Date",
        y=asset_selection,
        # template='plotly_dark',
        template='plotly_white',
        labels={"value": "Correlation",
                "variable": ""},
        title='Crypto-Assets: Correlation with Bitcoin',
        range_y=[-1, 1],
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

    csv_string = dff_range.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string)

    return fig_corr, csv_string


# syablecoin supply


@ app.callback(
    Output(component_id="date_range_stable",
           component_property="max_date_allowed"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_max_date_stable(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id="date_range_stable",
           component_property="end_date"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_end_date_stable(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@ app.callback(
    Output(component_id="stable_supply_line", component_property="figure"),
    [
        Input(component_id='date_range_stable',
              component_property='start_date'),
        Input(component_id='date_range_stable', component_property='end_date'),
        Input(component_id="yahoo-update", component_property="n_intervals")
    ]
)
def update_graph_stable_supply(start, stop, n):

    df_stable = query_mongo(DB_NAME, "stablecoin_all")
    dff_stable = df_stable.copy()

    dff_stable["Datetime"] = [datetime.strptime(
        x, "%Y-%m-%d") for x in dff_stable["Date"]]

    dff_range = dff_stable.loc[dff_stable.Datetime.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)

    fig_stable = go.Figure()

    fig_stable.add_trace(
        go.Scatter(
            x=dff_range["Datetime"],
            y=dff_range["USDT Supply"],
            name="USDT Supply",
            mode='lines',
            line_color="#86CE00",
        ))

    fig_stable.add_trace(
        go.Scatter(
            x=dff_range["Datetime"],
            y=dff_range["USDC Supply"],
            name="USDC Supply",
            mode='lines',
            line_color="#511CFB",
        ))

    fig_stable.update_layout(
        title_text="Stablecoins Supply",
        # template='plotly_dark',
        template='plotly_white',
    )

    fig_stable.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
        height=600
    )

    fig_stable.update_yaxes(
        # tickprefix="$",
        title_text="Number of Coins",
        fixedrange=True
    )

    fig_stable.update_xaxes(
        title_text="Date",
    )

    return fig_stable


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=4000, host='0.0.0.0')
