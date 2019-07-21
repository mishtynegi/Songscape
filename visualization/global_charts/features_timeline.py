import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objs as go

features = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness',
            'Speechiness', 'Tempo', 'Valence', 'Popularity', 'Rank']
df = pd.read_csv('./data/audio_feature.csv')

layout = [
    html.Div([
        html.Div([
            html.P('Change of Audio Features in Time')
        ], style={'text-align': 'center', 'font-size': 20}),

        html.Div([
            html.Div([
                html.Label('X axis'),
                dcc.Dropdown(
                    id='x-axis',
                    options=[{'label': i, 'value': i} for i in features],
                    value=features[0]
                )
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                html.Label('Y axis'),
                dcc.Dropdown(
                    id='y-axis',
                    options=[{'label': i, 'value': i} for i in features],
                    value=features[1]
                )
            ], style={'width': '30%', 'display': 'inline-block'})
        ]),

        html.Div([
            dcc.Graph(id='features-graphic'),
        ], style={'align': 'center'}),

        html.Div([
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].max(),
                step=1,
                dots=True,
                marks={str(i): str(i) for i in range(df['year'].min(), df['year'].max(), 5)}
            )
        ])
    ], style={'background-color': 'white'})
]


def update_heatmap(x_axis_name, y_axis_name, year_value):
    dff = df[df['year'] == year_value]

    return {
        'data': [
            go.Histogram2dContour(
                x=dff[x_axis_name.lower()],
                y=dff[y_axis_name.lower()],
                colorscale='Blues',
                reversescale=True,
                xaxis='x',
                yaxis='y'
            ),
            go.Scatter(
                x=dff[x_axis_name.lower()],
                y=dff[y_axis_name.lower()],
                mode='markers',
                marker={
                    'color': 'rgba(0,0,0,0.3)',
                    'size': 3
                    # 'size': 15,
                    # 'opacity': 0.5,
                    # 'line': {'width': 0.5, 'color': 'white'}
                }
            ),
            go.Histogram(
                y=dff[y_axis_name.lower()],
                xaxis='x2',
                marker=dict(
                    color='rgba(190,186,218,0.8)'
                )
            ),
            go.Histogram(
                x=dff[x_axis_name.lower()],
                yaxis='y2',
                marker=dict(
                    color='rgba(190,186,218,0.8)'
                )
            )
        ],

        'layout': go.Layout(
            autosize=False,
            xaxis={
                'title': x_axis_name,
                'zeroline': False,
                'domain': [0, 0.85],
                'showgrid': False
            },
            yaxis={
                'title': y_axis_name,
                'zeroline': False,
                'domain': [0, 0.85],
                'showgrid': False
            },
            xaxis2=dict(
                zeroline=False,
                domain=[0.85, 1],
                showgrid=False
            ),
            yaxis2=dict(
                zeroline=False,
                domain=[0.85, 1],
                showgrid=False
            ),
            height=300,
            width=600,
            bargap=0,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            showlegend=False
        )
    }
