import os
import sys
import numbers
import numpy as np
import pandas as pd
import pickle as cp
from datetime import datetime, timedelta
sys.path.append('../..')
from utils import unixtime_to_datetime, datetime_str_to_unixtime, string_to_datetime, \
                datetime_to_foldername, datetime_to_filename, lprint, create_folder, \
                datetime_str_to_unixtime

# todo: script filename structure

def list_date_folders_hour_files(interval):
    """
    param interval: python datetime format or unixtimestamp (int)

    """
    start = interval[0]
    end = interval[1]

    if isinstance(start, str):
        start = datetime_str_to_unixtime(start)
    if isinstance(end, str):
        end = datetime_str_to_unixtime(end)

    if isinstance(start, numbers.Integral):
        start = unixtime_to_datetime(start)
    if isinstance(end, numbers.Integral):
        end = unixtime_to_datetime(end)


    # FFList means dateFolderHourFileList
    FFList = [[datetime_to_foldername(start), datetime_to_filename(start)]]
    curr = start + timedelta(hours = 1)

    while curr.replace(minute=0, second=0, microsecond=0) <= end.replace(minute=0, second=0, microsecond=0):
        FFList.append([datetime_to_foldername(curr), datetime_to_filename(curr)])
        curr += timedelta(hours = 1)

    return FFList


def read_data(DATA_DIR, startTime, endTime):
    '''
    :param DATA_DIR: data directory
    :param startTime: unixtimestamp
    :param endTime: unixtimestamp
    :return:
    '''
    # 1.
    FFList = list_date_folders_hour_files([startTime, endTime])
    # dfConcat = [pd.read_csv(os.path.join(DATA_DIR, FFList[i][1]))\
    #             for i in range(len(FFList))]

    dfConcat = []
    for i in range(len(FFList)):
        try:
            dfConcat.append(pd.read_csv(os.path.join(DATA_DIR, FFList[i][1])))
        except:
            print('Data file ', FFList[i][1], ' does not exist.')

    try:
        df = pd.concat(dfConcat)
    except:
        print('Data from ', str(startTime), ' to ', str(endTime), ' do not exist.')
        return None

    # 2. if there are 10 characters,
    #  convert from second-unixtimestamp to millisecond-unixtimestamp
    if len(str(abs(startTime))) == 10:
        startTime = startTime * 1000
    if len(str(abs(endTime))) == 10:
        endTime = endTime * 1000

    # 3. cut the start and end of data chunk
    df = df[(df['Time'] > startTime) & (df['Time'] < endTime)]

    return df
