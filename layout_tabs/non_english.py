import dash_html_components as html

from dash.dependencies import Input, Output

from app import app

from visualization.non_englsih_charts import boxplot, bubble_chart, polar_plot

content = [
    # Features box plot
    html.Div(boxplot.layout),

    # Features bubble chart
    html.Hr(),
    html.Div(bubble_chart.layout),

    # Features polar chart
    html.Hr(),
    html.Div(polar_plot.layout)
]


@app.callback(
    Output('bubble-charts-with-dropdown', 'figure'),
    [Input('attr-dropdown-bubble-x', 'value'), Input('attr-dropdown-bubble-y', 'value'),
     Input('attr-radio-bubble', 'value')])
def update_bubble(x, y, z):
    return bubble_chart.update_bubble(x, y, z)


@app.callback(
    Output('graph-with-dropdown2', 'figure'),
    [Input('lang-dropdown', 'value'), Input('genre-dropdown', 'value')])
def update_figure(languages, genres):
    return polar_plot.update_figure(languages, genres)
