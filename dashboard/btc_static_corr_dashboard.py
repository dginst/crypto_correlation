import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from btc_analysis.config import DB_NAME, STATIC_COLORSCALE
from btc_analysis.dashboard_func import static_corr_df
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
                                            id='my_static_dropdown',
                                            options=[
                                                {'label': w, 'value': w} for w in window_list
                                            ],
                                            multi=False,
                                            value="3Y",
                                            style={"width": "50%"},
                                            clearable=False
                                        ),

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


@ app.callback(
    [Output(component_id="my_corr_heatmap", component_property="figure"),
     Output(component_id='download-link_static', component_property='href')],
    Input(component_id="my_static_dropdown", component_property="value")
)
def update_graph_vola(window_selection):

    df_static = static_corr_df(window_list)

    dff_static = df_static.copy()

    dff_window = dff_static.loc[dff_static.Window == window_selection]
    dff_window = dff_window.drop(columns=["Window"])

    N = 17
    corr_mat = [[dff_window.iloc[i, j] if i >= j else None for j in range(N)]
                for i in range(N)]

    hovertext = [[f'corr_mat({column_set[i]}, {column_set[j]})= {corr_mat[i][j]:.2f}' if i >=
                  j else '' for j in range(N)] for i in range(N)]
    print(hovertext)
    heat = go.Heatmap(z=corr_mat,
                      x=column_set,
                      y=column_set,
                      xgap=2, ygap=2,
                      colorscale=STATIC_COLORSCALE,
                      colorbar_thickness=20,
                      colorbar_ticklen=4,
                      hovertext=hovertext,

                      hoverinfo='text'
                      )

    title = 'Correlation Matrix'

    layout = go.Layout(title_text=title, title_x=0.5,
                       width=1000, height=1000,
                       xaxis_showgrid=False,
                       yaxis_showgrid=False,
                       yaxis_autorange='reversed',
                       template='plotly_dark')

    fig = go.Figure(data=[heat], layout=layout)
    fig.update_traces(text=corr_mat, selector=dict(type='heatmap'))

    csv_string_static = dff_window.to_csv(index=False, encoding='utf-8')
    csv_string_static = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string_static)

    return fig, csv_string_static


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=False, port=9000, host='0.0.0.0')
