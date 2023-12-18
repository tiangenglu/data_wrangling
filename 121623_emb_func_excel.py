#!/usr/bin/env python
# coding: utf-8
"""
Created on Sun Dec 17, 2023

@author: Tiangeng Lu

- To create a multi-tab excel output with embedded functions in specific cells
- The following creates a timesheet template of 26 pay periods for seven employees
    - The dates and days of week are provided in the tab for each pay period
    - There is an embedded function in the output excel tab that sums the total hours in one period for each employee.

"""

import os
import numpy as np
import pandas as pd

roster = ['Alice', 'Bob', 'Cathy', 'David', 'Ethan', 'Francis', 'Gaby']

df1 = pd.DataFrame(
    {'date': pd.date_range('2024-01-01', '2024-12-31', freq = 'D')\
     .strftime('%Y-%m-%d'),
     'day': pd.date_range('2024-01-01', '2024-12-31', freq = 'D')\
     .to_series().dt.day_name(),
     'week': pd.date_range('2024-01-01', '2024-12-31', freq = 'D')\
     .isocalendar().week})
df1['PP'] = np.ceil(df1['week'] / 2).astype(int)
# remove the last few days in the year that would count into the next year
df1 = df1.iloc[: 14 * 26]
# remove Sundays
df1 = df1[df1['day'] != 'Sunday']

df2 = pd.DataFrame(index = df1.index, columns = ['in', 'out', 'hours'])

df_blank = pd.DataFrame(index = df1.index, columns = ['  '])
df_blank['  '] = ''
df_blank.head(2)

df3 = pd.concat([df2, df_blank], axis = 1)
# order of index matters, put PP in the first place, it'll be gone after split
df3 = df3.set_index([df1['PP'], df1['date'], df1['day']])
# for all employees
df4 = pd.concat([df3] * len(roster), axis = 1, keys = roster)
# split the big dataframe into 26 pay periods
df_list = [None] * 26
for i in range(len(df_list)):
    # be aware of zero indexing, use i + 1 to get PP = 1
    df_list[i] = df4.loc[i + 1, :, :]

df_blank_row = pd.DataFrame(
    index = pd.MultiIndex.from_tuples([(' ', ' ')]),
    columns = df_list[0].columns)
df_blank_row

df_list_format = [None] * 26
for i in range(len(df_list_format)):
    df_list_format[i] = pd.concat([df_list[i].iloc[:6],
                                   df_blank_row,
                                   df_list[i].iloc[6:],
                                   df_blank_row])

single_letters = [chr(x).upper() for x in range(97, 123)]
double_letters = ['A' + lett  for lett in single_letters]
xlsx_col_seq = single_letters + double_letters
# How many columns does each person take?
col_nums = [xlsx_col_seq.index('E') + 4 * num for num in range(7)]
# get column letters
col_letters = []
for i in col_nums:
    letter = xlsx_col_seq[i]
    col_letters.append(letter)
print(col_nums)    
print(col_letters)

df_total_list = [None] * len(roster)
# list comprehension to embed excel functions
f_values = [f'=SUM({col}4:{col}9,{col}11:{col}16)' for col in col_letters]
print(f_values)

df_total_list = [None] * len(roster)
for i in range(len(df_total_list)):
    df_total_list[i] = pd.DataFrame(index = ['TOTAL'], columns = ['TOTAL'])
    df_total_list[i].iloc[0, 0] = f_values[i]
# i loops over 26 pay periods, j loops over all employees
with pd.ExcelWriter('timesheet_v2.xlsx') as writer:
    for i in range(len(df_list_format)):
        df_list_format[i].to_excel(writer,
                                   sheet_name = 'PP' + str(i+1),
                                   freeze_panes= (3,2))
        for j in range(len(df_total_list)):
            df_total_list[j].to_excel(writer,
                                     sheet_name='PP' + str(i+1),
                                     startrow = 18,
                                     startcol = col_nums[j],
                                     header = None)