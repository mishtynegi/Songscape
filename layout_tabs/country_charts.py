import dash_html_components as html
from dash_core_components import Input

from visualization import PopularSongs_BubbleChart_Heatmap_Network
from visualization import PolarPlot
from visualization import boxplot_audiofeatures_global
from app import app
from dash.dependencies import Input, Output
from plotly import graph_objs as go

content = [
    # box plot on audio features
    html.Div(boxplot_audiofeatures_global.audio_feature_box_plot),
    html.Hr(),
    # audio feature graph
    html.Div(PolarPlot.audio_feature_graph),
    html.Hr(),
    # network graphs
    html.Div(PopularSongs_BubbleChart_Heatmap_Network.network_popular_songs)

]

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('year-dropdown', 'value')])
def update_figure(selected_countries):
    return PolarPlot.update_figure(selected_countries)

@app.callback(
    Output('graph-with-radio', 'figure'),
    [Input('radio-items', 'value')])
def update_figure(selected_feature):
    return boxplot_audiofeatures_global.update_figure(selected_feature)