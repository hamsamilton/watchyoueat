import os
import sys
import pandas as pd
from datetime import timedelta
from datetime import datetime
from pytz import timezone
sys.path.append('../..')
from settings import settings
from utils import create_folder, list_files_in_directory, datetime_to_filename


def split_by_hour(file, NECKLACE_DIR):
    create_folder(NECKLACE_DIR)

    # This is a date days before the study, to remove the 1969 error data.
    starttimestamp = 1000000000000 #September 8, 2001 8:46:40 PM GMT-05:00 DST
    localtz = settings['TIMEZONE']

    print(file)

    df = pd.read_csv(file)

    print('len', len(df), '\n')
    df = df[~df['Time'].isin(['Time'])]
    print('Remove redundant headers...\n')
    print('len', len(df), '\n')
    l1 = len(df)

    df = df.dropna()
    df['Time'] = pd.to_numeric(df['Time'], errors='ignore')
    df = df[df['Time'] > starttimestamp]
    print('len', len(df), '\n')
    l2 = len(df)

    print('# Timestamp 1969 Error Lines: ', str(l1 - l2))

    df = df.sort_values('Time')

    df['date'] = pd.to_datetime(df['Time'],unit='ms')
    df = df.set_index(['date'])
    df.index = df.index.tz_localize('UTC').tz_convert(settings['TIMEZONE'])

    # dt: absolute hour of the first timestamp
    dt = datetime(year = df.index[0].year, month = df.index[0].month, \
                    day = df.index[0].day, hour = df.index[0].hour, minute = 0, second = 0)
    dt = localtz.localize(dt)
    print(df.index[0])
    print(df.index[-1])

    #========================================================================================================
    # split each hour into separate file under day folder
    #========================================================================================================
    startHour = dt
    endHour = dt + timedelta(hours = 1)

    while endHour < df.index[-1] + timedelta(hours = 1):
        dfHr = df[(df.index >= startHour) & (df.index < endHour)]
        
        if len(dfHr):
            file = datetime_to_filename(startHour)
            dfHr.to_csv(os.path.join(NECKLACE_DIR, file))

            print(startHour)
            print(endHour)
            print(len(dfHr))
            print(file)

        startHour += timedelta(hours = 1)
        endHour += timedelta(hours = 1)
        


# if __name__ == "__main__":
#     outfile = '/Volumes/Seagate/Periodic/RAW/200/NECKLACE/NEC2.csv'
#     NECKLACE_DIR = '/Volumes/Seagate/Periodic/CLEAN/200/NECKLACE/'
#     split_by_hour(outfile, NECKLACE_DIR)

