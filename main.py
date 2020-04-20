#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:24:53 2020

@author: lukas
"""

#import the visualization components
from data_layer import DataLayer
from gui import GUI

import global_code


#load the data and connect it to the GUI. 
#the GUI might have its own ViewController.

#load data
data_name = 'covid19_data.csv'
data_path = global_code.constants.DATA_PATH + data_name #this might be changeable by the UI
data = DataLayer(data_path)

#show user interface, that has a conection to the data layer
gui = GUI(data)
gui.showUI()