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
                                 BEST_PERFORMING_LIST_VOL,
                                 COMPLETE_MKT_CAP,
                                 CRYPTO_LIST, DB_NAME,
                                 YAHOO_DASH_LIST)
from btc_analysis.dashboard_func import (btc_total_dfs,
                                         usd_den_total_df,
                                         vola_total_df,
                                         date_elements)
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
yesterday = yesterday_str()
max_year = int(datetime.strptime(yesterday, "%Y-%m-%d").year)
max_month = int(datetime.strptime(yesterday, "%Y-%m-%d").month)
max_day = int(datetime.strptime(yesterday, "%Y-%m-%d").day)

last_quarter_ = last_quarter_end()
last_quarter = datetime.strptime(
    last_quarter_, "%d-%m-%Y").strftime("%Y-%m-%d")


corr_window_list = ["3Y", "1Y", "1Q", "1M", "YTD"]
window_list = ["5Y", "3Y", "2Y", "1Y", "6M", "3M", "1M", "1W", "YTD"]
vola_days_list = ["252", "90", "30", "ewm"]
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

corr_best_list = ["AMAZON",
                  "TESLA", "APPLE",
                  "NETFLIX"]
# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Best Performing Asset Analysis",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),

    dbc.Row([

        dbc.Col([

            dbc.Card(
                [
                    dbc.CardBody(
                        [

                            dbc.Row([

                                dbc.Col([


                                    html.Label(['Mode:']),

                                    dcc.Dropdown(
                                        id='color_mode',
                                        options=[
                                            {'label': 'Light Mode',
                                                'value': 'plotly_white'},
                                            {'label': 'Dark Mode',
                                                'value': 'plotly_dark'}

                                        ],
                                        multi=False,
                                        value="plotly_dark",
                                        style={"width": "50%"},
                                        clearable=False
                                    ),
                                ]),
                            ]),
                        ]),
                ]),
        ]),
    ]),
    # best performing asset performances

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
                                            id='time_window_dropdown',
                                            options=[{'label': k, 'value': k}
                                                     for k in window_list],
                                            multi=False,
                                            value="3M",
                                            style={"width": "50%"},
                                            clearable=True
                                        ),


                                        html.Hr(),

                                        html.Label(['As of:']),

                                        dcc.Dropdown(
                                            id='as_of_dropdown',
                                            style={"width": "50%"},
                                        ),

                                        html.Hr(),

                                        dcc.Checklist(
                                            id='usd_best_check',
                                            options=[
                                                {'label': x, 'value': x} for x in BEST_PERFORMING_LIST
                                            ],
                                            value=["BTC", "AMAZON",
                                                   "TESLA", "APPLE", "NETFLIX"],
                                            labelStyle={
                                                'display': 'inline-block'},
                                            inputStyle={"margin-right": "10px",
                                                        "margin-left": "10px"}
                                        ),

                                        dcc.Graph(
                                            id='best_perf_line', figure={}),

                                        html.A(
                                            'Download Data',
                                            id='download-link_yahoo_norm',
                                            download="yahoo_normalized.csv",
                                            href='',
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

    # best performing asset correlation with btc

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
                                        id='best_corr_dropdown',
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
                                        id='date_range_best_corr',
                                        min_date_allowed=date(2017, 1, 1),
                                        initial_visible_month=date(
                                            max_year, max_month, 1),
                                        start_date=date(max_year, 1, 1),
                                    ),

                                    html.Hr(),

                                    dcc.Checklist(
                                        id='best_corr_check',
                                        options=[
                                            {'label': x, 'value': x} for x in corr_best_list
                                        ],
                                        value=["AMAZON",
                                               "TESLA", "APPLE", "NETFLIX"],
                                        labelStyle={
                                            'display': 'inline-block'},
                                        inputStyle={"margin-right": "10px",
                                                    "margin-left": "10px"}
                                    ),


                                    dcc.Graph(
                                        id='best_corr_graph', figure={}),

                                    html.Hr(),

                                    html.A(
                                        'Download Data',
                                        id='download-link_corr_best',
                                        download="correlation_rawdata.csv",
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

    # best performing assets and BTC volatility

    dbc.Row([
            dbc.Col([

                dbc.Card(
                    [
                        dbc.CardBody(
                            [

                                dbc.Row([
                                    dbc.Col([

                                        html.Label(['Rolling Days:']),

                                        dcc.Dropdown(
                                            id='vola_dropdown',
                                            options=[
                                                {'label': w, 'value': w} for w in vola_days_list
                                            ],
                                            multi=False,
                                            value="ewm",
                                            style={"width": "50%"},
                                            clearable=False
                                        ),

                                        html.Hr(),

                                        html.Label(['Date Range:']),

                                        html.Br(),

                                        dcc.DatePickerRange(
                                            id='date_range_vola',
                                            min_date_allowed=date(2017, 1, 1),
                                            initial_visible_month=date(
                                                max_year, max_month, 1),
                                            start_date=date(max_year, 1, 1),
                                        ),

                                        html.Hr(),

                                        dcc.Checklist(
                                            id='vola_checklist',
                                            options=[
                                                {'label': x, 'value': x} for x in BEST_PERFORMING_LIST
                                            ],
                                            value=["BTC", "AMAZON",
                                                   "TESLA", "APPLE", "NETFLIX"],
                                            labelStyle={
                                                'display': 'inline-block'},
                                            inputStyle={"margin-right": "10px",
                                                        "margin-left": "10px"}
                                        ),

                                        dcc.Graph(
                                            id='vola_graph', figure={}),

                                        html.A(
                                            'Download Data',
                                            id='download-link_yahoo_vola',
                                            download="yahoo_vola.csv",
                                            href='',
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

    # best performing assets volume

    dbc.Row([
            dbc.Col([

                dbc.Card(
                    [
                        dbc.CardBody(
                            [

                                dbc.Row([
                                    dbc.Col([

                                        html.Label(['Date Range:']),

                                        html.Br(),

                                        dcc.DatePickerRange(
                                            id='date_range_vol',
                                            min_date_allowed=date(2017, 1, 1),
                                            initial_visible_month=date(
                                                max_year, max_month, 1),
                                            start_date=date(
                                                max_year - 1, 1, 1),
                                        ),

                                        html.Hr(),
                                        dcc.Checklist(
                                            id='best_volume',
                                            options=[
                                                {'label': x, 'value': x} for x in BEST_PERFORMING_LIST_VOL
                                            ],
                                            value=["BTC", "AMAZON",
                                                   "TESLA", "APPLE",
                                                   "NETFLIX"],
                                            labelStyle={
                                                'display': 'inline-block'},
                                            inputStyle={"margin-right": "10px",
                                                        "margin-left": "10px"}
                                        ),

                                        dcc.Graph(
                                            id='volume_graph', figure={}),

                                        html.A(
                                            'Download Data',
                                            id='download-link_yahoo_volume',
                                            download="yahoo_volume.csv",
                                            href='',
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

    dcc.Interval(id='update', n_intervals=0, interval=1000 * 5),

    dcc.Interval(id='yahoo-update', interval=100000, n_intervals=0)
])

# --------------------------
# Callbacks part


# dropdown can be unified putting the same ID into the Input of each callback,
# NB: the dropdpwn display should be, at that point, disabled except for the
# first one
# naming has to be commented in the layout part for the second and third graph

# best perfomring asset performances


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


# @app.callback(
#     Output(component_id='as_of_dropdown', component_property='options'),
#     Input(component_id="time_window_dropdown", component_property="value")
# )
# def set_as_of_option(selected_time_window):

#     return [{'label': i, 'value': i} for i in all_options[selected_time_window]]


@ app.callback(
    Output(component_id="as_of_dropdown", component_property="value"),
    Input(component_id="as_of_dropdown", component_property="options")
)
def set_as_of_value(available_options):

    return available_options[0]['value']


@ app.callback(
    [Output(component_id="best_perf_line", component_property="figure"),
     Output(component_id='download-link_yahoo_norm', component_property='href')],
    [Input(component_id="time_window_dropdown", component_property="value"),
        Input(component_id="as_of_dropdown", component_property="value"),
     Input(component_id="usd_best_check", component_property="value"),
     Input(component_id="color_mode", component_property="value")]
)
def update_graph_usd_best(window_selection, as_of_selection, asset_selection, sel_col):

    df_usd_norm = query_mongo(DB_NAME, "dash_usd_den")

    dff_norm = df_usd_norm.copy()

    if sel_col == "plotly_white":
        font_col = "black"
    else:
        font_col = "white"

    # window selection
    dff_norm_w = dff_norm.loc[dff_norm.Window == window_selection]
    dff_norm_w = dff_norm_w.drop(columns=["Window"])

    # as of selection
    dff_norm_as_of = dff_norm_w.loc[dff_norm_w["As Of"] == as_of_selection]
    dff_norm_as_of = dff_norm_as_of.drop(columns=["As Of"])

    dff_date_n = dff_norm_as_of["Date"]

    dff_filtered_norm = dff_norm_as_of[asset_selection]
    dff_filtered_norm["Date"] = dff_date_n

    fig_yahoo_norm = px.line(
        data_frame=dff_filtered_norm,
        x="Date",
        y=asset_selection,
        template=sel_col,
        labels={"value": "",
                "variable": "",
                "Date": ""},
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    fig_yahoo_norm.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1,
    ))

    fig_yahoo_norm.update_layout(
        title_text='Best Performing Asset: USD denominated performances',
        font_color=font_col,
        title_font_color=font_col,
        height=500,
        title_xanchor="left",
        title_x=0.05,
        title_y=0.98,
        title_yanchor="top",
        title_pad=dict(b=150)
    )
    csv_string_norm = dff_norm_w.to_csv(index=False, encoding='utf-8')
    csv_string_norm = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_norm)

    return fig_yahoo_norm, csv_string_norm


# volatility

@ app.callback(
    Output(component_id="date_range_vola",
           component_property="max_date_allowed"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_max_date_vola(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id="date_range_vola",
           component_property="end_date"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_end_date_vola(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@ app.callback(
    [Output(component_id="vola_graph", component_property="figure"),
     Output(component_id='download-link_yahoo_vola', component_property='href')],
    [Input(component_id="vola_dropdown", component_property="value"),
     Input(component_id='date_range_vola', component_property='start_date'),
     Input(component_id='date_range_vola', component_property='end_date'),
     Input(component_id="vola_checklist", component_property="value"),
     Input(component_id="color_mode", component_property="value")]
)
def update_graph_vola(days_selection, start, stop, asset_selection, sel_col):

    df_vola = query_mongo(DB_NAME, "dash_vola")
    dff_vola = df_vola.copy()

    if sel_col == "plotly_white":
        font_col = "black"
    else:
        font_col = "white"

    # selecting the rooling days vola type
    dff_days = dff_vola.loc[dff_vola.Days == days_selection]
    dff_days = dff_days.drop(columns=["Days"])

    # selecting start and stop
    dff_range = dff_days.loc[dff_days.Date.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)

    dff_v_date = dff_range["Date"]

    dff_vola_filtered = dff_range[asset_selection]
    dff_vola_filtered["Date"] = dff_v_date

    fig_yahoo_vola = px.line(
        data_frame=dff_vola_filtered,
        x="Date",
        y=asset_selection,
        template=sel_col,
        labels={"value": "",
                "variable": "",
                "Date": ""},
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    fig_yahoo_vola.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ))

    fig_yahoo_vola.update_layout(
        yaxis_tickformat='%',
        title_text='Annualized Volatility',
        font_color=font_col,
        title_font_color=font_col,
        height=500,
        title_xanchor="left",
        title_x=0.05,
        title_y=0.98,
        title_yanchor="top",
        title_pad=dict(b=150)
    )

    csv_string_vola = dff_range.to_csv(index=False, encoding='utf-8')
    csv_string_vola = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_vola)

    return fig_yahoo_vola, csv_string_vola


# volume

@ app.callback(
    Output(component_id="date_range_vol",
           component_property="max_date_allowed"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_max_date_vol(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id="date_range_vol",
           component_property="end_date"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_end_date_vol(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@ app.callback(
    [Output(component_id="volume_graph", component_property="figure"),
     Output(component_id='download-link_yahoo_volume', component_property='href')],
    [Input(component_id='date_range_vol', component_property='start_date'),
     Input(component_id='date_range_vol', component_property='end_date'),
     Input(component_id="best_volume", component_property="value"),
     Input(component_id="color_mode", component_property="value")
     ]
)
def update_graph_volume(start, stop, asset_selection, sel_col):

    df_volume = query_mongo(DB_NAME, "all_volume_y")
    dff_volume = df_volume.copy()

    if sel_col == "plotly_white":
        font_col = "black"
    else:
        font_col = "white"

    # selecting start and stop
    dff_vol_range = dff_volume.loc[dff_volume.Date.between(
        start, stop, inclusive=True)]
    dff_vol_range.reset_index(drop=True, inplace=True)

    dff_vol_date = dff_vol_range["Date"]

    dff_vol_filtered = dff_vol_range[asset_selection]
    dff_vol_filtered["Date"] = dff_vol_date

    fig_volume = px.line(
        data_frame=dff_vol_filtered,
        x="Date",
        y=asset_selection,
        template=sel_col,
        labels={"value": "",
                "variable": "",
                "Date": ""},
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    fig_volume.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ))

    fig_volume.update_layout(
        title_text='Volume in USD',
        font_color=font_col,
        title_font_color=font_col,
        height=500,
        title_xanchor="left",
        title_x=0.05,
        title_y=0.98,
        title_yanchor="top",
        title_pad=dict(b=150)
    )

    csv_string_volume = dff_vol_filtered.to_csv(index=False, encoding='utf-8')
    csv_string_volume = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_volume)

    return fig_volume, csv_string_volume


# correlation with btc

@ app.callback(
    Output(component_id="date_range_best_corr",
           component_property="max_date_allowed"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_max_date_corr(n):

    max_y, max_m, max_d = date_elements()

    max_date = date(max_y, max_m, max_d)

    return max_date


@ app.callback(
    Output(component_id="date_range_best_corr",
           component_property="end_date"),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def set_end_date_corr(n):

    max_y, max_m, max_d = date_elements()

    end_date_ = date(max_y, max_m, max_d)

    return end_date_


@ app.callback(
    [
        Output(component_id="best_corr_graph", component_property="figure"),
        Output(component_id='download-link_corr_best',
               component_property='href')
    ],
    [
        Input(component_id="best_corr_dropdown", component_property="value"),
        Input(component_id='date_range_best_corr',
              component_property='start_date'),
        Input(component_id='date_range_best_corr',
              component_property='end_date'),
        Input(component_id="best_corr_check", component_property="value"),
        Input(component_id="yahoo-update", component_property="n_intervals"),
        Input(component_id="color_mode", component_property="value")
    ]
)
def update_corr_graph_asset(window_selection, start, stop, asset_selection, n, sel_col):

    df_yahoo = query_mongo(DB_NAME, "dash_corr_yahoo")
    dff_yahoo = df_yahoo.copy()
    dff_yahoo["Date"] = [datetime.strptime(
        x, "%Y-%m-%d") for x in dff_yahoo["Date"]]

    if sel_col == "plotly_white":
        font_col = "black"
        tick_col = "white"
    else:
        font_col = "white"
        tick_col = "#111111"

    dff_yahoo = dff_yahoo.drop(columns=["ETH", "XRP", "LTC"])

    dff_w = dff_yahoo.loc[dff_yahoo.Window == window_selection]
    dff_w = dff_w.drop(columns=["Window"])

    dff_range = dff_w.loc[dff_w.Date.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)
    dff_date = dff_range["Date"]

    dff_filtered = dff_range[asset_selection]
    dff_filtered["Date"] = dff_date

    fig_corr = px.line(
        data_frame=dff_filtered,
        x="Date",
        y=asset_selection,
        template=sel_col,
        labels={"value": "",
                "variable": "",
                "Date": ""},
        range_y=[-1, 1],
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    fig_corr.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ))

    fig_corr.update_layout(
        yaxis_tickformat='%',
        title_text='Best Performing Asset correlation with Bitcoin',
        font_color=font_col,
        title_font_color=font_col,
        height=500,
        title_xanchor="left",
        title_x=0.05,
        title_y=0.98,
        title_yanchor="top",
        title_pad=dict(b=150)
    )

    fig_corr.update_xaxes(ticks="outside", tickwidth=1,
                          tickcolor=tick_col, ticklen=10)

    csv_string = dff_range.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string)

    return fig_corr, csv_string


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')
