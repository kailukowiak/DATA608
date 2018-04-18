import pandas as pd
import plotly as py
from skFunctions import cleaner, sankeyData, nodeNames, sankeyDiagram

df = pd.read_csv('results.csv')

dfRawV = cleaner(df, 'Raw', 'GL', 'Votes')

voteValues = sankeyData(dfRawV)


# Node Names
SKL = nodeNames()

votesFig = sankeyDiagram(voteValues, 'Votes Won by Cadidate in the 2018 PC Leadership Race', SKL)

py.offline.plot(votesFig, validate=False)



## Count of Ridings
dfCount = cleaner(df, 'Raw', 'GL', 'Points')
countValues = sankeyData(dfCount)
figCount = sankeyDiagram(countValues, 'Points Won in the 2018 PC leadership Race', SKL)

py.offline.plot(figCount, validate = False)
