#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3
import io
import getpass
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
print(sys.version)


# # s3 connection

# In[2]:


my_aws_access_key_id = '{0}'.format(getpass.getpass('aws_access_key_id: '))
my_aws_secret_access_key = '{0}'.format(getpass.getpass('aws_secret_access_key: '))


# In[3]:


my_bucket = my_bucket = '{}'.format(getpass.getpass('bucket_name: '))


# In[4]:


session = boto3.Session(profile_name = None, region_name = 'us-east-2')
s3 = session.client('s3',
                    aws_access_key_id = my_aws_access_key_id,
                    aws_secret_access_key = my_aws_secret_access_key)


# In[5]:


files_content = s3.list_objects(Bucket = my_bucket)['Contents']
file_names = [file['Key'] for file in files_content]


# In[6]:


# view objects
s3.list_objects(Bucket = my_bucket).keys()


# In[7]:


# contents
files_content


# # Retrieve data

# In[8]:


data_object = s3.get_object(Bucket = my_bucket, Key = 'gs_summary.csv')
data_object


# In[9]:


data_object_read = data_object['Body'].read()
type(data_object_read)


# In[10]:


io.BytesIO(data_object['Body'].read())


# In[11]:


df_gs = pd.read_csv(io.BytesIO(data_object_read), low_memory=False)


# In[12]:


df_gs.head(3)


# In[13]:


df_gs.isnull().sum()[df_gs.isnull().sum() > 0]


# # Summary statistics

# In[14]:


def p10(x):
    return x.quantile(.1)
def p25(x):
    return x.quantile(.25)
def p75(x):
    return x.quantile(.75)
def p90(x):
    return x.quantile(.9)


# In[15]:


df_gs.groupby(['stem'])['salary'].agg(['mean','std',
                                       p10, p25,'median', p75, p90]).round()


# In[16]:


np.nanpercentile(df_gs['salary'], [10, 25, 50, 75, 90])


# In[17]:


df_gs.groupby(['stem'])['gs'].agg(['mean', p25, 'median', p75]).round(1)


# In[18]:


gs1530 = df_gs.loc[df_gs['occ'] == '1530'].reset_index(drop = True)


# In[19]:


gs1530[['salary', 'los']].agg(['mean','std', p10, p25,'median', p75, p90]).round()


# In[20]:


gs1530['gs'].value_counts(normalize=True).sort_index()\
.plot(kind = 'bar', figsize = (10, 4), grid = True)
plt.xlabel('grade')
plt.title('GS-1530 Statisticians')
plt.show()


# # Upload dataframe to s3

# In[21]:


s3.put_object(Body = gs1530.to_csv(index = False), Bucket = my_bucket, Key = 'gs1530.csv')

# upload local file
s3.upload_file('median_salary_occ.csv', my_bucket, 'med_salary_occ.csv')