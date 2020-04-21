#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:24:53 2020

@author: lukas
""" 
class IOLogger():
    def __init__(self, debug_level):
        self.debug_level =  debug_level
    
    def log(self, msg, debug_level=1):
        if debug_level <= self.debug_level:
            print('[LOG] {}'.format(msg))
            