#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:43:58 2019

@author: Esuberante
"""

import dash_core_components as dcc
import dash_html_components as html

import numpy as np

import pandas as pd
import plotly.graph_objs as go

df_neng = pd.read_csv("./data/data_countries2/NonEnglish_PopularSongs.csv")

features = {'Acousticness': 'acousticness', 'Danceability': 'danceability', 'Energy': 'energy', 'Liveness': 'liveness',
            'Valence': 'valence', 'Speechiness': 'speechiness', 'Tempo': 'tempo_normalised',
            'Instrumentalness': 'instrumentalness'}

N = 10
c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]
data = [
    {
        'x': k,
        #        print(df_neng[features[k]])
        'y': df_neng[features[k]],
        'name': k,
        'marker': {
            'color': c[i]
        },
        "type": "box",
    } for i, (k, v) in enumerate(features.items())]

layout = [
        dcc.Graph(
            id='example-graph',
            figure={
                'data': data,
                'layout': go.Layout(
                    xaxis={'showgrid': False, 'zeroline': False, 'tickangle': 60, 'showticklabels': False},
                    yaxis={'showgrid': True, 'zeroline': False, 'gridcolor': 'rgb(233,233,233)',
                           'range': [0, 1]},
                    title={'text': 'Audio Features Analysis', 'font': {'size': 20}}
                    )
            }
        )
]

# app.layout = html.Div([
#    dcc.Graph(id='graph-with-radio'),
# ])
#
# @app.callback(
#    Output('graph-with-radio', 'figure'),
#    )
# def update_figure():
#    N = 10 
#    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
#    data = [
#    {
#        'x': k,
##        print(df_neng[features[k]])
#        'y': df_neng[features[k]],
#        'name':k,
#        'marker': {
#            'color': c[i]
#        },
#        "type": "box",
#    } for i,(k,v) in enumerate(features.items())]    
#
#    return {
#        'data': data,
#        'layout': go.Layout(xaxis = {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
#          yaxis = {'showgrid':True,'zeroline':False,'gridcolor':'rgb(233,233,233)', 'range': [0, 1]},
#        )
#    }

# if __name__ == '__main__':
#    app.run_server(debug=True)
#    update_figure()
