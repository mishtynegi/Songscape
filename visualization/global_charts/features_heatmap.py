#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:38:32 2019

@author: Esuberante
"""

import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objs as go

df_all = pd.read_csv("./data/audio_feature.csv")

layout = html.Div([
    dcc.Graph(id='heatmap-all-songs',
              figure={
                  'layout': {'title': 'Audio Features Heatmap'},
                  'data': [go.Heatmap(
                      z=[row for row in df_all.drop(
                          columns=['id', 'key', 'loudness', 'mode', 'time_signature',
                                   'popularity', 'genre', 'rank']).corr().values],
                      x=[k for k in df_all.drop(
                          columns=['id', 'key', 'loudness', 'mode', 'time_signature',
                                   'popularity', 'genre', 'rank']).columns],
                      y=[k for k in df_all.drop(
                          columns=['id', 'key', 'loudness', 'mode', 'time_signature',
                                   'popularity', 'genre', 'rank']).columns],
                      colorscale='YlGnBu'
                  )]
              }
              )
])
