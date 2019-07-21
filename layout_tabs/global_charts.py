import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from plotly import graph_objs as go

from app import app
from visualization.global_charts import features_polar, genres_violin, artists_network, \
    features_heatmap, features_timeline

content = [
    # Heat map
    html.Div(features_heatmap.layout),

    # Timeline
    html.Hr(),
    html.Div(features_timeline.layout),

    # Violin graph
    html.Hr(),
    html.Div([dcc.Graph(figure=go.Figure(genres_violin.fig))]),

    # Features polar graph
    html.Hr(),
    html.Div(features_polar.layout),

    # Artists network
    html.Hr(),
    html.Div(artists_network.layout)
]


@app.callback(
    Output('features-graphic', 'figure'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('year-slider', 'value')])
def update_timeline(x_axis_name, y_axis_name, year_value):
    return features_timeline.update_heatmap(x_axis_name, y_axis_name, year_value)


@app.callback(
    Output("features-table", "data"),
    [Input("year-features", "value")])
def update_table(year):
    return features_polar.update_table(year)


@app.callback(
    Output("features-polar", "figure"),
    [Input("year-features", "value"),
     Input('features-table', "derived_virtual_selected_rows")])
def update_polar_graph(year, selected_rows):
    return features_polar.update_polar_graph(year, selected_rows)


@app.callback(
    Output('artists-network', 'elements'),
    [Input('year-network', 'value')])
def update_network(year):
    return artists_network.update_layout(year)
