"""
Created on 2024-02-29
Created by Tiangeng Lu
HAPPY LEAP DAY 2024!
"""
import pandas as pd
df = pd.read_csv('/Users/tiangeng/Public/opm_202309/FACTDATA_SEP2023.TXT',
                dtype = 
                {'AGYSUB': str,
 'LOC': str,
 'AGELVL': str,
 'EDLVL': str,
 'GSEGRD': str,
 'LOSLVL': str,
 'OCC': str,
 'PATCO': str,
 'PP': str,
 'PPGRD': str,
 'SALLVL': str,
 'STEMOCC': str,
 'SUPERVIS': str,
 'TOA': str,
 'WORKSCH': str,
 'WORKSTAT': str,
 'DATECODE': float,
 'EMPLOYMENT': float,
 'SALARY': float})

# removed PP, EMPLOYMENT, GSEGRD, DATECODE
df = df[['AGYSUB', 'LOC', 'AGELVL', 'EDLVL', 'LOSLVL', 'OCC', 'PATCO',
       'PPGRD', 'SALLVL', 'STEMOCC', 'SUPERVIS', 'TOA', 'WORKSCH',
       'WORKSTAT','SALARY', 'LOS']]

# get STEM entries
df_stem = df[~df['STEMOCC'].isin(['XXXX', '****'])].reset_index(drop = True)
df_stem.drop(['STEMOCC'], axis = 1, inplace = True)
print(df_stem.columns)