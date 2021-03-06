#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:24:53 2020

@author: lukas
"""

#imports
import pandas as pd
import global_code

#Data columns as a variable struct
class Columns:
    SNO = 'SNo'
    OBSERVATION_DATE = 'ObservationDate' 
    PROVINCE = 'Province/State'
    COUNTRY = 'Country/Region'
    LAST_UPDATE = 'Last Update'
    CONFIRMED = 'Confirmed'
    DEATHS = 'Deaths'
    RECOVERED = 'Recovered'
    ALL = [SNO, OBSERVATION_DATE, PROVINCE, COUNTRY, LAST_UPDATE, CONFIRMED, DEATHS, RECOVERED]

logger = global_code.getLogger()


#start code
class DataLayer:
    '''
        Handles all data access
    
        ## documentation about all fields stored: ## 
            -dataframe
                contains basically all data as table
            -all_countries
                a list of all countries were data is available
            -province_mapping
                a list for each country of its subregion/regions
                e.g. province_mapping = ['USA':['Massach.', 'Ohio', ..], 'Spain':[..], ..]
            -total_days_recorded
                for each day recored 1 entry n format 'MM/DD/YYYY'
            -accum_deaths_for_day
                a mapping of accumuated deaths per day [03/27/2020:151, 03/28/2020:162,..]
            -accum_recovery_for_day
                a mapping of accumuated recovery per day [03/27/2020:151, 03/28/2020:162,..]
            -accum_confirms_for_day
                a mapping of accumuated confirmed cases per day [03/27/2020:151, 03/28/2020:162,..]
            
    '''


    def __init__(self, datafile):
        #load the data given
        #strore it in a more specific data format
        #anser querys from VierController
        self.__process_input_data(datafile)
        
    
    #--- private util mehods -----------------------------------------------------
    def __process_input_data(self, datafile):
        logger.log('Preprocessing data structures..')
        dframe  = pd.read_csv(datafile)
        self.dataframe = dframe
        
        
        #get all countries
        countries = dframe[Columns.COUNTRY].unique()
        self.all_countries = countries
        
        
        #add all provinces to country
        self.province_mapping = {}  
        for country in self.all_countries:
            country_indices = dframe[Columns.COUNTRY] == country
            provinces = dframe[country_indices][Columns.PROVINCE].unique()
            self.province_mapping[country] = list(provinces)
            
        #get all dates available    
        self.total_days_recorded = dframe[Columns.OBSERVATION_DATE].unique()
                
        #for each day, record how many people died, recovered or infected
        
        self.accum_deaths_for_day = {}
        self.accum_recovery_for_day = {}
        self.accum_confirms_for_day = {}
        
        for day in self.total_days_recorded:
            current_day_indices = dframe[Columns.OBSERVATION_DATE] == day
            total_day_deaths = dframe[current_day_indices][Columns.DEATHS].sum()
            total_day_recovers = dframe[current_day_indices][Columns.RECOVERED].sum()
            total_day_confirmed = dframe[current_day_indices][Columns.CONFIRMED].sum()
            
            self.accum_deaths_for_day[day] = total_day_deaths
            self.accum_recovery_for_day[day] = total_day_recovers
            self.accum_confirms_for_day[day] = total_day_confirmed
            
        #example filter
#        datafilter1 = dframe[Columns.DEATHS] > 100
#        datafilter2 = dframe[Columns.PROVINCE] == 'Hubei'
#        print(dframe[datafilter1 & datafilter2].head(5))
        
        logger.log('Preprocessing geomap')
        self.geo_map_dataframe = self.dataframe.rename(columns={'Country/Region':'Country'}) #copy & rename  
        self.geo_map_dataframe.rename(columns={'ObservationDate':'Date'}, inplace=True) #only rename
        
        
        logger.log('Preprocessing finished')
        
        
    #--- public mehods -----------------------------------------------------------
    def get_map_dataframe(self):
        final_df = self.geo_map_dataframe[self.geo_map_dataframe['Confirmed']>0]
        return final_df.groupby(['Date','Country']).sum().reset_index()
        
    def get_hotspot_dataframe(self):
        final_df = self.geo_map_dataframe[self.geo_map_dataframe['Confirmed']>0]
        all_data = final_df.groupby(['Date','Country']).sum().reset_index()
        last_day_data =  all_data[ all_data['Date'] == self.get_as_of_date() ]
        hotspot_filtered = last_day_data[last_day_data['Confirmed'] > global_code.constants.HOTSPOT_NUM]
        hotspot_countries = list(hotspot_filtered['Country'])
        
        hotspot_data = all_data[ all_data['Country'].isin(hotspot_countries) ]
        start = global_code.constants.HOTSPOT_START
        hotspot_data = hotspot_data[hotspot_data['Date'] > self.get_all_days_recorded()[start]]
        return hotspot_data
    
    def get_as_of_date(self):
        no_days = len(self.total_days_recorded)
        return self.total_days_recorded[no_days - 1]
    
    def get_all_days_recorded(self):
        return self.total_days_recorded
    
    def get_all_countries(self):
        return self.all_countries
    
    #Extend methods here as needed