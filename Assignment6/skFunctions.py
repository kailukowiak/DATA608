import pandas as pd
import plotly.graph_objs as go
from plotly import tools


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

def nodeNames():
    SKL = []
    candidates = ['Elliot', 'Ford', 'Mulroney', 'Alan']
    ballots = ['Ballot 1', 'Ballot 2', 'Ballot 3']
    for i in ballots:
        for j in candidates:
            node = i + ' ' + j
            SKL.append(node)
    return SKL


def sankeyDiagram(values, title, SKL):
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
            color = list(["#EB1A2C","#2C338E" ,'#2AB359' , "#ABE0AC"] * 3)
        ),
        link = dict(
            source = [0,1,2,4,5,3,3,3,6,6], # This is a non- robust way to make it work
            target = [4,5,6,8,9,4,5,6,8,9],
            value = values
        ))

    layout =  dict(
        title = title,
        font = dict(
            size = 10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig

def smallMultiples(df, title):
    colors = ["#EB1A2C","#2C338E" ,'#2AB359' , "#ABE0AC"]
    b1=df.iloc[:, 0].tolist()
    b2=df.iloc[:, 1].tolist()
    b3=df.iloc[:, 2].tolist()

    names=df.index.tolist()

    trace1 = go.Bar(
        x=names,
        y=b1,
        name='Round 1',
        marker=dict(color=colors)
    )
    trace2 = go.Bar(
        x=names,
        y=b2,
        name='Round 2',
        marker=dict(color=colors)
    )
    trace3 = go.Bar(
        x=names,
        y=b3,
        name='Round 3',
        marker=dict(color=colors)
    )
    fig = tools.make_subplots(rows=1, cols=3, subplot_titles=('Ballot 1',
                                                              'Ballot 2',
                                                              'Ballot 3'))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 3)
    fig['layout'].update(height=400, width=700, title=title, showlegend=False)
    return fig
