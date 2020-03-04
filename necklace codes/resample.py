"""
Functionality:
    Resample time series data with linear interplation method based on 
        a). a fixed sampling rate, or
        b). a given list of sampling positions

    When resampling based on a given list of sampling positions, 
        you can merge two sensors‘ time series data together at common sampling positions

Steps:

    1. Anchor sensor: read in all continuous data block in day level,
      A. Put data files into groups according to continuity
      B. Read in one data block at a time according to continuity groups

    2. Anchor sensor: resampling within each data block
      A. Take the first entry time of a block as start time
      B. When there is a gap in the data, if gap > 0.5 s, set value as nan, otherwise take interpolation value

    3. Boat sensor: resampling anchored to anchor sensor
      A. Take the anchor sensor's time column as target time column
      B. Same as Step 2(B), when gap >0.5s, set value as nan


Action items:
1. change all namings - done
2. 'linear interplation' in description - done
3. settings -> timeColHeader - done
4. move 'if n<2: return' out of loop - done
 
"""

import os 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import inspect
from PASDAC import resample
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from utils import create_folder, list_files_in_directory


def resampling_pandas(df, sampling_freq=20, higher_freq=100, max_gap_sec=1):
    ''' Resample unevenly spaced timeseries data linearly by 
    first upsampling to a high frequency (short_rate) 
    then downsampling to the desired rate.

    Parameters
    ----------
        df:               dataFrame
        sampling_freq:    sampling frequency
        max_gap_sec:      if gap larger than this, interpolation will be avoided
    
    Return
    ------
        result:           dataFrame
        
    Note: You will need these 3 lines before resampling_pandas() function
    ---------------------------------------------------------------------
        # df['date'] = pd.to_datetime(df['Time'],unit='ms')
        # df = df.set_index(['date'])
        # df.index = df.index.tz_localize('UTC').tz_convert(settings.TIMEZONE)

    '''
    
    # find where we have gap larger than max_gap_sec
    # print(df.index)
    # diff = np.diff(df.index)

    # print(diff)
    idx = np.where(np.greater(np.diff(df.index), 1000))[0]
    start = df.index[idx].tolist()
    stop = df.index[idx + 1].tolist()
    big_gaps = list(zip(start, stop))

    # upsample to higher frequency
    df = df.resample('{}ms'.format(1000/higher_freq)).mean().interpolate()

    # downsample to desired frequency
    df = df.resample('{}ms'.format(1000/sampling_freq)).ffill()

    # remove data inside the gaps
    for start, stop in big_gaps:
        df[start:stop] = None
    df.dropna(inplace=True)

    return df

# todo: move to pasdac
def resample_folder(inpath, outpath, timeColHeader, gapTolerance=np.inf, samplingRate=None):
    '''

    :param inpath:
    :param outpath:
    :param timeColHeader:
    :param gapTolerance:
    :param samplingRate:
    :return:
    '''
    create_folder(outpath)
    files = list_files_in_directory(inpath)

    for file in files:
        if not file.startswith('.'):
            dataDf = pd.read_csv(os.path.join(inpath, file))

            if len(dataDf):
                if 'date' in dataDf.columns:
                    dataDf = dataDf.drop(columns=['date'])
                # print(dataDf.dtypes)
                # dataDf = dataDf.astype({"Time": float})
                newDf = resample(dataDf, timeColHeader, samplingRate, gapTolerance=np.inf, fixedTimeColumn=None)
                newDf.to_csv(os.path.join(outpath, file), index=None)


def main():
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    timeColHeader = sys.argv[3]
    gapTolerance = int(sys.argv[4])
    samplingRate = int(sys.argv[5])

    resample_folder(inpath, outpath, timeColHeader, gapTolerance=gapTolerance, samplingRate=samplingRate)


if __name__ == '__main__':
    main()
