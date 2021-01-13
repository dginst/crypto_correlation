import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import btc_corr, btc_den


app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Prices denominated in Bitcoin|', href='/apps/btc_den'),
        dcc.Link('Bitcoin correlations', href='/apps/btc_corr'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@ app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')]
               )
def display_page(pathname):

    if pathname == '/apps/btc_den':
        return btc_den.layout
    if pathname == '/apps/btc_corr':
        return btc_corr.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False, port=4500)
