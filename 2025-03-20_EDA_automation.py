#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:03:58 2025

@author: Tiangeng Lu
"""
import os
import pandas as pd
from docx import Document
from docx.shared import Inches
my_data = pd.read_csv('iv_alltime.csv')
my_data.time.unique()
recent_data = my_data.set_index('time').loc['2025-01-31']

visa_totals=my_data.groupby('visa')['count'].sum()