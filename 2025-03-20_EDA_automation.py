#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:03:58 2025

@author: Tiangeng Lu

Expected Output

Data: [data]
Date: [date]

Subject matter (variable) of interest. Distribution patterns, including count frequency, mean, range, and outliers.
"""
import os
import pandas as pd
from docx import Document
from docx.shared import Inches
my_data = pd.read_csv('iv_alltime.csv')
my_data.time.unique()
recent_data = my_data.set_index('time').loc['2025-01-31']
# specify the (first) variable of interest
var_1 = str('visa')
visa_totals=my_data.groupby(var_1)['count'].sum() # create a series
group_count=int(visa_totals.describe().iloc[0]) # .iloc[] to avoid warning message