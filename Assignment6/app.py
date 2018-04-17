import pandas as pd
import plotly as py
import numpy as np

df = pd.read_csv('results.csv')




def cleaner(df, typeFilter, colDrop, colSelect):
    '''A function to clean df
    df = DataFrame
    typeFilter = Raw/Percent
    colDrop = 'GL'
    colSelect = Votes/Points
    '''
    colSelect = colSelect+'|Name' # NEcessary so name is not dropped
    df = df[df.Type == typeFilter] # Selects rows
    df = df[df.columns.drop(list(df.filter(regex=colDrop)))]
    df = df.filter(regex=colSelect)
    df = df.set_index("Name")
    return df

dfRawV = cleaner(df, 'Raw', 'GL', 'Votes')

def sankeyData(df):
    """
    A non-robust function to reshape data into a format
    readable by plotly
    """
    b0 = df.iloc[0:3, 0].tolist()
    b1 = df.iloc[0:2, 1].tolist()
    aVotes = (df.iloc[0:3, 1] - df.iloc[0:3, 0]).tolist()
    mVotes = (df.iloc[0:2, 2] - df.iloc[0:2, 1]).tolist()
    return b0+b1+aVotes+mVotes

values = sankeyData(dfRawV)
SKL = []
candidates = ['Elliot', 'Ford', 'Mulroney', 'Alan']
ballots = ['Ballot 1', 'Ballot 2', 'Ballot 3']
for i in ballots:
    for j in candidates:
        node = i + ' ' + j
        SKL.append(node)
data = dict(
    type='sankey',
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(
            color = "black",
            width = 0.5
        ),
        label = SKL,
        color = list(['blue'] * 12)
    ),
    link = dict(
      source = [0,1,2,4,5,3,3,3,6,6], # This is a non- robust way to make it work
      target = [4,5,6,8,9,4,5,6,8,9],
        value = values
  ))

layout =  dict(
    title = "Basic Sankey Diagram",
    font = dict(
      size = 10
    )
)

fig = dict(data=[data], layout=layout)
py.offline.plot(fig, validate=False)
