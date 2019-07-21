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

df_popular_songs = pd.read_csv("./data/data_countries2/NonEnglish_PopularSongs.csv")

layout = [
    html.Div([
        html.Div([
            html.P('Audio Features Comparison')
        ], style={'text-align': 'center', 'font-size': 20}),

        dcc.Dropdown(
            id='attr-dropdown-bubble-y',
            options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness', 'valence', 'liveness', 'energy', 'danceability']],
            value="acousticness",
            multi=False
        ),
        dcc.Dropdown(
            id='attr-dropdown-bubble-x',
            options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness', 'valence', 'liveness', 'energy', 'danceability']],
            value="speechiness",
            multi=False
        ),
        dcc.RadioItems(
            id='attr-radio-bubble',
            options=[
                {'label': 'Language', 'value': 'Language'},
                {'label': 'Genre', 'value': 'Genre'}
            ],
            value='Language'
        )
    ], style={'background-color': 'white'}),

    html.Div(children=[
        dcc.Graph(id='bubble-charts-with-dropdown')
    ]),
]


def update_bubble(x, y, z):
    data = []
    color = {
        'Spanish': 'lightblue', 'French': 'orange', 'Korean': 'red', 'Turkish': 'green', 'Italian': 'yellow',
        'German': 'grey',
        'Latin Pop': 'darkred', 'Hip Hop': 'black', 'Reggaeton': 'green', 'K-pop': 'violet', 'R&B': 'blue',
        'Folk': 'yellow',
        'Bachata': 'orange', 'Electronic': 'cyan', 'Dance': 'lightpink', 'Dancehall': 'pink',
        'Latin Urban': 'orangered',
        'Latin Trap': 'red', 'Romantic': 'maroon', 'Pop': 'lightblue'
    }
    categories = df_popular_songs[z].unique()
    for v in categories:
        is_category = df_popular_songs[z] == v
        size = [v for v in df_popular_songs[is_category]['Popularity']]
        datapoint = go.Scatter(
            x=[v for v in df_popular_songs[is_category][x]],
            y=[v for v in df_popular_songs[is_category][y]],
            text=["Popularity: " + str(v) for v in size],
            mode='markers',
            name=v,
            marker=dict(
                size=size,
                color=[color[v] for v in df_popular_songs[is_category][z]],
                sizemode='area',
                sizeref=2. * max(size) / (40. ** 2),
                sizemin=4
            )
        )
        data.append(datapoint)
    return {
        'data': data,
        'layout': go.Layout(
            title=x + " v. " + y + " (with popularity)",
            xaxis=dict(
                title=x,
                gridcolor='rgb(255, 255, 255)',
                type='log',
                zerolinewidth=1,
                ticklen=5,
                gridwidth=2,
            ),
            yaxis=dict(
                title=y,
                gridcolor='rgb(255, 255, 255)',
                zerolinewidth=1,
                ticklen=5,
                gridwidth=2,
            )
        )
    }
