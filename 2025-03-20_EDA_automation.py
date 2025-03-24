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
import datetime as dt # dt.date
from datetime import datetime # different from above
import sys
print(sys.version)
# create a handy function to print out last modified time of a file in an easy-to-read time format
def dtime(file):
    return datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d, %A, %H:%M:%S")
# done w/ packages and functions, data work begins
file_path = 'iv_alltime.csv'
my_data = pd.read_csv(file_path)
print(f'Data last modified time: {dtime(file_path)}')
my_data['time']=pd.to_datetime(my_data['time']).dt.date
# make sure the 'time' column has been converted to datetime format
collection_start_month = my_data['time'].min().strftime("%B, %Y") # 'March, 2017'
collection_cutoff_month = my_data['time'].max().strftime("%B, %Y")
print(my_data.info())
# visa descriptions, also scraped, see https://github.com/tiangenglu/WebScrape/blob/main/06222023_visa_descriptions.py
labels = pd.read_csv('visa_directory.csv')
labels_dict = labels.set_index('SYMBOL')['CLASS'].to_dict()
# subset the most recent monthly data
recent_data = my_data.loc[my_data['time'] == my_data['time'].max()].reset_index(drop = True)
recent_total=recent_data['count'].sum()
# How many months does the dataframe cover?
num_months_covered = len(my_data['time'].unique())
# Series of monthly totals
monthly_totals = my_data.groupby('time')['count'].sum()
max_month = monthly_totals.idxmax().strftime("%B, %Y") # month w/ highest visa issuance
min_month = monthly_totals.idxmin().strftime("%B, %Y") # month w/ lowest visa issuance
# summary statistics, convert to integer
monthly_summary = monthly_totals.describe().astype('int') # mean 1, sd 2, min 3, median 5, max 7

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
    
total_visa_types=int(visa_totals.describe().iloc[0]) # .iloc[] to avoid warning message

# overview
overview = f"""\
DISCLAIMER:\n
This summary is based on web-scraped data. It does not represent the official statistics. \
This program is part of an automated workflow from web-scraping raw data to a structured statistical report. \n
Overview:\n
Data were last scraped and cleaned at {dtime(file_path)}. \
The current data table covers between {collection_start_month} and {collection_cutoff_month}. \
The data has issuance records of {total_visa_types} unique immigrant visa classes.
"""

# highlights
if monthly_totals.iloc[-1] > monthly_summary.iloc[5]: # compared median
    latest_pattern = "is higher than"
elif monthly_totals.iloc[-1] == monthly_summary.iloc[5]:
    latest_pattern = "equals to"
else: latest_pattern = "is lower than"

latest_diff_median = abs(monthly_totals.iloc[-1] - monthly_summary.iloc[5])

highlights = f"""\
In {collection_cutoff_month}, {monthly_totals.iloc[-1]:,} immigrant visas were issued. \
This number {latest_pattern} the median by {latest_diff_median:,}.
"""


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

# start putting things in the output file
with open('monthly_visa_summary.txt', 'w') as file:
    file.write("Summary of Monthly Immigrant Visa Issuance\n")
    file.write(tm.strftime("%Y-%m-%d, %A\n\n"))
    file.write(overview)
    file.write(highlights)
    file.write(max_min)
    file.write("\nGenerated in Python")
    file.close()


