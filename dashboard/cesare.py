import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# ------------------------------
# start app


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ----------------
# app layout: bootstrap

app.layout = dbc.Container([

    # create as much rows and columns as needed foe the dashboard
    dbc.Row([
        dbc.Col(html.H1("Brero's Caesar Decrypter",
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

                                        html.I(
                                            "Type the encrypted message and the supposed key (an integer)"),
                                        html.Br(),
                                        dcc.Input(
                                            id="message",
                                            type="text",
                                            placeholder="Insert the message",
                                            value=''
                                        ),
                                        dcc.Input(id="key",
                                                  placeholder="Insert the key",
                                                  type='number',
                                                  value=0),
                                        html.Br(),
                                        # html.Div(id="result"),
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
                                dbc.Row([
                                    dbc.Col([

                                        html.Div(id="result"),
                                    ])

                                ]),
                            ]),
                    ],
                    style={"width": "70rem"},
                    className="mt-3"
                )

            ]),

            ], justify='center'),

])

# --------------------------
# Callbacks part


# btc denominated altcoin callback

# dropdown can be unified putting the same ID into the Input of each callback,
# NB: the dropdpwn display should be, at that point, disabled except for the
# first one
# naming has to be commented in the layout part for the second and third graph

@app.callback(
    Output("result", "children"),
    [
        Input("message", "value"),
        Input("key", "value"),
    ]
)
def update_output(mess, key_):

    translated = ''

    for symbol in mess:

        if symbol in LETTERS:

            num = LETTERS.find(symbol)
            num = num - key_

            if num < 0:

                num = num + len(LETTERS)

            translated = translated + LETTERS[num]
        else:

            translated = translated + symbol

    return "The message decrypted is: {}".format(translated)


print("Done")
# --------------------
if __name__ == '__main__':
    app.run_server(debug=False, port=9000, host='0.0.0.0')
