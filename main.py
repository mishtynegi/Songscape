import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from app import app

from layout_tabs import non_english, global_charts, country_charts, reference

app.layout = html.Div([
    # header
    html.Div([
        html.Span("Songscape", className='app-title')
    ], className="row header", style={'text-align': 'center', 'font-weight': 'bold'}
    ),

    html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Global Charts', value='tab-1'),
            dcc.Tab(label='Charts by Country', value='tab-2'),
            dcc.Tab(label='Non-English Song Chart', value='tab-3'),
            dcc.Tab(label='Reference', value='tab-4')
        ])
    ]),

    html.Div(id='tabs-content', className="row", style={"margin": "2% 3%"}),

    html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
    html.Link(
        href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506"
             "/stylesheet-oil-and-gas.css",
        rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
    html.Link(
        href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw"
             "/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
        rel="stylesheet")
],
    className="row",
    style={"margin": "0%"}
)


@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return global_charts.content
    elif tab == 'tab-2':
        return country_charts.content
    elif tab == 'tab-3':
        return non_english.content
    elif tab == 'tab-4':
        return reference.content


if __name__ == "__main__":
    app.run_server(debug=True)
