import json
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc

with open('./data/artists_network.json', 'r') as f:
    df = json.load(f)
years = list(df.keys())

layout = [
    html.Div([
        html.Div([
            html.P('Artists Network')
        ], style={'text-align': 'center', 'font-size': 20}),

        html.Div([
            html.Label('Year: '),
            dcc.Dropdown(
                id='year-network',
                options=[{'label': i, 'value': i} for i in years],
                value=years[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        cyto.Cytoscape(
            id='artists-network',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '500px'},
            elements=[],
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'line-color': 'rgb(220,220,220)'
                    }
                }
            ]
        )
    ], style={'background-color': 'white'})
]


def update_layout(year):
    return df[year]
