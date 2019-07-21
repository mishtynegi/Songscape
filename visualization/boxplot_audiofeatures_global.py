#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:38:32 2019

@author: Esuberante
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.plotly as py

import pandas as pd
import plotly.graph_objs as go

df_global = pd.read_csv("./data/data_countries/Global.csv")
df_usa = pd.read_csv("./data/data_countries/USA.csv")
df_canada = pd.read_csv("./data/data_countries/Canada.csv")
df_brazil = pd.read_csv("./data/data_countries/Brazil.csv")
df_columbia = pd.read_csv("./data/data_countries/Columbia.csv")
df_argentina = pd.read_csv("./data/data_countries/Argentina.csv")
df_denmark = pd.read_csv("./data/data_countries/Denmark.csv")
df_germany = pd.read_csv("./data/data_countries/Germany.csv")
df_france = pd.read_csv("./data/data_countries/France.csv")
df_italy = pd.read_csv("./data/data_countries/Italy.csv")
df_israel = pd.read_csv("./data/data_countries/Israel.csv")
df_turkey = pd.read_csv("./data/data_countries/Turkey.csv")
df_newz = pd.read_csv("./data/data_countries/Newzealand.csv")
df_australia = pd.read_csv("./data/data_countries/Australia.csv")
df_austria = pd.read_csv("./data/data_countries/Austria.csv")
df_ph = pd.read_csv("./data/data_countries/Philippines.csv")
df_indonesia = pd.read_csv("./data/data_countries/Indonesia.csv")
df_bharat = pd.read_csv("./data/data_countries/India.csv")
df_hk = pd.read_csv("./data/data_countries/HongKong.csv")
df_japan = pd.read_csv("./data/data_countries/Japan.csv")
df_poland = pd.read_csv("./data/data_countries/Poland.csv")
df_sg = pd.read_csv("./data/data_countries/Singapore.csv")
df_sw = pd.read_csv("./data/data_countries/Switzerland.csv")
df_spain = pd.read_csv("./data/data_countries/Spain.csv")
df_uk = pd.read_csv("./data/data_countries/UnitedKingdom.csv")

# print(df_global.columns)
# print(df_usa.columns)
# print(df_canada.columns)
# print(df_brazil.columns)
# print(df_columbia.columns)
# print(df_argentina.columns)
# print(df_denmark.columns)
# print(df_germany.columns)
# print(df_france.columns)
# print(df_italy.columns)
# print(df_israel.columns)
# print(df_turkey.columns)
# print(df_newz.columns)
# print(df_australia.columns)
# print(df_austria.columns)
# print(df_ph.columns)
# print(df_indonesia.columns)
# print(df_bharat.columns)
# print(df_hk.columns)
# print(df_japan.columns)
# print(df_poland.columns)
# print(df_sg.columns)
# print(df_sw.columns)
# print(df_spain.columns)
# print(df_uk.columns)

countries = {"Global": df_global, "USA": df_usa, "Brazil": df_brazil, "Columbia": df_columbia,
             "Argentina": df_argentina, "Denmark": df_denmark,
             "Germany": df_germany, "France": df_france, "Italy": df_italy, "Israel": df_israel, "Turkey": df_turkey,
             "New Zealand": df_newz, "Australia": df_australia, "Austria": df_austria, "Philippines": df_ph,
             "Indonesia": df_indonesia, "India": df_bharat, "Hong Kong": df_hk, "Japan": df_japan, "Canada": df_canada,
             "Poland": df_poland, "Singapore": df_sg, "Switzerland": df_sw, "Spain": df_spain, "UK": df_uk}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

audio_feature_box_plot = html.Div([
    html.Div([
        html.P('Audio Features Comparison')
    ], style={'text-align': 'center', 'font-size': 20}),
    dcc.Graph(id='graph-with-radio'),
    dcc.RadioItems(
        id='radio-items',
        options=[
            {'label': 'Acousticness', 'value': 'acousticness'},
            {'label': 'Danceability', 'value': 'danceability'},
            {'label': 'Valence', 'value': 'valence'},
            {'label': 'Instrumentalness', 'value': 'instrumentalness'},
            {'label': 'Speechiness', 'value': 'speechiness'},
            {'label': 'Liveness', 'value': 'liveness'},
            {'label': 'Energy', 'value': 'energy'},
            {'label': 'Tempo', 'value': 'tempo_normalised'},
        ],
        value='acousticness',
        labelStyle={'display': 'inline-block'},
        inputStyle={"margin-left": "20px"}

    ),
], style={'background-color': 'white'})

layout = html.Div([
    html.Div([
        html.P('Audio Features Comparison')
    ], style={'text-align': 'center', 'font-size': 20}),
    dcc.Graph(id='graph-with-radio'),
    dcc.RadioItems(
        id='radio-items',
        options=[
            {'label': 'Acousticness', 'value': 'acousticness'},
            {'label': 'Danceability', 'value': 'danceability'},
            {'label': 'Valence', 'value': 'valence'},
            {'label': 'Instrumentalness', 'value': 'instrumentalness'},
            {'label': 'Speechiness', 'value': 'speechiness'},
            {'label': 'Liveness', 'value': 'liveness'},
            {'label': 'Energy', 'value': 'energy'},
            {'label': 'Tempo', 'value': 'tempo_normalised'},
        ],
        value='acousticness',
        labelStyle={'display': 'inline-block'},
        inputStyle={"margin-left": "20px"}

    ),
], style={'background-color': 'white'})


def update_figure(selected_feature):
    N = 25
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]
    data = [
        {
            'x': k,
            'y': v[selected_feature].tolist(),
            'name': k,
            'marker': {
                'color': c[i]
            },
            "type": "box",
        } for i, (k, v) in enumerate(countries.items())]
    # print(data)

    return {
        'data': data,
        'layout': go.Layout(xaxis={'showgrid': False, 'zeroline': False, 'tickangle': 60, 'showticklabels': False},
                            yaxis={'showgrid': True, 'zeroline': False, 'gridcolor': 'rgb(233,233,233)',
                                   'range': [0, 1]},
                            )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
