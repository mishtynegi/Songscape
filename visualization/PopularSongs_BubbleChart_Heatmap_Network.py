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

import pandas as pd
import plotly.graph_objs as go

import networkx as nx
import numpy as np
import dash_cytoscape as cyto

from collections import defaultdict


df_usa = pd.read_csv("./data/data_countries2/USA.csv")
df_canada = pd.read_csv("./data/data_countries2/Canada.csv")
df_brazil = pd.read_csv("./data/data_countries2/Brazil.csv")
df_columbia = pd.read_csv("./data/data_countries2/Columbia.csv")
df_argentina = pd.read_csv("./data/data_countries2/Argentina.csv")
df_denmark = pd.read_csv("./data/data_countries2/Denmark.csv")
df_germany = pd.read_csv("./data/data_countries2/Germany.csv")
df_france = pd.read_csv("./data/data_countries2/France.csv")
df_italy = pd.read_csv("./data/data_countries2/Italy.csv")
df_israel = pd.read_csv("./data/data_countries2/Israel.csv")
df_turkey = pd.read_csv("./data/data_countries2/Turkey.csv")
df_newz = pd.read_csv("./data/data_countries2/Newzealand.csv")
df_australia = pd.read_csv("./data/data_countries2/Australia.csv")
df_austria = pd.read_csv("./data/data_countries2/Austria.csv")
df_ph = pd.read_csv("./data/data_countries2/Philippines.csv")
df_indonesia = pd.read_csv("./data/data_countries2/Indonesia.csv")
df_bharat = pd.read_csv("./data/data_countries2/India.csv")
df_hk = pd.read_csv("./data/data_countries2/HongKong.csv")
df_japan = pd.read_csv("./data/data_countries2/Japan.csv")
df_poland = pd.read_csv("./data/data_countries2/Poland.csv")
df_sg = pd.read_csv("./data/data_countries2/Singapore.csv")
df_sw = pd.read_csv("./data/data_countries2/Switzerland.csv")
df_spain = pd.read_csv("./data/data_countries2/Spain.csv")
df_uk = pd.read_csv("./data/data_countries2/UnitedKingdom.csv")
df_popular_songs = pd.read_csv("./data/data_countries2/NonEnglish_PopularSongs.csv")

# print (df_global.columns)
# print (df_usa.columns)
# print (df_canada.columns)
# print (df_brazil.columns)
# print (df_columbia.columns)
# print (df_argentina.columns)
# print (df_denmark.columns)
# print (df_germany.columns)
# print (df_france.columns)
# print (df_italy.columns)
# print (df_israel.columns)
# print (df_turkey.columns)
# print (df_newz.columns)
# print (df_australia.columns)
# print (df_austria.columns)
# print (df_ph.columns)
# print (df_indonesia.columns)
# print (df_bharat.columns)
# print (df_hk.columns)
# print (df_japan.columns)
# print (df_poland.columns)
# print (df_sg.columns)
# print (df_sw.columns)
# print (df_spain.columns)
# print (df_uk.columns)


c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, 24)]

countries = {"USA": df_usa, "Brazil": df_brazil, "Columbia": df_columbia, "Argentina": df_argentina, "Denmark": df_denmark,
             "Germany": df_germany, "France": df_france, "Italy": df_italy, "Israel": df_israel, "Turkey": df_turkey,
             "New Zealand": df_newz, "Australia": df_australia, "Austria": df_austria, "Philippines": df_ph,
             "Indonesia": df_indonesia, "India": df_bharat, "Hong Kong": df_hk, "Japan": df_japan, "Canada": df_canada,
             "Poland": df_poland, "Singapore": df_sg, "Switzerland": df_sw, "Spain": df_spain, "UK": df_uk}

common_songs = defaultdict(dict)

for k,v in countries.items():
    for k1,v1 in countries.items():
        common_songs[k][k1] = pd.merge(v, v1, how='inner', on='id').shape[0]

def generate_network_data():
    g = nx.Graph()

    edge_list = []
    node_list = []

    # nodes
    g.add_nodes_from([k for k in common_songs])
    for k,v in common_songs.items():
        for k1,v1 in v.items():
            if k != k1:
                g.add_edge(k, k1, weight=v1)
                edge_list.append({'data': {'source': k, 'target': k1, 'weight': v1/10}})

                
    pos = nx.kamada_kawai_layout(g, scale=600)

    for i,x in enumerate(list(g.nodes)):
        node_list.append({'data': {'id': x, 'label': x, 'weight': sum([v for k,v in common_songs[x].items()])/5},
                          'position': {'x': pos[x][0], 'y':  pos[x][1]},
                          'style': {'background-color': c[i]}})
    node_list.extend(edge_list)

    return node_list

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


heatmap = html.Div(children=[
    dcc.Graph(id='heatmap-popular-songs',
        figure={
            'data': [go.Heatmap(
                z=[list(v.values()) for k,v in common_songs.items()],
                x=[k for k in common_songs],
                y=[k for k in common_songs],
                colorscale='Viridis'
            )]
        }
    )
])
network_popular_songs = html.Div(children=[
    html.Div([
            html.P('Countries Network by Common Songs')
        ], style={'text-align': 'center', 'font-size': 20}),
    cyto.Cytoscape(
    id='network-popular-songs',
    layout={'name': 'preset'},
    style={'width': '100%', 'height': '800px'},
    elements= generate_network_data(),
    stylesheet=[
        {
            'selector': 'edge',
            'style': {
                'width': 'data(weight)'
            }
        },
        {
            'selector': 'node',
            'style': {
                'width': 'data(weight)',
                'height': 'data(weight)',
                'label': 'data(label)',
                'labelsize': '20'
            }
        }
    ]
    )
], style={'background-color': 'white'}),

bubble_charts_with_dropdown = html.Div(children=[
    dcc.Graph(id='bubble-charts-with-dropdown'),
    dcc.Dropdown(
        id='attr-dropdown-bubble-x',
        options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness']],
        value="speechiness",
        multi=False
    ),
    dcc.Dropdown(
        id='attr-dropdown-bubble-y',
        options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness']],
        value="acousticness",
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
])



app.layout = html.Div([
    # html.Div(children=[
    #     dcc.Graph(id='polar-graph-with-dropdown'),
    #     dcc.Dropdown(
    #         id='year-dropdown-polar',
    #         options=[{'label': k, 'value': k} for k in countries],
    #         value=["USA"],
    #         multi=True

    #     )
    # ]),
    html.Div(children=[
        dcc.Graph(id='heatmap-popular-songs',
            figure={
                'data': [go.Heatmap(
                    z=[list(v.values()) for k,v in common_songs.items()],
                    x=[k for k in common_songs],
                    y=[k for k in common_songs],
                    colorscale='Viridis'
                )]
            }
        )
    ]),
    html.Div(children=[
        cyto.Cytoscape(
            id='network-popular-songs',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '800px'},
            elements= generate_network_data(),
            stylesheet=[
                {
                    'selector': 'edge',
                    'style': {
                        'width': 'data(weight)'
                    }
                },
                {
                    'selector': 'node',
                    'style': {
                        'width': 'data(weight)',
                        'height': 'data(weight)',
                        'label': 'data(label)',
                        'labelsize': '20'
                    }
                }
            ]
        )
    ]),
    html.Div(children=[
        dcc.Graph(id='bubble-charts-with-dropdown'),
        dcc.Dropdown(
            id='attr-dropdown-bubble-x',
            options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness']],
            value="speechiness",
            multi=False
        ),
        dcc.Dropdown(
            id='attr-dropdown-bubble-y',
            options=[{'label': k, 'value': k} for k in ['acousticness', 'tempo', 'speechiness']],
            value="acousticness",
            multi=False
        ),
        # dcc.RadioItems(
        #     id='attr-radio-bubble',
        #     options=[
        #         {'label': 'Language', 'value': 'Language'},
        #         {'label': 'Genre', 'value': 'Genre'}
        #     ],
        #     value='Language'
        # )
    ]),
])


# @app.callback(
#     Output('polar-graph-with-dropdown', 'figure'),
#     [Input('year-dropdown-polar', 'value')])
# def update_polar(selected_countries):
#     data = []
#     for selected_country in selected_countries:
#         df_selection = countries[selected_country][['acousticness', 'danceability', 'energy', 'liveness', 'speechiness', 'valence']]
#         datapoint = go.Scatterpolar(
#                 theta=df_selection.columns,
#                 name=selected_country,
#                 r=[df_selection[column].mean() for column in df_selection],
#                 fill="toself"
#         )
#         data.append(datapoint)
#     return {
#         'data': data,
#         'layout': go.Layout(
#             polar=dict(
#                 radialaxis=dict(
#                     visible=True,
#                     range=[0,1]
#                 ),
#             ),
#         )
#     }

def update_bubble(x, y, z):
    data = []
    color = {
        'Spanish': 'lightblue', 'French': 'orange', 'Korean': 'red', 'Turkish': 'green', 'Italian': 'yellow', 'German' : 'grey',
        'Latin Pop': 'darkred', 'Hip Hop': 'black', 'Reggaeton': 'green', 'K-pop': 'violet', 'R&B': 'blue', 'Folk': 'yellow',
         'Bachata': 'orange', 'Electronic': 'cyan', 'Dance': 'lightpink', 'Dancehall': 'pink', 'Latin Urban': 'orangered',
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
                sizeref=2.*max(size)/(40.**2),
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

if __name__ == '__main__':
    app.run_server(debug=True)
