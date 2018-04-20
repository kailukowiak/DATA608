import pandas as pd
import plotly as py
from skFunctions import cleaner
import plotly.graph_objs as go
from plotly import tools

df = pd.read_csv('results.csv')

dfVotes = cleaner(df, 'Raw', 'GL', 'Votes')

#trace1 = [go.Bar(x=dfVotes.index.tolist(), y=dfVotes.B1Votes.tolist())]
def smallMultiples(df):
    b1=df.iloc[:, 0].tolist()
    b2=df.iloc[:, 1].tolist()
    b3=df.iloc[:, 2].tolist()

    names=df.index.tolist()

    trace1 = go.Bar(
        x=names,
        y=b1
    )
    trace2 = go.Bar(
        x=names,
        y=b2
    )
    trace3 = go.Bar(
        x=names,
        y=b3
    )
    fig = tools.make_subplots(rows=1, cols=3)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 3)
    fig['layout'].update(height=600, width=600, title='i <3 subplots')
    return fig




trace1 = go.Bar(
    x=dfVotes.index.tolist(),
    y=dfVotes[0].tolist()
)
trace2 = go.Bar(
     x=dfVotes.index.tolist(),
    y=dfVotes.B2Votes.tolist()
)

trace3 = go.Bar(
     x=dfVotes.index.tolist(),
    y=dfVotes.B3Votes.tolist()
)


fig = tools.make_subplots(rows=1, cols=3)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)

fig['layout'].update(height=600, width=600, title='i <3 subplots')
py.offline.plot(fig)
