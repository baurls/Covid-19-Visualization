#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:24:53 2020

@author: lukas
"""

class DataLayer:
    def __init__(self, datafile):
        #load the data given
        #strore it in a more specific data format
        #anser querys from VierController
        self.__process_input_data(datafile)
        
    
    #--- private util mehods -----------------------------------------------------
    def __process_input_data(datafile):
        pass
    
    
    
    #--- public mehods -----------------------------------------------------------
    
        # accumulated data
    
    def total_death_trend_data_for(incl_timeinterval): #see global code for interval
        start = incl_timeinterval.start
        end = incl_timeinterval.end
        #todo
        return None
    
    def total_recovered_trend_data_for(incl_timeinterval): #see global code for interval
        start = incl_timeinterval.start
        end = incl_timeinterval.end
        #todo
        return None
    
    def total_infected_trend_data_for(incl_timeinterval): #see global code for interval
        start = incl_timeinterval.start
        end = incl_timeinterval.end
        #todo
        return None
    
    
        # location data
    
    def infected_in_country_for(country, incl_timeinterval):
        #returns the number of infections in a country within the given time interval 
        #todo
        return None