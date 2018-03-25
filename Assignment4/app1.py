import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt
import numpy as np

# Data preperation

# Raw data
df = pd.read_csv('Data/data.csv')
df['Date'] = pd.to_datetime(df.Date)

# rememoves >< symbols and converts to numeric.
df['EnteroCount'] = df['EnteroCount'].map(lambda x: x.lstrip('<>'))\
                                     .astype(float)
df2 = df.set_index('Date')
allDates = pd.date_range(start=df2.index.min(), end=df2.index.max())

dfPivot = df.pivot(index='Date',
                   columns='Site',
                   values='EnteroCount').reindex(allDates).ffill()
dfPivot['Date1'] = dfPivot.index
# melt data on unique values and originl date
# I used original date to avoid confusion between records and index
colNames = list(df.Site.unique())

dfFilled = dfPivot.melt(id_vars='Date1', value_vars=colNames)

dfFinal = pd.merge(dfFilled,
                   df,
                   how='left',
                   left_on=['Date1', 'Site'],
                   right_on=['Date', 'Site'])

dfFinal = dfFinal.ffill()
dfFinal.drop(['value'], axis=1)

dfFinal['Date'] = 'Recored Taken On: ' + dfFinal['Date'].astype(str)


# Dash app
app = dash.Dash()

app.layout = html.Div([
    html.H2("Pick a Date"),
    html.Div(
        [
            dcc.DatePickerSingle(
                id='DatePicked',
                min_date_allowed=dt(2006, 9, 19),
                max_date_allowed=dt(2013, 10, 21),
                date=dt(2010, 5, 10)
                ),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
        dcc.Graph(id='polutionGraph'),
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
    dash.dependencies.Output('polutionGraph', 'figure'),
    [dash.dependencies.Input('DatePicked', 'date')])
def update_graph(DatePicked):
        dfDay = dfFinal.loc[dfFinal.Date1 == DatePicked]
        CRed = 'rgb(222,0,0)'
        CGreen = 'rgb(0,222,0)'
        Color = ([CRed if dfDay.EnteroCount.iloc[x] > 110
                  else CGreen for x in range(len(dfDay))])
        # Thanks to:
        # https://stackoverflow.com/questions/43011405/change-bar-color-based-on-value
        return {
                'data': [
                go.Bar(x=dfDay.Site,
                       y=dfDay.EnteroCount.apply(np.log),
                       text=dfDay.Date,
                       marker=dict(color=Color),
                       name='Data for {}'.format(DatePicked)
                ),
                go.Bar(x=dfDay.Site,
                       y=df.groupby('Site')['EnteroCount'].mean().apply(np.log),
                       marker=dict(color='rgb(158,202,225)'),
                       name='Average'
                )
                ],
                'layout': {'title': 'Safety Levels of Different Ares for {}'
                           .format(DatePicked),
                           'barmode':'group',
                           'shapes':[{
                                   'type' : 'line',
                                   'x0' : dfDay.Site.iloc[0],
                                   'y0' : np.log(110),
                                   'x1' : dfDay.Site.iloc[-1],
                                   'y1' : np.log(110)}
                ]}

        }


if __name__ == '__main__':
    app.run_server(debug=True)
