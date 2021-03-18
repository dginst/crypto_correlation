import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from btc_analysis.config import DB_NAME, YAHOO_TO_CAPM
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


# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Capital Asset Pricing Model",
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


                                        dcc.Graph(
                                            id='my_area_chart', figure={}),

                                    ])

                                ]),

                            ]),
                    ],
                    style={"width": "70rem"},
                    className="mt-3"
                )

            ]),

            dbc.Row([
                dbc.Col([

                    dbc.Card(
                        [
                            dbc.CardBody(
                                [

                                    dbc.Row([

                                        dbc.Col([


                                            dcc.Graph(
                                                id='my_eff_frontier', figure={}),

                                        ])

                                    ]),

                                ]),
                        ],
                        style={"width": "70rem"},
                        className="mt-3"
                    )

                ]),


    dcc.Interval(id='update', n_intervals=0, interval=1000 * 5),

    dcc.Interval(id='yahoo-update', interval=100000, n_intervals=0)
])

# --------------------------
# Callbacks part


@ app.callback(
    Output(component_id='my_area_chart', component_property='figure'),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def update_area_chart(n):

    CAPM_df=query_mongo(DB_NAME, "CAPM")

    CAPM_dff=CAPM_df.copy()
    CAPM_dff=CAPM_dff.drop(columns=["Return"])

    fig_area=px.area(
        data_frame=CAPM_dff,
        x="Volatility",
        y=YAHOO_TO_CAPM,
        template='plotly_dark',
        title='CAPM',
        labels={"value": "weights"},
        color_discrete_map={
            "BTC": "#FEAF16",
            "S&P500": "#511CFB",
            "CRUDE OIL": "#663300",
            "TESLA": "#86CE00",
            "US index": "#FBE426",
            "US_TREASURY": "#A777F1",
            "AMAZON": "#F58518",
            "APPLE": "#BAB0AC",
            "NETFLIX": "#FD3216",
        }
    )

    return fig_area


@ app.callback(
    Output(component_id='my_eff_frontier', component_property='figure'),
    Input(component_id="yahoo-update", component_property="n_intervals")
)
def update_eff_frontier(n):

    CAPM_df=query_mongo(DB_NAME, "CAPM")
    CAMP_no_df=query_mongo(DB_NAME, "CAPM_no_BTC")

    CAPM_dff=CAPM_df.copy()
    CPAM_no_dff=CAMP_no_df.copy()

    CAPM_dff_eff=CAPM_dff[["Return", "Volatility"]]

    CAPM_no_dff_eff=CPAM_no_dff[["Return", "Volatility"]]

    # Create figure with secondary y-axis
    fig=make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=CAPM_dff_eff["Volatility"],
                   y=CAPM_dff_eff["Return"],
                   name="Efficient Frontier w BTC",
                   mode='lines',
                   line_color='#ED7014'
                   ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=CAPM_no_dff_eff["Volatility"],
                   y=CAPM_no_dff_eff["Return"],
                   name="Efficient Frontier w/out BTC",
                   mode='lines',
                   line_color='#028A0F'),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Efficient Frontier",
        template='plotly_dark'
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Volatility",
                     range=[0, 0.3])

    # Set y-axes titles
    fig.update_yaxes(title_text="Return",
                     secondary_y=False,
                     range=[-0.1, 0.5])
    fig.update_yaxes(
        title_text="Return", secondary_y=True, range=[-0.1, 0.5])

    return fig


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=5500, host='0.0.0.0')
