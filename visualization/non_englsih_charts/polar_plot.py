#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 04:17:48 2019

@author: Esuberante
"""

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:38:32 2019

@author: Esuberante
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from collections import defaultdict

df_popular_songs = pd.read_csv("./data/data_countries2/NonEnglish_PopularSongs.csv")

attributes_lang = {"Spanish": 'Spanish', "German": 'German', "Korean": 'Korean', "Italian": 'Italian'}
attributes_genre = {"Bachata": 'Bachata', "Dance": 'Dance', "Dancehall": 'Dancehall', "Folk": 'Folk',
                    "Hip Hop": 'Hip Hop',
                    "K-pop": 'K-pop', "Latin Pop": 'Latin Pop', "Latin Trap": 'Latin Trap', "Pop": 'Pop',
                    "R&B": 'R&B', "Reggaeton": 'Reggaeton', "Romantic": 'Romantic'}

color = {'Spanish': 'lightblue', 'French': 'orange', 'Korean': 'red', 'Turkish': 'green', 'Italian': 'yellow',
         'German': 'grey',
         'Latin Pop': 'darkred', 'Hip Hop': 'black', 'Reggaeton': 'green', 'K-pop': 'violet', 'R&B': 'blue',
         'Folk': 'yellow',
         'Bachata': 'orange', 'Electronic': 'cyan', 'Dance': 'lightpink', 'Dancehall': 'pink',
         'Latin Urban': 'orangered',
         'Latin Trap': 'red', 'Romantic': 'maroon', 'Pop': 'lightblue'}

common_songs = defaultdict(dict)

c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, 24)]

# for k,v in countries.items():
#    for k1,v1 in countries.items():
#        common_songs[k][k1] = v.merge(v1, on='id').shape[0]


layout = [
    dcc.Graph(id='graph-with-dropdown2'),
    dcc.Dropdown(
        id='lang-dropdown',
        options=[{'label': k, 'value': k} for k in attributes_lang],
        value=["Spanish"],
        multi=True
    ),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': k, 'value': k} for k in attributes_genre],
        value=["R&B"],
        multi=True
    )
]


def update_figure(languages, genres):
    data = []
    for language in languages:
        is_language = df_popular_songs['Language'] == language
        df_selection = df_popular_songs[is_language][
            ['acousticness', 'danceability', 'energy', 'liveness', 'valence', 'speechiness', 'tempo_normalised']]
        datapoint = go.Scatterpolar(
            theta=['Acousticness', 'Danceability', 'Energy', 'Liveness', 'Valence', 'Speechiness', 'Tempo'],
            name=language,
            r=[df_selection[column].mean() for column in df_selection],
            fill="toself",
            line=dict(color=color[language])
        )
        data.append(datapoint)
    for genre in genres:
        is_genre = df_popular_songs['Genre'] == genre
        df_selection = df_popular_songs[is_genre][
            ['acousticness', 'danceability', 'energy', 'liveness', 'valence', 'speechiness', 'tempo_normalised']]
        datapoint = go.Scatterpolar(
            theta=['Acousticness', 'Danceability', 'Energy', 'Liveness', 'Valence', 'Speechiness', 'Tempo'],
            name=genre,
            r=[df_selection[column].mean() for column in df_selection],
            fill="toself",
            line=dict(color=color[genre])

        )
        data.append(datapoint)
    # print(data)
    return {
        'data': data,
        'layout': go.Layout(
            title={'text': 'Audio Features by Language and Genre', 'font': {'size': 20}},
            legend=dict(orientation="h"),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                ),
            ),
        )
    }
