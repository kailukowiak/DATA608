import pandas as pd
from skFunctions import cleaner, sankeyData, nodeNames, sankeyDiagram
from skFunctions import smallMultiples
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

# Dash app
app = dash.Dash()


image_filename = 'ONPCLogo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app.layout = html.Div([
        html.Div([
                html.Div([
                         html.Img(src='data:image/png;base64,{}'
                                  .format(encoded_image.decode()))
                ], className='two columns'),

                html.Div([
                        dcc.Markdown('''
## Ontario Provincial PC Leadership Race
After a rather dramatic resignation of the Ontario PC leader, Patric Brown, was 
ousted over sexual harassment allegations.

The resulting leadership race saw a dramatic finish between the top two as Mr 
Ford one more point (calculated by counting the number of people in a riding up 
to 100 and then assigning 100 to the result after that).

Ms Elliott ended with more of the popular votes but fewer points, leading to a 
confusing and almost contested recount/challenge.[Pundits](http://www.cbc.ca/news/politics/grenier-pc-leadership-results-1.4571699) 
have theorized that Ms Granic Allen's voters delivered the victory mostly because
 Mr Ford mimicked her stance on sexual education in schools, taking a more 
conservative stance.

The Data was collected from [Wikipedia](https://en.wikipedia.org/wiki/Progressive
Conservative_Party_of_Ontario_leadership_election,_2018).

This data is interesting because Mr Ford ran on a populist agenda, similar to 
Mr Trump's campaign (although less fraught with controversy). In fact, in 
Canada, Mr Trump was often compared to Mr Ford's late brother and former mayor 
of Toronto Rob. This analysis is an attempt to give insight into the alliance 
between religious candidates making alliances with populists. 

This data also highlights the importance of differing election styles, such as 
the points system used in the PC race. 
'''),], className='ten columns'),     
                ], className='row'),
        html.Div([
                html.H3('Chose Total Votes or Total Points'),
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
                            '{} Won by Cadidate in the 2018 PC Leadership Race'
                            .format(VorR),
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
