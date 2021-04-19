import urllib.parse
from datetime import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from btc_analysis.calc import last_quarter_end
from btc_analysis.config import DB_NAME, STATIC_COLORSCALE
from btc_analysis.dashboard_func import static_corr_df
from btc_analysis.market_data import yesterday_str
from btc_analysis.mongo_func import query_mongo
from dash.dependencies import Input, Output

pio.templates.default = "none"

stat_corr = query_mongo(DB_NAME, "stat_yahoo_correlation_1M")

column_set = list(stat_corr.columns)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# -------------------
# Data

window_list = ["all", "3Y", "1Y", "1Q", "1M"]

yesterday = yesterday_str()
last_quarter_ = last_quarter_end()
last_quarter = datetime.strptime(
    last_quarter_, "%d-%m-%Y").strftime("%Y-%m-%d")

as_of_list = [yesterday, last_quarter_]

all_options = {

    'all': [yesterday, last_quarter_],
    '3Y': [yesterday, last_quarter_],
    '1Y': [yesterday, last_quarter_],
    '1Q': [yesterday, last_quarter_],
    '1M': [yesterday, last_quarter_],

}


# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Static Correlation Dashboard",
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

                                        html.Label(['Correlation Window']),

                                        dcc.Dropdown(
                                            id='corr_static_dropdown',
                                            options=[
                                                {'label': w, 'value': w} for w in all_options.keys()
                                            ],
                                            multi=False,
                                            value="3Y",
                                            style={"width": "50%"},
                                            clearable=False
                                        ),

                                        html.Hr(),

                                        html.Label(['As of:']),

                                        dcc.Dropdown(id='as_of_dropdown',
                                                     style={"width": "50%"},
                                                     ),

                                        html.Hr(),

                                        dcc.Graph(
                                            id='my_corr_heatmap', figure={}),

                                        html.A(
                                            'Download Data',
                                            id='download-link_static',
                                            download="static_corr.csv",
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


@app.callback(
    Output(component_id='as_of_dropdown', component_property='options'),
    Input(component_id="corr_static_dropdown", component_property="value")
)
def set_as_of_option(selected_time_window):

    yesterday = yesterday_str()
    last_quarter_ = last_quarter_end()

    all_options = {

        'all': [yesterday, last_quarter_],
        '3Y': [yesterday, last_quarter_],
        '1Y': [yesterday, last_quarter_],
        '1Q': [yesterday, last_quarter_],
        '1M': [yesterday, last_quarter_],

    }

    return [{'label': i, 'value': i} for i in all_options[selected_time_window]]


@app.callback(
    Output(component_id="as_of_dropdown", component_property="value"),
    Input(component_id="as_of_dropdown", component_property="options")
)
def set_as_of_value(available_options):

    return available_options[0]['value']


@ app.callback(
    [Output(component_id="my_corr_heatmap", component_property="figure"),
     Output(component_id='download-link_static', component_property='href')],
    [Input(component_id="corr_static_dropdown", component_property="value"),
     Input(component_id="as_of_dropdown", component_property="value"),
     Input(component_id="yahoo-update", component_property="n_intervals")]
)
def update_corr_matrix(window_selection, as_of_selection, n_intervals):

    df_static = query_mongo(DB_NAME, "dash_static_corr")

    dff_static = df_static.copy()

    # window selection
    dff_window = dff_static.loc[dff_static.Window == window_selection]
    dff_window = dff_window.drop(columns=["Window"])

    # as of selection
    dff_corr_as_of = dff_window.loc[dff_window["As Of"] == as_of_selection]
    dff_corr_as_of = dff_corr_as_of.drop(columns=["As Of"])

    N = len(list(dff_corr_as_of.columns)) - 1

    corr_mat = [[dff_corr_as_of.iloc[i, j] if i >= j else None for j in range(N)]
                for i in range(N)]

    hovertext = [[f'corr_mat({column_set[i]}, {column_set[j]})= {corr_mat[i][j]:.2f}' if i >=
                  j else '' for j in range(N)] for i in range(N)]

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(z=corr_mat,
                   x=column_set,
                   y=column_set,
                   xgap=2,
                   ygap=2,
                   zmin=-1,
                   zmax=1,
                   colorscale=STATIC_COLORSCALE,
                   colorbar_thickness=20,
                   colorbar_ticklen=4,
                   hovertext=hovertext,
                   hoverinfo='text'
                   )
    )

    fig.add_trace(
        go.Scatter(xaxis='x2',
                   yaxis='y2'
                   )
    )

    fig.add_trace(
        go.Scatter(xaxis='x3',
                   yaxis='y3'
                   )
    )

    fig.add_trace(
        go.Scatter(xaxis='x4',
                   yaxis='y4'
                   )
    )

    fig.add_trace(
        go.Scatter(xaxis='x5',
                   yaxis='y5'
                   )
    )

    fig.update_layout(
        title_text='Correlation Matrix',
        title_x=0.5,
        width=1000,
        height=1000,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        yaxis_autorange='reversed',
        xaxis_autorange=True,
        template='plotly_dark'

    )
    fig.update_layout(
        xaxis=dict(
            range=[0, N],
            tickfont=dict(color="#FFA500"),
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['BTC', 'ETH', 'LTC', 'XRP'],
        ),
        xaxis2=dict(
            range=[0, N],
            tickfont=dict(color="#228B22"),
            tickmode='array',
            tickvals=[4.5, 5.5, 6.5, 7.5],
            ticktext=['GOLD', 'COPPER', 'CRUDE OIL', 'CORN'],
            overlaying="x",
            side="bottom",
        ),
        xaxis3=dict(
            range=[0, N],
            tickfont=dict(color="#4169E1"),
            tickmode='array',
            tickvals=[8.5, 9.5, 10.5, 11.5],
            ticktext=['EUR', 'GBP', 'JPY', 'CHF'],
            overlaying="x",
            side="bottom",
        ),
        xaxis4=dict(
            range=[0, N],
            tickfont=dict(color="#A9A9A9"),
            tickmode='array',
            tickvals=[12.5, 13.5, 14.5, 15.5],
            ticktext=['NASDAQ', 'S&P500', 'EUROSTOXX50', 'VIX'],
            overlaying="x",
            side="bottom",
        ),
        xaxis5=dict(
            range=[0, N],
            tickfont=dict(color="#C0C0C0"),
            tickmode='array',
            tickvals=[16.5, 17.5],
            ticktext=['US TREASURY', 'PAN EUR'],
            overlaying="x",
            side="bottom",
        ),
        yaxis=dict(
            range=[0, N],
            tickfont=dict(color="#FFA500"),
            tickmode='array',
            tickvals=[17, 16, 15, 14],
            ticktext=['BTC', 'ETH', 'LTC', 'XRP'],
            # overlaying="y",
            side="bottom",

        ),
        yaxis2=dict(
            range=[0, N],
            tickfont=dict(color="#228B22"),
            tickmode='array',
            tickvals=[4.5, 5.5, 6.5, 7.5],
            ticktext=['GOLD', 'COPPER', 'CRUDE OIL', 'CORN'],
            overlaying="y",
            side="left",
        ),
        yaxis3=dict(
            range=[0, N],
            tickfont=dict(color="#4169E1"),
            tickmode='array',
            tickvals=[8.5, 9.5, 10.5, 11.5],
            ticktext=['EUR', 'GBP', 'JPY', 'CHF'],
            overlaying="y",
            side="bottom",
        ),
        yaxis4=dict(
            range=[0, N],
            tickfont=dict(color="#A9A9A9"),
            tickmode='array',
            tickvals=[12.5, 13.5, 14.5, 15.5],
            ticktext=['NASDAQ', 'S&P500', 'EUROSTOXX50', 'VIX'],
            overlaying="y",
            side="bottom",
        ),
        yaxis5=dict(
            range=[0, N],
            tickfont=dict(color="#C0C0C0"),
            tickmode='array',
            tickvals=[16.5, 17.5],
            ticktext=['US TREASURY', 'PAN EUR'],
            overlaying="y",
            side="bottom",
        ),
    )

    fig.update_traces(text=corr_mat, selector=dict(type='heatmap'))

    fig.update_yaxes(ticks="outside",
                     tickfont=dict(
                         family='Rockwell',
                         # color='crimson',
                         size=14)
                     )

    fig.update_xaxes(ticks="outside",
                     tickangle=45,
                     tickfont=dict(
                         family='Rockwell',
                         # color='crimson',
                         size=14)
                     )

    csv_string_static = dff_window.to_csv(index=False, encoding='utf-8')
    csv_string_static = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_static)

    return fig, csv_string_static


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=9000, host='0.0.0.0')
