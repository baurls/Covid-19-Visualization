"""
Created on Mon Apr 20 05:24:53 2020

@author: Shardool
"""
#local imports 
import global_code

#global packages
import matplotlib.pyplot as plt
import plotly.express as px


logger = global_code.getLogger()

class GUI:
    def __init__(self, data_object):
        self.data_controller = data_object
    
    
    def showUI(self):
        #show GUI
        self.displayMap()
        logger.log('Map loading finished')
        


    def displayMap(self):
        print(self.data_controller.get_map_dataframe())
        fig = px.choropleth(self.data_controller.get_map_dataframe(), 
                    locations="Country", 
                    locationmode = "country names",
                    color="Confirmed", 
                    hover_name="Country", 
                    hover_data=["Deaths", "Recovered"],
                    animation_frame="Date",
                    color_continuous_scale= px.colors.sequential.Reds
                   )
        as_of_date = self.data_controller.get_as_of_date()
        fig.update_layout(
            title_text = 'Global Spread of Coronavirus as of {}'.format(as_of_date),
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
        x = self.x_vals
        y = self.y_vals
        x_label = self.x_label
        y_label = self.y_label
        t = self.title
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(t)
        plt.yscale('log')
        plt.plot(x,y)  
        plt.show()
        return 

