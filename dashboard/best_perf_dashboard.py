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
                                         vola_total_df)
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


# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Best Performing Asset Analysis",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),

    # best perfomring asset performances

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
                                            value="1W",
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
                                            id='my_yahoo_norm',
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
                                            value="252",
                                            style={"width": "50%"},
                                            clearable=False
                                        ),

                                        html.Hr(),

                                        html.Label(['Date Range:']),

                                        html.Br(),

                                        dcc.DatePickerRange(
                                            id='date-picker-range',
                                            min_date_allowed=date(2017, 1, 1),
                                            max_date_allowed=date(
                                                max_year, max_month, max_day),
                                            initial_visible_month=date(
                                                max_year, max_month, 1),
                                            start_date=date(max_year, 1, 1),
                                            end_date=date(
                                                max_year, max_month, max_day)
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
                                            id='date-picker-range_vol',
                                            min_date_allowed=date(2017, 1, 1),
                                            max_date_allowed=date(
                                                max_year, max_month, max_day),
                                            initial_visible_month=date(
                                                max_year, max_month, 1),
                                            start_date=date(max_year, 1, 1),
                                            end_date=date(
                                                max_year, max_month, max_day)
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

@app.callback(
    Output(component_id='as_of_dropdown', component_property='options'),
    Input(component_id="time_window_dropdown", component_property="value")
)
def set_as_of_option(selected_time_window):

    return [{'label': i, 'value': i} for i in all_options[selected_time_window]]


@app.callback(
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
     Input(component_id="my_yahoo_norm", component_property="value")]
)
def update_graph_norm(window_selection, as_of_selection, asset_selection):

    df_usd_norm = usd_den_total_df(window_list)

    dff_norm = df_usd_norm.copy()

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
        template='plotly_dark',
        labels={"value": "Performance",
                "variable": ""},
        title='Best Performing Asset: USD denominated performances',
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
        y=1.02,
        xanchor="right",
        x=1,
    ))

    csv_string_norm = dff_norm_w.to_csv(index=False, encoding='utf-8')
    csv_string_norm = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_norm)

    return fig_yahoo_norm, csv_string_norm


# volatility

@ app.callback(
    [Output(component_id="vola_graph", component_property="figure"),
     Output(component_id='download-link_yahoo_vola', component_property='href')],
    [Input(component_id="vola_dropdown", component_property="value"),
     Input(component_id='date-picker-range', component_property='start_date'),
     Input(component_id='date-picker-range', component_property='end_date'),
     Input(component_id="vola_checklist", component_property="value")]
)
def update_graph_vola(days_selection, start, stop, asset_selection):

    df_vola = vola_total_df(vola_days_list)
    dff_vola = df_vola.copy()

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
        template='plotly_dark',
        title='Annualized Volatility',
        labels={"value": "Volatility",
                "variable": ""},
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

    csv_string_vola = dff_range.to_csv(index=False, encoding='utf-8')
    csv_string_vola = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_vola)

    return fig_yahoo_vola, csv_string_vola


# volume

@ app.callback(
    [Output(component_id="volume_graph", component_property="figure"),
     Output(component_id='download-link_yahoo_volume', component_property='href')],
    [Input(component_id='date-picker-range_vol', component_property='start_date'),
     Input(component_id='date-picker-range_vol',
           component_property='end_date'),
     Input(component_id="best_volume", component_property="value"),
     ]
)
def update_graph_volume(asset_selection, start, stop):

    df_volume = query_mongo(DB_NAME, "all_volume_y")
    dff_volume = df_volume.copy()

    # selecting start and stop
    dff_range = dff_volume.loc[dff_volume.Date.between(
        start, stop, inclusive=True)]
    dff_range.reset_index(drop=True, inplace=True)

    dff_vol_date = dff_range["Date"]

    dff_vol_filtered = dff_range[asset_selection]
    dff_vol_filtered["Date"] = dff_vol_date

    fig_volume = px.line(
        data_frame=dff_vol_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Best Performing Assets: Volume',
        labels={"value": "Volume (USD)",
                "variable": ""},
        color_discrete_map={
            "BTC": "#FEAF16",
            "TESLA": "#86CE00",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    csv_string_volume = dff_vol_filtered.to_csv(index=False, encoding='utf-8')
    csv_string_volume = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_volume)

    return fig_volume, csv_string_volume


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=False, port=5000, host='0.0.0.0')
