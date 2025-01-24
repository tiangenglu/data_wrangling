#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 2025

@author: Tiangeng Lu

Download geo shape files from https://www2.census.gov/geo/tiger/TIGER2024/
Unzip
"""
# create the folder if haven't done it yet
import os
if not os.path.exists(r'tiger2024'):
    os.makedirs('tiger2024')
else: print('Folder exists.')
# change directory to the new folder
os.chdir('tiger2024')
# check system version
import sys
print(sys.version)
import time as tm # create time stamps for each iteration

import requests # .get().content from a url
from scrapy import Selector # Selector(text =)
from urllib import request # .urlretrieve(url, filename)

main_url = "https://www2.census.gov/geo/tiger/TIGER2024/TABBLOCK20/"
main_html = requests.get(main_url).content
main_selector = Selector(text = main_html)
# get the target objects to download
all_links = main_selector.xpath(query = '//*[contains(@href, ".zip")]/@href').extract()
# get the FULL valid urls with "http"
full_urls = [main_url + link for link in all_links if not link.startswith('http')]
# start the download
for i in range(len(all_links)):
    if os.path.exists(all_links[i]):
        print(f"File {all_links[i]} exists.")
    else:
        print(f'Now downloading {all_links[i]}, {tm.strftime("%Y-%m-%d, %H:%M:%S")}')
        request.urlretrieve(full_urls[i], all_links[i])

# Extract downloaded zipped files
from zipfile import ZipFile
zip_files_list = [f for f in os.listdir() if f.endswith(".zip")]
folder_names = [f.split(".")[0] for f in zip_files_list]

# create folders
for i in range(len(zip_files_list)):
    if not os.path.exists(folder_names[i]):
        os.makedirs(folder_names[i])
    else:
        print(f"Folder {folder_names[i]} exists.")

# unzip
for i in range(len(zip_files_list)):
    if len(os.listdir(folder_names[i])) < 1:
        with ZipFile(zip_files_list[i]) as zip_need_extract:
            print(f'Processing {zip_files_list[i]}, {tm.strftime("%Y-%m-%d, %H:%M:%S")}')
            zip_need_extract.extractall(path = folder_names[i])
    else: 
        print(f'{zip_files_list[i]} has been extracted.')
        print(os.listdir(folder_names[i]))