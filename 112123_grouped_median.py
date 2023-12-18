#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:31:31 2023

@author: Tiangeng Lu

"""

import numpy as np
import pandas as pd

def grouped_median(df, sorted_class, var, I = 1):
    """
    

    Parameters
    ----------
    df : data.frame
        Takes a dataframe that contain at least two variables: sorted_class and var.
    sorted_class : variable from the data
        Numeric intervals such as age and test scores.
    var : numeric variable from the data frame
        The numeric values of the specific sorted_class.
    I : optional interval
        The default is 1.
    L: lower limit of the median interval
    
    N: total number of data points
    
    CF: number of data points BELOW the median interval
    
    F: number of data points IN the mdian interval
    
    grouped median = L + I * (0.5 * N - CF) / F

    Returns a single-row data frame
    -------
    Prerequisite: (1) the var column must be numeric. (2) the var column cannot be all zeros.

    """
    df = df.sort_values(sorted_class, ascending = True).reset_index(drop = True)
    df['cum'] = np.cumsum(df[var])
    while not df[var].var() == 0 & df[var].sum() == 0:
        L = df[sorted_class][df['cum'] >= df[var].sum() / 2].min
        CF = df['cum'][df[sorted_class] == L - 1].iloc[0]
        F = df[var][df[sorted_class] == L].iloc[0]
        N = df[var].sum()
        grouped_median = L + I * (0.5 * N - CF) / F
        output_df = pd.DataFrame.from_dict([{'L': L, 'CF': CF, 'F': F, 'N': N, 'median': grouped_median}])
    return output_df