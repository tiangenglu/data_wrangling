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

# summary statistics, do not merge tables yet.
# adding variable label info by merging tables

# stem vs non-stem
def stem(x):
    if x == 'XXXX' or x == '****':
        return '0'
    else: return '1'

df['stem_flag'] = df.apply(lambda row: stem(row['STEMOCC']), axis = 1)
df_stem_describe = round(df[['SALARY']].groupby(df['stem_flag']).describe(),2)

# stem occupation frequency
stem_occ_freq = df_stem[['OCC']].value_counts().to_frame().reset_index().merge(occ[['OCC', 'OCCT','OCCFAM','OCCFAMT']], on = 'OCC')

# stem occupation frequency by broader job families
stem_fam_freq = stem_occ_freq.groupby(['OCCFAM', 'OCCFAMT'])[['count']].sum().reset_index()

# stem salary by occupation
stem_occ_sal = round(df_stem.groupby(['OCC'])['SALARY']\
                     .agg(['count','median', 'mean', 'std','max','min', 'sum']), 2).reset_index()\
    .merge(occ[['OCC', 'OCCT','OCCFAM','OCCFAMT']], on = 'OCC')\
        .sort_values(['sum','median','mean','std'], ascending = False)\
            .reset_index(drop = True)[['OCC', 'OCCT','OCCFAM','OCCFAMT', 'count','median', 'mean','max','min', 'std', 'sum']]
# stem salary by job family
stem_fam_sal = df_stem.merge(occ[['OCC', 'OCCT','OCCFAM','OCCFAMT']], on = 'OCC')\
    .groupby(['OCCFAM','OCCFAMT'])['SALARY']\
        .agg(['count','median', 'mean', 'std','max','min', 'sum'])\
            .reset_index()

# job family by agency

agy_fam_freq = df_stem[['SALARY','OCC', 'AGYSUB']]\
    .merge(occ[['OCC', 'OCCT','OCCFAM','OCCFAMT']], on = 'OCC')\
        .merge(agy[['AGYSUB', 'AGYSUBT']], on = 'AGYSUB')\
            .pivot_table(index = ['AGYSUBT'],
                         columns = ['OCCFAM'],
                         values = 'SALARY',
                         aggfunc = 'count',
                         fill_value = 0, margins = True).reset_index()

agy_med_sal = df_stem[['SALARY','OCC', 'AGYSUB']]\
    .merge(occ[['OCC', 'OCCT','OCCFAM','OCCFAMT']], on = 'OCC')\
        .merge(agy[['AGYSUB', 'AGYSUBT']], on = 'AGYSUB')\
            .pivot_table(index = ['AGYSUBT'],
                         columns = ['OCCFAM'],
                         values = 'SALARY',
                         aggfunc = 'median',
                         fill_value = 0).reset_index()            

with pd.ExcelWriter('opm_summary.xlsx') as writer:
    df_stem_describe.to_excel(writer, sheet_name = 'stem_desc')
    stem_occ_freq.to_excel(writer, sheet_name = 'occ_freq', index = False, freeze_panes = (1, 0))
    stem_fam_freq.to_excel(writer, sheet_name = 'occ_jobfam', index = False)
    stem_occ_sal.to_excel(writer, sheet_name = 'occ_sal', index = False)
    stem_fam_sal.to_excel(writer, sheet_name = 'jobfam_sal', index = False)
    agy_fam_freq.to_excel(writer, sheet_name = 'jobfam_agy', index = False)
    agy_med_sal.to_excel(writer, sheet_name = 'agy_med_sal', index = False)


