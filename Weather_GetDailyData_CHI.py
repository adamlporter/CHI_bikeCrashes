# This file will, over several days, download the weather data for Chicago, every fourth hour.
# 
# The dataset will begin on 1 Jan 2018 and go through 31 Dec 2021.

#import datetime as dt
import numpy as np
import pandas as pd
import json

def weatherLookup(apiQuery):
    import urllib
    import json

    try: 
        with urllib.request.urlopen(ApiQuery) as response:
            html = response.read()
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()

    weather = json.loads(html.decode('utf-8'))
    return weather

# get API tokens
with open('.env.development') as f:
    data = f.read()

for line in data.split('\n'):
    head,sep,tail = line.partition(' = ')
    
    if head == 'crashAPIkey':
        crashAPIkey = tail
    elif head == 'weatherAPIkey':
        weatherAPIkey = tail

# these are the middle points for the crash data from 2021
lat = '41.89529666462941'
lon = '-87.67682552741503'

# load the existing data files and look for largest date value
with open('rawData.json','r') as fin:
    RawData = json.load(fin)

with open('processedData.json','r') as fin:
    ProcessedData = json.load(fin)

# rather than writing code to deal with leap years, different month lengths, etc.
# I'm going to use the numpy library's date functions
lastDate = ProcessedData[-1]['date'] # get the last date as a string

# find the next date and use that as the date+1 to start 
d_start = np.datetime64(lastDate) + np.timedelta64(1,'D')

# date to end is 3 months beyond this
# this line 1) looks at the YYYY-MM of the lastDate string, increments it by 3
# 2) converts it to a string and adds the first day of month
# 3) converst it back to a datetime  
d_end =  np.datetime64(str(np.datetime64(lastDate[0:7]) + np.timedelta64(3,'M')) + '-01')

d_list = pd.date_range(d_start,d_end,freq="D")

# now that we have the list of dates, let's get the weather for each date
# we will look for six points per day
times = ['00:00:01','04:00:01','8:00:01','12:00:01','16:00:01','20:00:01']
for d in d_list[0:1]:
    for t in times:
        dd = {}
        dateTimeS = f'{d.strftime("%Y-%m-%d")}T{t}'
        ApiQuery = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+\
            lat+'%2C'+lon+'/'+dateTimeS+'?unitGroup=us&key='+weatherAPIkey+'&include=current&contentType=json'
        
        rawResponse = weatherLookup(ApiQuery)
        rawData.append(rawResponse)
        dd = rawResponse['currentConditions']
        dd['date'] = rawResponse['days'][0]['datetime']
        dd['time'] = dd['datetime']
        processedData.append(dd)

        print(d)

# now save the newly extended lists

with open('rawData.json','w') as fout:
    json.dump(rawData,fout)

with open('processedData.json','w') as fout:
    json.dump(processedData,fout)


