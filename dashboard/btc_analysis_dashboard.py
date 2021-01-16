
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import urllib.parse
from btc_analysis.dashboard_func import (
    btc_total_dfs
)


# ------------------------------
# start app


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# -------------------
# Data

window_list = ["3Y", "1Y", "6M", "3M", "1M"]
df_alt, df_yahoo = btc_total_dfs(window_list, "btc_denominated")

df_alt_col = list(df_alt.columns)
df_alt_col.remove('Date')
df_alt_col.remove('Window')


df_yahoo = df_yahoo.drop(columns=["ETH", "XRP", "LTC", "BCH"])
df_yahoo = df_yahoo.rename(
    columns={'BBG Barclays PAN EURO Aggregate': 'Eur Aggregate Bond'})
df_col_yahoo = list(df_yahoo.columns)
df_col_yahoo.remove('Date')
df_col_yahoo.remove('Window')

# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("BTC analysis Dashboard",
                        className='text-center text-primary, mb-4'),
                width=12)

    ]),


    dbc.Row([
        dbc.Col([

            html.Label(['Time Window']),

            dcc.Dropdown(
                id='my_alt_dropdown',
                options=[
                    {'label': w, 'value': w} for w in window_list
                ],
                multi=False,
                value="3Y",
                style={"width": "50%"},
                clearable=False
            ),

            html.Label(['Crypto Assets']),
            dcc.Checklist(
                id='my_alt_check',
                options=[
                    {'label': x, 'value': x} for x in df_alt_col
                ],
                value=["BTC", "ETH", "XRP", "LTC", "BCH"],
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-right": "10px",
                            "margin-left": "10px"}
            ),


            dcc.Graph(id='my_multi_line', figure={}),

            html.A(
                'Download Data',
                id='download-link_alt',
                download="altcoin_rawdata.csv",
                href="",
                target="_blank"
            )
        ])

    ]),

    dbc.Row([
        dbc.Col([


            html.Label(['Time Window']),

            dcc.Dropdown(
                id='my_yahoo_dropdown',
                options=[
                    {'label': w, 'value': w} for w in window_list
                ],
                multi=False,
                value="3Y",
                style={"width": "50%"},
                clearable=False
            ),

            html.Label(['Assets']),

            dcc.Checklist(
                id='my_yahoo_check',
                options=[
                    {'label': x, 'value': x} for x in df_col_yahoo
                ],
                value=["BTC", "GOLD", "AMAZON", "TESLA"],
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-right": "10px",
                            "margin-left": "10px"}
            ),


            dcc.Graph(id='my_multi_line_2', figure={}),

            html.A(
                'Download Data',
                id='download-link_yahoo',
                download="yahoo_rawdata.csv",
                href="",
                target="_blank"
            )
        ])

    ]),
])

# --------------------------
# Callbacks part


# btc denominated altcoin callback


@ app.callback(
    Output(component_id="my_multi_line", component_property="figure"),
    [Input(component_id="my_alt_dropdown", component_property="value"),
     Input(component_id="my_alt_check", component_property="value"),
     ]
)
def update_graph_alt(window_selection, asset_selection):

    dff_alt = df_alt.copy()
    dff_w = dff_alt.loc[dff_alt.Window == window_selection]
    dff_w = dff_w.drop(columns=["Window"])
    dff_date = dff_w["Date"]
    dff_filtered = dff_w[asset_selection]
    dff_filtered["Date"] = dff_date

    fig_alt = px.line(
        data_frame=dff_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='Altcoin prices denominated in Bitcoin,
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

    return fig_alt


@app.callback(
    Output(component_id='download-link_alt', component_property='href'),
    Input(component_id='my_alt_dropdown', component_property='value')
)
def update_download_link_alt(window_selection):

    dff_alt_d = df_alt.copy()
    dff_w = dff_alt_d.loc[dff_alt_d.Window == window_selection]

    csv_string = dff_w.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string)

    return csv_string

# various asset btc den


@ app.callback(
    Output(component_id="my_multi_line_2", component_property="figure"),
    [Input(component_id="my_yahoo_dropdown", component_property="value"),
     Input(component_id="my_yahoo_check", component_property="value")]
)
def update_graph_yahoo(window_selection, asset_selection):

    dff_yahoo = df_yahoo.copy()
    dff_w = dff_yahoo.loc[dff_yahoo.Window == window_selection]
    dff_w = dff_w.drop(columns=["Window"])
    dff_date = dff_w["Date"]
    dff_filtered = dff_w[asset_selection]
    dff_filtered["Date"] = dff_date

    fig_yahoo = px.line(
        data_frame=dff_filtered,
        x="Date",
        y=asset_selection,
        template='plotly_dark',
        title='to be defined',
        color_discrete_map={
            "BTC": "#FEAF16",
            "S&P500": "#511CFB",
            "PETROL": "#222A2A",
            "SILVER": "#E2E2E2",
            "TESLA": "#86CE00",
            "US index": "#FBE426",
            "CORN": "#DA16FF",
            "NASDAQ": "#B68100",
            "VIX": "#00B5F7",
            "DOWJONES": "#750D86",
            "US_TREASURY": "#A777F1",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    return fig_yahoo


@app.callback(
    Output(component_id='download-link_yahoo', component_property='href'),
    Input(component_id='my_yahoo_dropdown', component_property='value')
)
def update_download_link_yahoo(window_selection):

    dff_y_d = df_yahoo.copy()
    dff_w = dff_y_d.loc[dff_y_d.Window == window_selection]

    csv_string = dff_w.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string)

    return csv_string


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=4000, host='0.0.0.0')
