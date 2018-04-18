import pandas as pd
from skFunctions import cleaner, sankeyData, nodeNames, sankeyDiagram
import dash
import dash_core_components as dcc
import dash_html_components as html

# Data preperation
df = pd.read_csv('results.csv')

SKL = nodeNames()

voteDF= cleaner(df, 'Raw', 'GL', 'Votes')
voteValues = sankeyData(voteDF)
votesFig = sankeyDiagram(voteValues,
                         'Votes Won by Cadidate in the 2018 PC Leadership Race',
                         SKL)

## Count of Ridings
dfCount = cleaner(df, 'Raw', 'GL', 'Points')
countValues = sankeyData(dfCount)
countFig = sankeyDiagram(countValues,
                         'Points Won in the 2018 PC leadership Race',
                         SKL)

# Dash app
app = dash.Dash()

app.layout = html.Div([
        html.H3("Pick Votes or Count"),
        dcc.Dropdown(
                id='VorR',
                options=[
                        {'label': 'Votes View', 'value': votesFig},
                        {'label': 'Ridings View', 'value': countFig}
                ],
                value=countFig,
        ),
        dcc.Graph(id='sankeyGraph')
])



@app.callback(
    dash.dependencies.Output('sankeyGraph', 'figure'),
    [dash.dependencies.Input('VorR', 'value')])
def update_graph(graphToShow):
        return graphToShow


if __name__ == '__main__':
    app.run_server(debug=True)
