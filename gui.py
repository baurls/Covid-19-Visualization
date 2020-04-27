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
import plotly.graph_objects as go


#Date-Time Converter 
from dateutil import parser

logger = global_code.getLogger()

class GUI:
    def __init__(self, data_object):
        self.data_controller = data_object
        df = self.data_controller.get_map_dataframe()
        dates = list(df['Date'])
        date_set = []
        for date in dates:
            if date not in date_set: date_set.append(date)
        self.date_map = date_set
    
    
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
        

        plots_list.append(html.H2('Plot'))
        plots_list.append(html.Div(dcc.Graph(id='main-graph')))
       

        lower_list = []
        lower_list.append(html.Div(navigation_list, style={'columnCount': 1}))
        lower_list.append(html.Div(plots_list, style={'columnCount': 1}))
        lower_list.append(html.Div(id='dd-output-container1'))
        lower_div = html.Div(lower_list,style={'columnCount': 2})
        
 
        main_div.append(UIComponents.get_map(data_pointer))
        main_div.append(lower_div)        
        
        app.layout = html.Div(main_div)
        

        #Callback for dropdown
        @app.callback(
            Output('main-graph', 'figure'),
            [Input(component_id='country_dropdown', component_property='value'),
            Input(component_id='start_slider', component_property='value'),
            Input(component_id='end_slider', component_property='value')]
        )

        def update_graph(country,start_date,end_date):
            data_pointer = self.data_controller
            date_set = self.date_map[start_date:end_date+1]
            dates = self.date_map
            df = data_pointer.get_map_dataframe()
            cases_dict = {}
            deaths_dict = {}
            recovered_dict = {} 
            if country != 'MTL':
                updated_df = df.loc[df['Country'] == country]
                for index,row in updated_df.iterrows():
                    if row['Date'] in date_set:
                        day = row['Date']
                        if day in cases_dict:
                            cases_dict[day] += row['Confirmed']
                            deaths_dict[day] += row['Deaths']
                            recovered_dict[day] += row['Recovered']
                        else:
                            cases_dict[day] = row['Confirmed']
                            deaths_dict[day] = row['Deaths']
                            recovered_dict[day] = row['Recovered']
                
                y_data = [value for key,value in cases_dict.items()]
                y2_data = [value for key,value in deaths_dict.items()]
                y3_data = [value for key,value in recovered_dict.items()]
                x_data = list(range(len(date_set)))

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_data, y=y_data,
                    mode='lines+markers',
                    name='Confirmed Cases'))
                fig.add_trace(go.Scatter(x=x_data, y=y2_data,
                    mode='lines+markers',
                    name='Deaths'))
                fig.add_trace(go.Scatter(x=x_data, y=y3_data,
                    mode='lines+markers', name='Recovered'))
                t = f"Confirmed Cases, Deaths, and Recoveries for {country} from {dates[start_date]} to {dates[end_date-1]}"
                fig.update_layout(title=t, xaxis_title='Day',
                   yaxis_title='Number of People')
                return fig
                
            return dash.no_update
                
                
        port = global_code.constants.APP_PORT
        app.run_server(port=port, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
        
        logger.log('GUI Server offlie')
  
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