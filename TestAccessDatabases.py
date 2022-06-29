#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 20:46:41 2022

created in sypder

@author: alp 
"""

# this is based on https://dev.socrata.com/blog/2016/02/02/plotly-pandas.html
# I want to explore CDPS crash data about bicycles
#

import pandas as pd
import numpy as np
import matplotlib
#import cufflinks as cf
#import plotly
#import plotly.offline as py
#import plotly.graph_objs as go

#cf.go_offline() # required to use plotly offline (no account required).
#py.init_notebook_mode() # graphs charts inline (IPython).

url= "https://data.cityofchicago.org/resource/85ca-t3if.json?$$app_token=5I2MKS1rZ49obGC9dtfgr2Pgi$where=crash_date%20between$20'2021-01-01T00:00:00'%20and%20'2022-01-01T00:00:00'"
# this URL generates an "invalid app token error" but the app token is cut-and-pasted from CHI's website

url2="https://data.cityofchicago.org/resource/85ca-t3if.json?$where=crash_date%20between%20%272021-01-01T00:00:00%27%20and%20%272022-01-01T00:00:00%27"
# this URL works, but is throttled to 1000 records

crashes = pd.read_json(url)

cyclist = crashes[crashes['first_crash_type'] == 'PEDALCYCLIST']
dooring = crashes[crashes['dooring_i'].notna()]


from sodapy import Socrata
client=Socrata('data.cityofchicago.org','5I2MKS1rZ49obGC9dtfgr2Pgi')
# chicago data, App_token
results=client.get('85ca-t3if',limit=2000)
# this works - pulls 2K crash records

results=client.get('85ca-t3if',where='first_crash_type == PEDALCYCLIST',limit=2000)
# generates an error -- can't find the column name, but it is there!

results=client.get('85ca-t3if',where='first_crash_type' == 'PEDALCYCLIST',limit=2000)
# this doesn't generate an error but also doesn't pull in any data!

results_2=client.get('85ca-t3if',where= "crash_date>'21-01-01T00:00:00'",limit=2000)
# This works!

# working examples
url = 'https://data.cityofchicago.org/resource/85ca-t3if.json?$$app_token=5I2MKS1rZ49obGC9dtfgr2Pgi&$where=crash_date%20between%20%272021-01-01T00:00:00%27%20and%20%272022-01-01T00:00:00%27%20AND%20first_crash_type=%20%27PEDALCYCLIST%27'
crashes=pd.read_json(url)
crashes.columns
crashes.info()
crashes.date = pd.to_datetime(crashes.date)
crashes.crash_date = pd.to_datetime(crashes.crash_date)

#quick and dirty: what columns have interesting info?
cols=crashes.columns
for col in cols:
    print(crashes[col].value_counts(),'\n' )

crashes['crash_hour'].value_counts().sort_index().plot.bar(title='Crashes per hour of day')

crashes['crash_day_of_week'].value_counts().sort_index().plot.bar(title='Crashes by DOW (Sun = 1)')

crashes['crash_month'].value_counts().sort_index().plot.bar(title='Crashes by Month')

# mapping
import folium
mapCrashes = crashes.dropna(subset=['latitude','longitude'])
crash_lat = mapCrashes['latitude']
crash_lon = mapCrashes['longitude']
m = folium.Map(location=[crash_lat[0],crash_lon[0]])


