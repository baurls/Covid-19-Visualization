"""
Created on Mon Apr 20 05:24:53 2020

@author: Shardool
"""
#local imports 
import global_code

#global packages
import matplotlib.pyplot as plt
import plotly.express as px


#plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

logger = global_code.getLogger()

class GUI:
    def __init__(self, data_object):
        self.data_controller = data_object
        self.st_date = 0
        self.ed_date = 0
        self.country = ""
    
    
    def showUI(self):
        #show GUI
        name = global_code.constants.APP_NAME
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(name, external_stylesheets=external_stylesheets)
        data_pointer = self.data_controller
        
        #add elemts to the layout
        main_div = []
        navigation_list = []
        plots_list = []
        
        navigation_list.append(html.H2('Country Selection'))
        navigation_list.append(UIComponents.get_country_dropdown(data_pointer))
        navigation_list.append(html.Label(' '))
        
        navigation_list.append(html.H2('Timeframe Selection'))
        navigation_list.append(html.Label(' Start'))
        navigation_list.append(UIComponents.get_timeframe_selection(data_pointer, 'start'))
        navigation_list.append(html.Label(' End'))
        navigation_list.append(UIComponents.get_timeframe_selection(data_pointer, 'end'))
        
        plots_list.append(html.H2('Plots'))
        plots_list.append(html.H3('Confirmed for selected Interval/Country'))
        plots_list.append(html.Label('<insert_plot_here>'))
        plots_list.append(html.H3('Deaths for selected Interval/Country'))
        plots_list.append(html.Label('<insert_plot_here>'))
        plots_list.append(html.H3('Recovered for selected Interval/Country'))
        plots_list.append(html.Label('<insert_plot_here>'))
        
        lower_list = []
        lower_list.append(html.Div(navigation_list, style={'columnCount': 1}))
        lower_list.append(html.Div(plots_list, style={'columnCount': 1}))
        lower_list.append(html.Div(id='dd-output-container'))
        lower_list.append(html.Div(id='dd-output-container2'))
        lower_list.append(html.Div(id='dd-output-container3'))
        lower_div = html.Div(lower_list,style={'columnCount': 2})
        
 
        main_div.append(UIComponents.get_map(data_pointer))
        main_div.append(lower_div)        
        
        app.layout = html.Div(main_div)
        

        #Callback for dropdown
        @app.callback(
            Output(component_id='dd-output-container', component_property='children'),
            [Input(component_id='country_dropdown', component_property='value')]
        )

        def update_value(value):
            self.country = value
            self.prepare_data()

        #callback for start date
        @app.callback(
            Output(component_id='dd-output-container2', component_property='children'),
            [Input(component_id='start_slider', component_property='value')]
        )

        def update_start(start_date):
            self.st_date = start_date
            self.prepare_data()

        #callback for end date
        @app.callback(
                Output(component_id='dd-output-container3', component_property='children'),
                [Input(component_id='end_slider', component_property='value')]
        )

        def update_end(end_date):
            self.ed_date = end_date
            self.prepare_data()


        port = global_code.constants.APP_PORT
        app.run_server(port=port, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
        
        logger.log('GUI Server offlie')
        


    def prepare_data():
        #TODO use the current country start and end date to select which data to pass to plotting methods

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
    
class UIComponents:
    def get_country_dropdown(data_pointer):
        choose_options = []
        countries = data_pointer.get_all_countries()
        for country in countries:
            entry = {'label': country, 'value': country}
            choose_options.append(entry)
        
        dropdown = dcc.Dropdown(id='country_dropdown',options=choose_options,value='MTL')
        return dropdown
    
    def get_map(data_pointer):
        return dcc.Graph(figure=UIComponents.__get_map_figure(data_pointer))
    
    def get_timeframe_selection(data_pointer, time_type):
        day_list = data_pointer.get_all_days_recorded()
        count_days = len(day_list)
        
        selected = count_days/4 if time_type == 'start' else 3* count_days/4 
        selected = int(selected )
        
        slider_id = 'start_slider' if time_type == 'start' else 'end_slider'
        slider = dcc.Slider(
            id=slider_id,
            min=0,
            max=count_days-1,
            marks={i: day if i%10 == 0 else str('') for i,day in enumerate(day_list)},
            value=selected,
        )
        return slider


#util methods
    def __get_map_figure(data_pointer):
        fig = px.choropleth(data_pointer.get_map_dataframe(), 
                    locations="Country", 
                    locationmode = "country names",
                    color="Confirmed", 
                    hover_name="Country", 
                    hover_data=["Deaths", "Recovered"],
                    animation_frame="Date",
                    color_continuous_scale= px.colors.sequential.Reds
                   )
        as_of_date = data_pointer.get_as_of_date()
        fig.update_layout(
            title_text = 'Global Spread of Coronavirus as of {}'.format(as_of_date),
            title_x = 0.5,
            geo=dict(
                showframe = False,
                showcoastlines = False,
            ))
        return fig