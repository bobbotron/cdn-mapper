import geopandas
import pandas as pd
import pandas_bokeh
import matplotlib.pyplot as plt
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
#df=DataFrame({'PCODE': ['P0V','P0L','P0T','P0Y', 'P0G', 'K0G'], 'A':[6,3,5,2,2,42] })

# Join ontario dataset with sample data
new_df=ontario.join(df.set_index('PCODE'), on='CFSAUID').fillna(0)


new_df.plot_bokeh(#simplify_shapes=20000,
                  category="A",
                  colormap="Spectral", 
                  hovertool_columns=["CFSAUID","A"])