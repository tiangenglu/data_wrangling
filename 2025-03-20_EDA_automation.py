#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:03:58 2025

@author: Tiangeng Lu

Expected Output

Data: [data]
Date: [date]

Basic: Subject matter (variable) of interest. Distribution patterns, including count frequency, mean, range, and outliers.
"""
import os
import pandas as pd
from docx import Document
from docx.shared import Inches
import time as tm
import sys
print(sys.version)
my_data = pd.read_csv('iv_alltime.csv')
print(my_data.columns)
labels = pd.read_csv('visa_directory.csv')
labels_dict = labels.set_index('SYMBOL')['CLASS'].to_dict()
my_data.time.unique()
recent_data = my_data.set_index('time').loc['2025-01-31']
# specify the (first) variable of interest
var_1 = str('visa')
var_2 = str('nationality')
# totals
visa_totals=my_data.groupby(var_1)['count'].sum() # create a series
country_totals = my_data.groupby(var_2)['count'].sum()

# check for totals
if my_data['count'].sum() == visa_totals.sum():
    print("Grand total matches the sum of all visa types.")
else:
    print("Grand total doesn't match the sum of all visa types. Check for errors.")
    
if my_data['count'].sum() == country_totals.sum():
    print("Grand total matches the sum of all nationalities.")
else:
    print("Grand total doesn't match the sum of all nationalities. Check for errors.")
    
group_count=int(visa_totals.describe().iloc[0]) # .iloc[] to avoid warning message
# max and min
visa_totals.idxmax() # index of the max value
visa_totals.max() # max of series
labels_dict[visa_totals.idxmax()]

visa_totals.idxmin()
visa_totals.min()
if visa_totals.idxmin() not in labels_dict.keys():
    print("visa descriptions unavailable.")
    labels_min = "visa descriptions unavailable."
else:
    print(labels_dict[visa_totals.idxmin()])
    labels_min = labels_dict[visa_totals.idxmin()]

country_totals.idxmax().title()
country_totals.max()

max_min = f"""\
{visa_totals.idxmax()}, known as "{labels_dict[visa_totals.idxmax()]}", has the highest number of issuance at {visa_totals.max():,}. \
{visa_totals.idxmin()}, known as "{labels_min}", has the lowest number of issuance at only {visa_totals.min():,}.
In terms of nationalities, {country_totals.idxmax().title()} has been the top recipient of immigrant visas.
"""

# monthly average



# start putting things in the output file
with open('monthly_visa_summary.txt', 'w') as file:
    print(max_min)
    file.write(tm.strftime("%Y-%m-%d, %A\n\n"))
    file.write(max_min)
    file.write("\nGenerated in Python")
    file.close()


