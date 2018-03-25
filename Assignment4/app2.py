import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


df = pd.read_csv('Data/data.csv')

df['EnteroCount'] = df['EnteroCount'].map(lambda x: x.lstrip('<>'))\
                                     .astype(float)

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='site-menue',
        options=[{'label': i, 'value': i} for i in list(df.Site.unique())],
        multi=True,
        value='Gowanus Canal'
        # value=  list(df.Site.unique()) # "MTL"
        ),
    dcc.Graph(id='location-scatter-plot'),
     dcc.Markdown('''
#### Water Safety levels in various kayak areas:

Water safety levels vary along the Hudson River and over time. 
Select a calendar day to see if the location you kayaked on was 
safe or if you could have been at risk. Higher red levels indicate
potentially unsafe water. If the area is red on a particular day, 
it could mean that you have been exposed to dangerous pathogens. 


The black line indicates the safe level of toxins.


*Note:* safety leves are taken from federal regulations and guidelines.
Measurments are not taken each day. Please refer to the chart to see when 
the last count was taken. (Hover over the column you're interested in.)
''')
])


@app.callback(
    dash.dependencies.Output('location-scatter-plot', 'figure'),
    [dash.dependencies.Input('site-menue', 'value')])
def update_figure(selectedSites):
    # selectedSites = list(df.Site.unique()) # Delete after
    filterDF = df[df['Site'].isin(selectedSites)]
    traces = []
    for i in filterDF.Site.unique():
        dfLocation = filterDF[filterDF['Site'] == i]
        traces.append(go.Scatter(
            x=dfLocation['FourDayRainTotal'],
            y=dfLocation['EnteroCount'],
            mode='markers',
            opacity=0.7,
            marker={'size': 15},
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title':'Rain Fall in Last 4 Days'},
            yaxis={'title': 'Polution Rates'},
            legend=dict(orientation="v",x=-0.3,y=1),
            #legend={'x': 10, 'y': 10},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
