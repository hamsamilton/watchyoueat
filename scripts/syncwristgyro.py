import os
import re
import sys
import json
import time
import yaml
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pylab
from datetime import datetime, timedelta, time, date
from shutil import copyfile
from utils import create_folder, \
					datetime_to_unixtime, \
					parse_timestamp_tz_naive, \
					list_files_in_directory, \
					truncate_df_index_dt,\
					truncate_df_index_str,\
					parse_timestamp_tz_aware,\
					unixtime_to_datetime
from settings import settings

print(settings['TIMEZONE'])

SUBJ = 'P411'
DEVICE = 'Wrist'
DATE = '2019-11-12'
HOUR = '21'
SETTING_PATH = os.path.join(os.getcwd(), SUBJ, 'sync.yaml')

with open(SETTING_PATH) as f:
    SETTINGS = yaml.load(f)
print(SETTINGS)
videoLenInMinute = 60

DATA_FOLDER = os.path.join(os.getcwd(),SUBJ,'In Wild',DEVICE,'Clean','Resampled','Gyroscope',DATE,HOUR) 
file = 'accel_data.csv'
dataPath = os.path.join(DATA_FOLDER, file)
dataDf = pd.read_csv(dataPath)

dataDf['Unixtime'] = dataDf['Time']
dataDf['Time'] = pd.to_datetime(dataDf['Time'],unit='ms',utc=False)
dataDf = dataDf.set_index(['Time'])
dataDf.index = dataDf.index.tz_localize('UTC').tz_convert(settings['TIMEZONE'])
print(dataDf)

for episode in SETTINGS:
	print("episode: ", episode)
	# get start time and end time
	sync_relative = SETTINGS[episode]['sync_relative']
	sync_absolute = SETTINGS[episode]['sync_absolute']
	video_lead_time = SETTINGS[episode]['video_lead_time']
	print("video_lead_time: ", video_lead_time)
	
	# sync_absolute = parse_timestamp_tz_aware(unixtime_to_datetime(sync_absolute))
	sync_absolute = parse_timestamp_tz_aware(sync_absolute)
	t = datetime.strptime(sync_relative,"%H:%M:%S")
	startTime = sync_absolute - timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)\
							 + timedelta(seconds=video_lead_time/1000)
	endTime = startTime + timedelta(minutes=videoLenInMinute)
	startTimeExt = startTime - timedelta(minutes = 10)
	endTimeExt = endTime + timedelta(minutes = 10)

	epiDf = dataDf[(dataDf.index > startTimeExt) & (dataDf.index <= endTimeExt)]
	epiDf['ELAN_time'] = (epiDf['Unixtime'] - datetime_to_unixtime(startTime)).astype(int)
	print(startTime)
	print(endTime)
	# epiDf[['accx','accy','accz']].plot()
	# plt.show()
	NEW_FOLDER = os.path.join(os.getcwd(),'syncd')
	create_folder(NEW_FOLDER)
	newDataPath = os.path.join(NEW_FOLDER, SUBJ + DEVICE + 'gyr' + DATE + HOUR + file)
	epiDf.to_csv(newDataPath, index = None)