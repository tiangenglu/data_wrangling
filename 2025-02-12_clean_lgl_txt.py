#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 23:24:25 2025

@author: Tiangeng Lu
"""

#import os
import numpy as np
import pandas as pd
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


# concatenated column names, needs work
colnames_raw = line_by_line[:loop_end_locations[0]][0]
print(f'raw column names:\n {colnames_raw}')
colnames_raw_list= colnames_raw.split('  ') # ['Precinct', '', '', '', '', '', '', '', '', '', '', 'Registered Voters', '', '', '', '', '', ' Ballots Cast', '', '', '', '', '', '', '', '', 'Voter Turnout', '', '', '', '', '', '', '', ' \n']
print(f'raw column names split by two spaces:\n {colnames_raw_list}')
print([len(col) for col in colnames_raw_list])
# get the finalized snake_case column names, strip(' ') to remove leading spaces and retain the non-empty and non-line-break characters
colnames_list=[col.strip(' ').replace(' ','_').lower() for col in colnames_raw_list if len(col) > 2 and not col.endswith('\n')]
print(f'After a few string manipulation steps, get the final column names: \n{colnames_list}')

split_line_by_line = [None] * (loop_end_locations[0]+1) # zero indexing
for i,line in enumerate(line_by_line[:loop_end_locations[0] + 1]):
    split_line_by_line[i] = line_by_line[i].replace('\n','').replace('%','').split('  ')
print('Print the first and last row of the data before cleaning:')    
print(split_line_by_line[0])
print(split_line_by_line[-1])

clean_line_by_line = []
# here, the range is 1, because 0 (the very first row) should be the header
for i in range(1,loop_end_locations[0] + 1):
    if split_line_by_line[i] is not None:
        clean_line_by_line.append([l.strip() for l in split_line_by_line[i] if l is not None and len(l) > 0])
print('Print the data in list form after removing the blank elements:')        
print(clean_line_by_line[:5])
print(clean_line_by_line[-5:])

summary_results = pd.DataFrame(clean_line_by_line, columns=colnames_list)
print('Create dataframe from the list, and then print the first and last several rows:')
print(summary_results.head())
print(summary_results.tail())
print('Print the dataframe info:')
print(summary_results.info())
"""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 161 entries, 0 to 160
Data columns (total 4 columns):
 #   Column             Non-Null Count  Dtype 
---  ------             --------------  ----- 
 0   precinct           161 non-null    object
 1   registered_voters  161 non-null    object
 2   ballots_cast       161 non-null    object
 3   voter_turnout      161 non-null    object
dtypes: object(4)
memory usage: 5.2+ KB
"""

data_type_summary_results = dict(zip(colnames_list,['str','int','int','float']))
print(data_type_summary_results)
summary_results = summary_results.astype(data_type_summary_results)
summary_results = summary_results.drop_duplicates() # just in case, drop duplicates
print('After changing the data type of each column, the new data info shows:')
print(summary_results.info())
# output the summary table
summary_results.to_csv('PA_York_2024_election_summary.csv', index = False)
# next steps:
# because the data contains several election results, try to single out the 2024 presidential election results
# in line_by_line, each "line" are the results of a specific precinct of a specific election








