from btc_analysis.mongo_func import (
    query_mongo
)
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

connection = MongoClient("3.138.244.245", 27017)


def query_mongo_x(database, collection, query_dict=None):

    # defining the variable that allows to work with MongoDB
    db = connection[database]
    coll = db[collection]
    if query_dict is None:

        df = pd.DataFrame(list(coll.find()))

        try:

            df = df.drop(columns="_id")

        except AttributeError:

            df = []

        except KeyError:

            df = []

    else:

        df = pd.DataFrame(list(coll.find(query_dict)))

        try:

            df = df.drop(columns="_id")

        except AttributeError:

            df = []

        except KeyError:

            df = []

    return df

# start app


app = dash.Dash(__name__)
# -------------------
# Data
df = query_mongo_x("index", "index_level_1000")
df["Year"] = df['Date'].str[:4]
df = df.drop(columns="Time")
y_list = list(pd.unique(df["Year"]))
y_list = [int(y) for y in y_list]
df["Year"] = [int(y) for y in df["Year"]]

df_weight = query_mongo_x("index", "index_weights")
last_row_date = np.array(df_weight.tail(1)["Date"])[0]
print(last_row_date)
df_weight = df_weight.drop(columns=["Time"])
df_no_time = df_weight.drop(columns="Date")
print(df_no_time)
col_list = list(df_no_time.columns)
print(df_weight)
# ----------------
# app layout


app.layout = html.Div(children=[

    html.Div([
        html.H1("Crypto Index", style={"text-align": "center"}),

        dcc.RangeSlider(
            id="slct_years",
            marks={int(i): ' {}'.format(i) for i in y_list},
            min=y_list[0],
            max=y_list[len(y_list)-1],
            value=[2017, 2018, 2019, 2020, 2021]
        ),

        html.Div(id="out_cont", children=[]),

        html.Br(),


        dcc.Graph(id="my_index_level", figure={}),
    ]),

    html.Div([
        html.H1("Weight", style={"text-align": "center"}),

        html.Div([
            html.Label(['Period']),

            dcc.Dropdown(
                id='my_dropdown',
                # options=[
                #     {'label': str(last_row_date), 'value': col_list}
                # ],
                multi=False,
                value=str(last_row_date),
                style={"width": "50%"},
                clearable=False
            ),


            dcc.Graph(id='my_weight_pie')
        ])
    ]),

    # dcc.Graph(id='my_weight_pie', figure=pie_fig)

])


# --------------------
# connect the plotly graph with Dash comp

@ app.callback(
    [
        Output(component_id="out_cont", component_property="children"),
        Output(component_id="my_index_level", component_property="figure"),
        Output(component_id="my_weight_pie", component_property="figure")
    ],
    [Input(component_id="slct_years", component_property="value"),
     Input(component_id="my_dropdown", component_property="value")]
)
def update_graph(option_slct, my_dropdown):

    container = "The selected years are: {}".format(option_slct)

    dff = df.copy()
    dff_filtered = pd.DataFrame(columns=dff.columns)
    for y in option_slct:

        df_v = dff.loc[dff["Year"] == y]
        dff_filtered = dff_filtered.append(df_v)

    fig = px.line(
        data_frame=dff_filtered,
        x="Date",
        y="Index Value",
        template='plotly_dark'

    )
    dff_w = df_weight.copy()
    dff_w_filt = dff_w.loc[dff_w["Date"] == my_dropdown]
    print(dff_w_filt)
    dff_w_filt = dff_w_filt.drop(columns="Date")
    pie_fig = px.pie(
        data_frame=dff_w_filt,
        # names=my_dropdown,
        hole=.3
    )

    print("H")
    return container, fig, pie_fig


# --------------------
if __name__ == '__main__':
    app.run_server(debug=True)
