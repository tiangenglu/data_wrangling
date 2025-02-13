#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 23:24:25 2025

@author: Tiangeng Lu
"""

#import os
import numpy as np
#import pandas as pd
# read in uncleaned .txt detail data of York County election results
line_by_line = []
with open("detail.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        line_by_line.append(line)
        
# Get a list of boroughs/townships by printing the first 30 characters from each component
l_start=[l[:30].strip() for l in line_by_line]

# Get the number of characters(length) of each line
char_length = [len(l) for l in line_by_line ]
print('min length:',min(char_length),'max length:',max(char_length))

# in the uncleaned data, if the length of the line is 1, then it's a line breaker
print("Which are the elements with length 1?\n",[l for l in line_by_line if len(l)==1])

# try to get a list of precincts (boroughs/towns)
# 'Total:' was identified from eyeballing the data
mark_location_by_idx = l_start.index('Total:')
print(f"""Where does the end of the list of all precints? 
      There're {mark_location_by_idx - 1} boroughs, cities, or townships in York County results.""")
      
all_precincts=l_start[1:mark_location_by_idx]
print(len(all_precincts))      
      
# use one of the unique town names and count its frequency.
# This is because it's a combined and detailed dataset with all election results of all precincts.
l_start.count('Carroll Township')

# the last precinct?
print(f'Last precinct in the list: {all_precincts[-1]}')

# locate the location of the end of each iteration?
print(l_start.index(all_precincts[-1])) # This only returns the first occurrence

# use np.where(element == 'pattern')[0] to identify all indeces
l_start_array = np.array(l_start)
loop_end_locations = np.where(l_start_array == all_precincts[-1])[0]
print(f'This is the output without indexing[0]: {np.where(l_start_array == all_precincts[-1])}')
print(f'This is the (correct) output when indexing[0] from np.where: {loop_end_locations}')
# to be continued







