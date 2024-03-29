#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 01:46:36 2024

multi_sheet_formatted_excel

@author: Tiangeng Lu
"""

import numpy as np
import pandas as pd
import time as tm

# how many staff members?
staff_num = 3
roster = ['staff_'+str(num)
          for num in [num for num in range(1,staff_num + 1)]]
print(roster)
pp_begin = pd.date_range('2024-01-14', '2025-01-11', freq = '14D').to_series()
# a pandas series has index, here the index equals to row values
print(pp_begin.head(2))
pp_end = pd.date_range('2024-01-27', '2025-01-11', freq = '14D').to_series()
print(pp_end.head(2))
pp = np.repeat([num for num in np.arange(1, len(pp_end)+1)], 14)
df1 = pd.DataFrame({
    'date': pd.date_range('2024-01-14', '2025-01-11', freq = 'D').strftime('%b %d'),
    'day': pd.date_range('2024-01-14', '2025-01-11', freq = 'D').strftime('%a'),
    'week': pd.date_range('2024-01-14', '2025-01-11', freq = 'D').isocalendar().week,
    'PP': pp
})
# remove weekends
df1 = df1[~df1['day'].isin(['Sat', 'Sun'])]
# create a blank dataframe
df2 = pd.DataFrame(index = df1.index,
                   columns = ['work_time', 'leave_time', 'total_hours'])
# nrow = number of work days
print(f'The shape of df2(schedule) is {df2.shape}')
# padding column between staff members
df_blank = pd.DataFrame(index = df1.index, columns = ['  '])
# blank colname and blank values
df_blank['  '] = ''
df3 = pd.concat([df_blank, df2], axis = 1)
# set index with pay period, date, and day of a week
df3 = df3.set_index([df1['PP'], df1['date'], df1['day']])
# multiply df3 by the number of staff members
df4 = pd.concat([df3] * len(roster), axis = 1, keys = roster)
# split
df_list = [None] * len(pp_end)
# split into multiple dataframes by pay period
for i in range(len(pp_end)):
    # zero indexing, i + 1 to start from 1 for the PP(1-26) index
    df_list[i] = df4.loc[i+1, :, :]

# add padding blank rows between two weeks
df_blank_row = pd.DataFrame(
    # '.' has to be there to avoid the cells to be undesirably merged
    # duplicate single-row still has the merge in output
    index = pd.MultiIndex.from_tuples([(' ',' '),('.',' ')], names = ['date', 'day']),
    columns = df_list[0].columns)

df_list_format = [None] * len(pp_end)
# continue formatting, insert blank rows between two weeks
# .iloc[5:] is the 2nd week, from the 5th work day to end
for i in range(len(pp_end)):
    df_list_format[i] = pd.concat([df_list[i].iloc[:5], 
                                  df_blank_row,
                                  df_list[i].iloc[5:]
                                  ])
# work on excel columns
single_letters = [chr(x) for x in range(65,91)] # A-Z
# after column Z, followed by AA, AB...AZ columns
double_letters = ['A'+letter for letter in single_letters]
xlsx_col_seq = single_letters + double_letters
print(xlsx_col_seq)
table_width = len(df_list[0].index[0]) + df_list[0].shape[1]
print(f'The output table has {table_width} columns,\
corresponding to the {xlsx_col_seq[table_width - 1]} column.')
# Get the desired column position for the total hours for each staff.
# How many columns does each staff member occupy?
col_nums = [xlsx_col_seq.index('E') + df3.shape[1] * num for num in range(staff_num)]
print(f'''The zero-indexed column number for calculated total hours 
      are: {col_nums}''') # triple quotes for multi-line strings
# prepare the total mini-table
col_letters = []
for i in col_nums:
    letter = xlsx_col_seq[i]
    col_letters.append(letter)
print(f'The cell for calculated total hours are in the following columns: {col_letters}')   
# the content value starts from the 5th row (1st work day)
# the content value ends with the 16th row (last work day)
f_values = [f'=SUM({xlsx_col_seq[i]}5:{xlsx_col_seq[i+1]}16)' for i in col_nums]
print(f'The cells that will be formatted are: {f_values}')
# add a new one-cell data frame to calculate the total hours for each staff
# in the output excel, the total hours will be calculated using the SUM()
df_total_list = [None] * len(roster) # same as the number of staff members
for i in range(len(df_total_list)):
    df_total_list[i] = pd.DataFrame(index = ['TOTAL'], columns = ['TOTAL'])
    df_total_list[i].iloc[0,0] = f_values[i] 
# generate a list of sheet titles
sheet_title_list = [None] * len(df_list_format)
for i in range(len(df_list_format)):
    # pp_begin & pp_end are series, use .iloc[i] to index
    sheet_title_list[i] = f'PAY PERIOD {i+1}: {pp_begin.iloc[i].date()} to {pp_end.iloc[i].date()}'

##### FINAL OUTPUT #####
with pd.ExcelWriter('format_excel_py.xlsx') as writer:
    # set the `.book` method of writer(output excel file)
    workbook = writer.book # to add_format later
    for i in range(len(df_list_format)):
        df_list_format[i].to_excel(writer,
                                  sheet_name = 'PP'+str(i+1),
                                  startrow=1,
                                  freeze_panes=(4,2))
        # a specific sheet of an excel workbook
        worksheet = writer.sheets['PP'+str(i+1)] # point to specific sheet
        header_format = workbook.add_format({"bold":True,
                                             "text_wrap":False,
                                             "font_size":15,
                                             "valign": 'vcenter',
                                             'align': 'center',
                                             'border': 1,
                                             'fg_color': '#cfe2f3'}) # slightly deeper #9fc5e8
        # within the specific sheet, format targeted rows & columns
        worksheet.set_column(first_col=0, last_col=2, width=7) # column A & B width 6
        worksheet.set_column(first_col=3, last_col=table_width-1, width=9) # from col, to col, column width
        # (2,1,3,3, first_row, first_col, last_row, last_col, zero-index)
        worksheet.merge_range(0,0,0,table_width-1, sheet_title_list[i],
                              header_format)
        worksheet.set_row(3,None,None, {'hidden': True})
        # autofit
        #worksheet.autofit() # void the set_column codes
        # add comment
        worksheet.write_comment(row=16, col=0,
                                comment =  tm.strftime('%Y-%m-%d, %a, %H:%M'))
        for j in range(len(df_total_list)):
            df_total_list[j].to_excel(writer,
                                      sheet_name = 'PP'+str(i+1),
                                      startrow=17, 
                                      startcol=col_nums[j],
                                      header = None)

del(df1, df2, df3, df4, df_list, df_list_format, df_total_list, df_blank, df_blank_row)