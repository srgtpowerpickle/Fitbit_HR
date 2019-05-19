# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Import relevant libraries
import json
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.dates import HourLocator, DateFormatter

import datetime
from datetime import timedelta

# Set how many days to plot     
days = 365

# Set initial day to plot
dateString = [datetime.datetime(2018, 1, 1, 0, 0)] * days

# Create filename strings
for i in range(days):
    if i > 0:
        dateString[i] = dateString[i-1] + timedelta(days=1) 
        
# Initialize the variables
DATEPRIME = dict()
DATE = dict()
TIME = dict()
HR = dict()
count = 0

# Initialize plot
fig, ax1 = plt.subplots(figsize=(16/1.5,9/1.5),dpi=100)
ax1.grid(zorder=0,alpha=0.35)

for i in range(days):
    
    exists = os.path.isfile('heart_rate-' + dateString[i].strftime("%Y-%m-%d") + '.json')
    
    if exists:
        
        # If the file exists, open it. Otherwise move to the next one
        with open('heart_rate-' + dateString[i].strftime("%Y-%m-%d") + '.json') as f:
            data = json.load(f)
                              
        LATESTDATE = [datetime.datetime(2018, 1, 1, 0, 0)] * len(data)
        LATESTHR = [0] * len(data)
        
        # Read in daily heart rate from jsons
        for j in range(len(data)):
            
            count = count + 1
            
            DATEPRIME[count] = datetime.datetime.strptime(data[j]['dateTime'],'%m/%d/%y %H:%M:%S')   
            DATE[count] = datetime.datetime.strptime(data[j]['dateTime'],'%m/%d/%y %H:%M:%S').strftime('%m/%d/%y')
            TIME[count] = datetime.datetime.strptime(data[j]['dateTime'],'%m/%d/%y %H:%M:%S').strftime('%H:%M:%S')
            HR[count] = data[j]['value']['bpm']
            
            LATESTDATE[j] = datetime.datetime.strptime(data[j]['dateTime'],'%m/%d/%y %H:%M:%S').strftime('%H:%M:%S')    
            LATESTHR[j] = data[j]['value']['bpm']
    
        # Plot the day's heart rate
        ax1.plot_date(pd.to_datetime(LATESTDATE),LATESTHR,'o', color='k',
                      markerfacecolor='r',alpha=0.01,markeredgewidth=0,zorder=3)
    
# Format plot and save
ax1.xaxis.set_major_formatter(DateFormatter('%#I %p'))
ax1.set_xlim([pd.to_datetime('00:00:00'),pd.to_datetime('00:00:00') + pd.DateOffset(days=1)])
ax1.xaxis.set_major_locator(HourLocator(np.arange(0, 24, 3)))
ax1.set_ylim([0,200])
ax1.set_yticks(np.arange(0, 200+1, 20))
ax1.set_xlabel('Time of Day') 
ax1.set_ylabel('Heart Rate (BPM)')  
fig.suptitle("Heart Rate Data From " + dateString[1].strftime("%m/%Y") + " - " + 
             dateString[-1].strftime("%m/%Y"),weight="bold",size=16)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig('HR_Data_Scatter.png')


