import geopandas
import pandas as pd
import pandas_bokeh
import matplotlib.pyplot as plt
import colorsys

pandas_bokeh.output_notebook()

# Download this from 
# https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2011-eng.cfm
# select:
# lang -> english
# format -> arcGIS
# Forward sortation areas 

canada = geopandas.read_file("./gfsa000b11a_e.shp")
ontario = canada[canada['PRUID'] == '35']

# Sample data to plot
df=pd.read_csv('survey-data.csv');

# Load pop data per FSA and just use the population data
fsa_pop_df=pd.read_csv('9810001901_databaseLoadingData.csv')
fsa_pop_df=fsa_pop_df[fsa_pop_df['Population and dwelling counts (3)'].str.contains('Population, 2021')]
fsa_pop_df=fsa_pop_df[['GEO','VALUE']].copy().rename(columns={"GEO":"GEO", "VALUE": "POP_COUNT"})

# Join our sample data to FSA geo code
df=df.join(fsa_pop_df.set_index('GEO'), on='PCODE');

# Normalize per 100,000 people
df["B"]=100000*df["A"]/df["POP_COUNT"]

# Join ontario dataset with sample data
new_df=ontario.join(df.set_index('PCODE'), on='CFSAUID').dropna()
#fillna(0)

num_colors = 10
colors = [colorsys.hsv_to_rgb(213/360, 0.398, 1 - x*0.9/num_colors) for x in range(num_colors)]
rgb = map(lambda x : '#{:02x}{:02x}{:02x}'.format(int(x[0]*255),int(x[1]*255),int(x[2]*255)), colors)

new_df.plot_bokeh(category="B",
                  title="Responses per 100,000 pop",
                  colormap = list(rgb),
                  figsize=(900, 600),
                  # colormap=["#6B8BB3", "#4D6480", "#2E3C4D", "#0F141A", "#080A0D"],
                  # colormap="Blues", #  colormap=["#009933", "#ff3399"],
                  hovertool_columns=["CFSAUID","A","B", "POP_COUNT"])