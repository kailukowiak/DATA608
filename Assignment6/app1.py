import pandas as pd
from skFunctions import cleaner, sankeyData, nodeNames, sankeyDiagram, smallMultiples
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools

# Dash app
app = dash.Dash()


app.layout = html.Div([
        html.Div([
                dcc.Dropdown(
                id='VorR',
                options=[
                        {'label': 'Votes View', 'value': 'Votes'},
                        {'label': 'Ridings View', 'value': 'Points'}
                ],
                        value='Points',),
                
        ]),
    html.Div([
        html.Div([
            html.H3('Sankey Diagram of Voting Preferences'),
                 dcc.Graph(id='sankeyGraph')
        ], className="six columns"),

        html.Div([
            html.H3('By Round Results'),
            dcc.Graph(id='smGraph')
        ], className="six columns"),
    ], className="row")
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    dash.dependencies.Output('sankeyGraph', 'figure'),
    [dash.dependencies.Input('VorR', 'value')])
def update_graph(VorR):
        df = pd.read_csv('results.csv')
        SKL = nodeNames()
        df = cleaner(df, 'Raw', 'GL', VorR)
        df = sankeyData(df)
        fig = sankeyDiagram(df,
                            '{} Won by Cadidate in the 2018 PC Leadership Race'.format(VorR),
                         SKL)
        return fig


@app.callback(
    dash.dependencies.Output('smGraph', 'figure'),
    [dash.dependencies.Input('VorR', 'value')])
def update_sm(VorR):
        df = pd.read_csv('results.csv')
        df = cleaner(df, 'Raw', 'GL', VorR)
        smg=smallMultiples(df, '{} Won by Round'.format(VorR))
        return smg

if __name__ == '__main__':
    app.run_server(debug=True)
