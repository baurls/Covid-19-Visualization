"""
@author: Shardool
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pandas

class GUI:
    def __init__(self, data_object):
        self.dataController = data_object
    
    def showUI(self):
        #show GUI
        print("test message for debugging")
        pass


    def displayMap(data):
        gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
        #TODO: display data on a map GUI and add slider 



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

