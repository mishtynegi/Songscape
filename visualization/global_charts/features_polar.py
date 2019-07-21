import dash_table
import dash_html_components as html
import dash_core_components as dcc

import plotly.graph_objs as go
import pandas as pd

tracks = pd.read_csv('./data/top_by_year_unmodified.csv')
features = pd.read_csv('./data/audio_feature.csv')
data = tracks.merge(features, on=['id', 'year', 'rank'], how='left')
years = data['year'].unique()
table_header = ['Rank', 'Artists', 'Song']

layout = [
    html.Div([
        html.Div([
            html.P('Audio Features by Song')
        ], style={'text-align': 'center', 'font-size': 20}),

        html.Div([
            html.Label('Year: '),
            dcc.Dropdown(
                id='year-features',
                options=[{'label': i, 'value': i} for i in years],
                value=years[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                dash_table.DataTable(
                    id="features-table",
                    columns=[{"name": i, "id": i} for i in table_header],
                    style_table={
                        'height': 500,
                        'overflowY': 'scroll'
                    },
                    style_header={
                        'fontWeight': 'bold'
                    },
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[{
                        'if': {'column_id': 'Rank'},
                        'textAlign': 'center'
                    }],
                    style_as_list_view=True,
                    row_selectable="multi"
                )
            ], style={'width': '59%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='features-polar')
            ], style={'width': '40%', 'height': '700', 'float': 'right', 'display': 'inline-block'})
        ])
    ], style={'background-color': 'white'})
]


def update_table(year):
    df = data[data['year'] == year].rename(columns={'rank': 'Rank', 'artist': 'Artists', 'title': 'Song'})
    return df[table_header].to_dict('rows')


def update_polar_graph(year, selected_rows):
    df = data[data['year'] == year]

    if selected_rows:
        polar_trace = [go.Scatterpolar(
            r=[df.loc[i, 'acousticness'] * 100, df.loc[i, 'danceability'] * 100, df.loc[i, 'energy'] * 100,
               df.loc[i, 'instrumentalness'] * 100, df.loc[i, 'liveness'] * 100, df.loc[i, 'loudness'],
               df.loc[i, 'speechiness'] * 100, df.loc[i, 'valence'] * 100, df.loc[i, 'popularity'],
               df.loc[i, 'acousticness'] * 100],
            theta=['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness',
                   'Loudness', 'Speechiness', 'Valence', 'Popularity', 'Acousticness'],
            fill='toself'
        ) for i in selected_rows]
    else:
        polar_trace = [go.Scatterpolar(
            r=[-20, -20, -20, -20, -20, -20, -20, -20, -20, -20],
            theta=['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness',
                   'Loudness', 'Speechiness', 'Valence', 'Popularity', 'Acousticness'],
            fill='toself'
        )]

    polar_layout = go.Layout(
        title='Audio Features',
        polar=dict(
            radialaxis=dict(
                range=[-20, 100],
                visible=True
            )
        ),
        showlegend=False
    )

    return {
        "data": polar_trace,
        "layout": polar_layout
    }
