import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#Must run: %pylab
# Data Import
df  = pd.read_csv('RidingData.csv')
gdf = gpd.read_file('Polling Division Shapefile - 2018 General Election/POLLING_DIVISION.shp')[['ED_NAME_EN', 'geometry']].to_crs('+proj=robin')

# Data Clearning
df.Riding = df.Riding.str.strip()

gdf.ED_NAME_EN.replace(regex=True,
                              inplace=True, to_replace='\\x97',value=r' ')
gdf.ED_NAME_EN.replace(regex=True, inplace=True,
                               to_replace='\\-',value=r' ')

gdf = gdf.loc[gdf['ED_NAME_EN'] !=  'Etobicoke Centre']

df.Riding = df.Riding.str.replace('—', ' ') # Note that the hyphen like symbol is not acutally a minus sign.
# That was a good hour of my day gone trying to fix that.
df.Riding = df.Riding.str.replace('-', ' ') # And somehow there was even a hyphen in the list.

df.Riding = df.Riding.str.replace('Mississauga Erindale', 'Mississauga Erin Mills')
df.Riding = df.Riding.str.replace('Scarborough Rouge', 'Scarborough Rouge Park')


# Splitting Data Frames


Ballot1 = df.filter(regex='B1')
Ballot1 = Ballot1.filter(regex='Votes')
Ballot1['Riding'] =  df.Riding

Ballot2 = df.filter(regex='B2')
Ballot2 = Ballot2.filter(regex='Votes')
Ballot2['Riding'] =  df.Riding

Ballot3 = df.filter(regex="B3")
Ballot3 = Ballot3.filter(regex='Votes')
Ballot3['Riding'] =  df.Riding


## Will break Stuf below
from bokeh.plotting import save, figure, show
from bokeh.models import GeoJSONDataSource, CategoricalColorMapper
from bokeh.layouts import column


def maxRiding(df, gdf):
    tall = pd.melt(df, id_vars=['Riding'],
                   var_name="Candidate",
                   value_name="Votes")
    idx = tall.groupby(['Riding'],sort=False)['Votes'].transform(max) == tall['Votes']
    tall = tall[idx]
    tall['Candidate'] = tall['Candidate'].map(lambda x: x.lstrip('B1').lstrip('B2').lstrip('B3').replace("_Votes", ""))
    # https://stackoverflow.com/questions/15705630/python-getting-the-row-which-has-the-max-value-in-groups-using-groupby
    mapDF = gdf.merge(tall, left_on='ED_NAME_EN', right_on='Riding')
    geo_source = GeoJSONDataSource(geojson=mapDF.to_json())
    return geo_source


b1Geo =  maxRiding(Ballot1, gdf)
b2Geo =  maxRiding(Ballot2, gdf)
b3Geo =  maxRiding(Ballot3, gdf)


# Initialize our plot figure
p1 = figure(title="Ballot One Results")


color_mapper = CategoricalColorMapper(factors=['Elliott', 'Ford', 'Mulruney', 'Allan'],
                                      palette=['#EB1A2C', "#2C338E" ,'#2AB359' , "#ABE0AC"])
p1.patches('xs', 'ys', source=b1Geo,
          fill_color= {'field': 'Candidate', 'transform': color_mapper},
          fill_alpha=1,
           line_color="black", line_width=0.2)
p1.xgrid.visible = False
p1.ygrid.visible = False
p1.axis.visible = False

p2 = figure(title="Ballot Two Results")
p2.patches('xs', 'ys', source=b2Geo,
          fill_color= {'field': 'Candidate', 'transform': color_mapper},
          fill_alpha=1,
          line_color="black", line_width=0.2)
p2.xgrid.visible = False
p2.ygrid.visible = False
p2.axis.visible = False

p3 = figure(title="Ballot Three Results")
p3.patches('xs', 'ys', source=b3Geo,
          fill_color= {'field': 'Candidate', 'transform': color_mapper},
          fill_alpha=1,
          line_color="black", line_width=0.2)

p3.xgrid.visible = False
p3.ygrid.visible = False
p3.axis.visible = False
outfp = r"map.html"

# Save the map
#save(p, outfp)
#show(p)
from bokeh.io import export_png
#p = column(p1, p2, p3)
#export_png(p1, filename="plot1.png"
# export_png(p2, filename="plot2.png")
# export_png(p3, filename="plot3.png")
show(column(p1, p2, p3))
