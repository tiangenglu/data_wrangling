"""
Created on 2024-02-29
Created by Tiangeng Lu
HAPPY LEAP DAY 2024!
"""
import pandas as pd
# main table
df = pd.read_csv('/Users/tiangeng/Public/opm_202309/FACTDATA_SEP2023.TXT',
                dtype = 
                {'AGYSUB': str, # join w/ agency table
                 'LOC': str, # location, d_loc
                 'AGELVL': str, # age
                 'EDLVL': str, # edu
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

# agency table
# AGYTYP,AGYTYPT,AGY,AGYT,AGYSUB,AGYSUBT
agy = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTagy.txt',
                  dtype = {
                      'AGYTYP': str,
                      'AGYTYPT': str,
                      'AGY': str,
                      'AGYT': str, 
                      'AGYSUB': str, # join
                      'AGYSUBT': str
                      })

# location table
# LOCTYP,LOCTYPT,LOC,LOCT
d_loc = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTloc.txt',
                    dtype = {
                        'LOCTYP': str,
                        'LOCTYPT': str,
                        'LOC': str, # join
                        'LOCT': str
                        })
# age
# AGELVL,AGELVLT
age = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTagelvl.txt',
                  dtype = {
                      'AGELVL': str, # join
                      'AGELVLT': str
                      })

# education level
# EDLVLTYP,EDLVLTYPT,EDLVL,EDLVLT
edu = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTedlvl.txt',
                  dtype = {
                      'EDLVLTYP': str,
                      'EDLVLTYPT': str,
                      'EDLVL': str, # join
                      'EDLVLT': str
                      })


# occupation
# OCCTYP,OCCTYPT,OCCFAM,OCCFAMT,OCC,OCCT
occ = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTocc.txt',
                  dtype = {
                      'OCCTYP': str,
                      'OCCTYPT': str,
                      'OCCFAM': str,
                      'OCCFAMT': str,
                      'OCC': str, # join
                      'OCCT': str
                      })

# occupation category
patco = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTpatco.txt',
                    dtype = {
                        'PATCO': str,
                        'PATCOT': str
                        })

# supervisory status
# SUPERTYP,SUPERTYPT,SUPERVIS,SUPERVIST
d_super = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTsuper.txt',
                      dtype = {
                          'SUPERTYP': str,
                          'SUPERTYPT': str,
                          'SUPERVIS': str,
                          'SUPERVIST': str
                          })
# type of appt
# TOATYP,TOATYPT,TOA,TOAT
toa = pd.read_csv('/Users/tiangeng/Public/data/opm_202309/DTtoa.txt',
                  dtype = {
                      'TOATYP': str,
                      'TOATYPT': str,
                      'TOA': str,
                      'TOAT': str
                      })
# end of data import

