"""
Created on Mon Apr 20 05:24:53 2020

@author: Shardool and Lukas
"""
#local imports 
import global_code

#global packages
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


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
        
        navigation_list.append(html.Label(' Axis type'))
        navigation_list.append(UIComponents.get_log_checkbox())
        

        plots_list.append(html.H2('Plot'))
        plots_list.append(html.Div(dcc.Graph(id='main-graph')))
        plots_list.append(html.H2('Compare spread over time'))
        plots_list.append(UIComponents.get_country_dropdown(data_pointer,forComparison=True))
        plots_list.append(html.Div(dcc.Graph(id='compare-graph')))
        plots_list.append(html.Div(dcc.Graph(id='daily-compare-graph')))
        plots_list.append(html.H2('Hotspots over time'))
        plots_list.append(html.H3('Confirmed Cases'))
        plots_list.append(UIComponents.get_hotspot_diagram(data_pointer))
        plots_list.append(html.H3('Deaths'))
        plots_list.append(UIComponents.get_hotspot_diagram(data_pointer, showDeaths=True))
        
        lower_list = []
        lower_list.append(html.Div(navigation_list, style={'columnCount': 1, 'padding':'5px'}))
        lower_list.append(html.Div(plots_list, style={'columnCount': 1, 'padding':'20px'}))
        lower_list.append(html.Div(id='dd-output-container1'))
        lower_div = html.Div(lower_list,style={'columnCount': 1})
        
 
        main_div.append(UIComponents.get_map(data_pointer))
        main_div.append(lower_div)        
        
        app.layout = html.Div(main_div)
        

        
        def get_country_over_time_data(country, date_range):
            df = self.data_controller.get_map_dataframe()
            updated_df = df.loc[df['Country'] == country]
            cases_dict = {}
            deaths_dict = {}
            recovered_dict = {} 
            
            for index,row in updated_df.iterrows():
                if row['Date'] in date_range:
                    day = row['Date']
                    if day in cases_dict:
                        cases_dict[day] += row['Confirmed']
                        deaths_dict[day] += row['Deaths']
                        recovered_dict[day] += row['Recovered']
                    else:
                        cases_dict[day] = row['Confirmed']
                        deaths_dict[day] = row['Deaths']
                        recovered_dict[day] = row['Recovered']
            
            cases_data = [value for key,value in cases_dict.items()]
            death_data = [value for key,value in deaths_dict.items()]
            recovered_data = [value for key,value in recovered_dict.items()]
            x_data = list(range(len(date_range)))
            return x_data, cases_data, death_data, recovered_data
        
        #Callback for dropdown
        @app.callback(
            Output('main-graph', 'figure'),
            [Input(component_id='country_dropdown', component_property='value'),
            Input(component_id='start_slider', component_property='value'),
            Input(component_id='end_slider', component_property='value'),
            Input(component_id='log_type', component_property='value')]
        )
        def update_graph(country,start_date,end_date,axis_type):
            date_range = self.date_map[start_date:end_date+1]
            (x_data, cases_data, death_data, recovered_data) = get_country_over_time_data(country, date_range)
            dates = self.date_map
       
            if country != 'MTL':
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_data, y=cases_data,
                    mode='lines+markers',
                    name='Confirmed Cases'))
                
                fig.add_trace(go.Scatter(x=x_data, y=death_data,
                    mode='lines+markers',
                    name='Deaths'))
                
                fig.add_trace(go.Scatter(x=x_data, y=recovered_data,
                    mode='lines+markers', name='Recovered'))
                
                t = f"Details for {country} from {dates[start_date]} to {dates[end_date-1]}"
                
                axis_type = 'linear' if axis_type == 'Linear' else 'log'
                
                fig.update_layout(title=t, xaxis_title='Day', yaxis_title='Number of People', yaxis_type=axis_type, updatemenus=[
                   dict(
                        buttons=list([
                            dict(
                                args=[{"visible": [True, True, True]}],
                                label="Show Confirmed Cases",
                                method="restyle"
                            ),
                            dict(
                                args=[{"visible": [False, True, True]}],
                                label="Hide Confirmed Cases",
                                method="restyle"
                            )]),
                        type = "buttons",
                        direction="right",
                        pad={"l": 10, "t": 10},
                        showactive=True,
                        x=0.03,
                        xanchor="left",
                        yanchor="top"
                        ),     
                        ] )
                return fig
                
            return dash.no_update
        
        
        #Callback for dropdown
        @app.callback(
            Output('compare-graph', 'figure'),
            [Input(component_id='country_dropdown', component_property='value'),
            Input(component_id='country2_dropdown', component_property='value'),
            Input(component_id='start_slider', component_property='value'),
            Input(component_id='end_slider', component_property='value'),
            Input(component_id='log_type', component_property='value')]
        )
        def update_graph(country1,country2,start_date,end_date,axis_type):
            date_range = self.date_map[start_date:end_date+1]

            if country1 != 'MTL' and country2 != 'MTL':
  
                (x_data, cases_data1, _, _) = get_country_over_time_data(country1, date_range)
                (x_data, cases_data2, _, _) = get_country_over_time_data(country2, date_range)
                dates = self.date_map
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_data, y=cases_data1,
                    mode='lines+markers',
                    name='#Confirmed in ' + country1))
                
                fig.add_trace(go.Scatter(x=x_data, y=cases_data2,
                    mode='lines+markers',
                    name='#Confirmed in ' + country2))
                                
                t = f"Absolute (cumulative) cases comparison of {country1} and {country1} {dates[start_date]} to {dates[end_date-1]}"
                
                axis_type = 'linear' if axis_type == 'Linear' else 'log'
                
                fig.update_layout(title=t, xaxis_title='Day', yaxis_title='Number of confirmed cases', yaxis_type=axis_type)
                return fig
            return dash.no_update
                
        def extract_daily_increas(cum_cases):
            daily1 = np.zeros(len(cum_cases)-1)
            for i in range(len(daily1)):
                daily1[i] = cum_cases[i+1] -  cum_cases[i]
            return daily1
                
             #Callback for dropdown
        @app.callback(
            Output('daily-compare-graph', 'figure'),
            [Input(component_id='country_dropdown', component_property='value'),
            Input(component_id='country2_dropdown', component_property='value'),
            Input(component_id='start_slider', component_property='value'),
            Input(component_id='end_slider', component_property='value'),
            Input(component_id='log_type', component_property='value')]
        )
        def update_graph(country1,country2,start_date,end_date,axis_type):
            date_range = self.date_map[start_date-1:end_date+1]

            if country1 != 'MTL' and country2 != 'MTL':
  
                (x_data, cases_data1, _, _) = get_country_over_time_data(country1, date_range)
                (x_data, cases_data2, _, _) = get_country_over_time_data(country2, date_range)
                dates = self.date_map
                
                                
                daily1 = extract_daily_increas(cases_data1)
                daily2 = extract_daily_increas(cases_data2)
                
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=x_data[:-1], y=daily1,
                    name='#Confirmed in ' + country1))
                
                fig.add_trace(go.Bar(x=x_data[:-1], y=daily2,
                    name='#Confirmed in ' + country2))
                                
                t = f"Daily cases comparison of {country1} and {country2} {dates[start_date]} to {dates[end_date-1]}"
                
                axis_type = 'linear' if axis_type == 'Linear' else 'log'
                
                fig.update_layout(title=t, xaxis_title='Day', yaxis_title='Number of confirmed cases', yaxis_type=axis_type)
                return fig
            return dash.no_update
                
        port = global_code.constants.APP_PORT
        app.run_server(port=port, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
        
        logger.log('GUI Server offline')
  
class UIComponents:
    def get_country_dropdown(data_pointer, forComparison=False):
        choose_options = []
        countries = data_pointer.get_all_countries()
        for country in countries:
            entry = {'label': country, 'value': country}
            choose_options.append(entry)
        html_id =  'country_dropdown'
        if forComparison:
            html_id = 'country2_dropdown'
        dropdown = dcc.Dropdown(id=html_id,options=choose_options,value='MTL')
            
        return dropdown
    
    def get_hotspot_diagram(data_pointer, showDeaths=False):
        return html.Div(dcc.Graph(figure=UIComponents.__get__hotspot_figure(data_pointer,showDeaths)))
    
    def get_map(data_pointer):
        return dcc.Graph(figure=UIComponents.__get_map_figure(data_pointer))
    
    def get_log_checkbox():
        radio_item = dcc.RadioItems(
                id='log_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        return radio_item
        
    
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
    
    def __get__hotspot_figure(data_pointer, showDeaths): 
        data = data_pointer.get_hotspot_dataframe()
        plottype = 'Confirmed' if showDeaths == False else "Deaths"
        scale = [(0, "rgb(166,206,227)"),  (0.20, "rgb(166,206,227)"),
                 (0.20, "rgb(185, 255, 166)"),(0.40, "rgb(185, 255, 166)"),
                 (0.40, "rgb(251, 255, 166)"),(0.60, "rgb(251, 255, 166)"),
                 (0.60, "rgb(252, 208, 154)"),  (0.80, "rgb(252, 208, 154)"),
                 (0.80, "rgb(252, 154, 154)"),  (1, "rgb(252, 154, 154)"),
                 (1, "rgb(252, 154, 154)")]
         
        fig = px.bar(data, x='Country', y=plottype,
                    hover_name="Country", 
                    color=plottype,
                    color_continuous_scale=scale,
                    hover_data=["Deaths", "Recovered", "Confirmed"],
                    animation_frame="Date")
        return fig
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
            width=1400,
            height=700,
            autosize=True,
            geo=dict(
                showframe = False,
                showcoastlines = False,
            ))
        return fig