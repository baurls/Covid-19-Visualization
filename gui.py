"""
@author: Shardool
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
import json
import plotly as py
import plotly.express as px
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, plot

class GUI:
    def __init__(self, data_object):
        self.dataController = data_object
        self.dataFrame = pd.read_csv('Data/2020-04-21/covid_19_data.csv')
        self.displayMap()
    
    
    def showUI(self):
        #show GUI
        print("test message for debugging")
        pass


    def displayMap(self):
        self.dataFrame= self.dataFrame.rename(columns={'Country/Region':'Country'})
        self.dataFrame = self.dataFrame.rename(columns={'ObservationDate':'Date'})
        final_df = self.dataFrame[self.dataFrame['Confirmed']>0]
        final_df = final_df.groupby(['Date','Country']).sum().reset_index()

        fig = px.choropleth(final_df, 
                    locations="Country", 
                    locationmode = "country names",
                    color="Confirmed", 
                    hover_name="Country", 
                    animation_frame="Date",
                    color_continuous_scale= px.colors.sequential.Reds
                   )
        fig.update_layout(
            title_text = 'Global Spread of Coronavirus as of April 20, 2020 {Author: Shardool}',
            title_x = 0.5,
            geo=dict(
                showframe = False,
                showcoastlines = False,
            ))
        
        fig.show()



    def showTrend(self,x_vals,y_vals,x_label,y_label,title):
        #Will graph the trend in cases for a given timeframe and given location
        x = self.x_vals
        y = self.y_vals
        x_label = self.x_label
        y_label = self.y_label
        t = self.title
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(t)
        plt.plot(x,y)  
        plt.show()
        return 

    def showLogTransform(self,x_vals,y_vals,x_label,y_label,title):
        '''Will plot a log transformation to present exponential 
           trends for a give timeframe and given location'''
        return

