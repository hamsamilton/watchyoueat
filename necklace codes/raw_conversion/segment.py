# Thursday, January 3, 2019 5:16:11.090 PM GMT-06:00
# Friday, January 4, 2019 3:48:26.520 PM GMT-06:00

import os
from os.path import join
import logging
import sys
from datetime import date
import pandas as pd
import numpy as np

sys.path.insert(0, '../beyourself/beyourself')
from beyourself import settings
from beyourself.data import get_necklace_timestr
from beyourself.core.algorithm import interval_intersect_interval
from beyourself.core.util import humanstr_withtimezone_to_datetime_df, maybe_create_folder
sys.path.insert(0, '../mining')
from periodic import periodic_subsequence, get_periodic_stat, peak_detection
import matplotlib.pyplot as plt
from utils import df_to_datetime_tz_aware

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# subj = "P103"
# inclusion = pd.read_csv(join(settings.CLEAN_FOLDER, subj + "/label/inclusion.csv"))

# df_chewing = pd.read_csv(os.path.join(settings.CLEAN_FOLDER, subj +'/label/chewing.csv'))
# df_chewing = humanstr_withtimezone_to_datetime_df(df_chewing, ['start', 'end'])
# interval_chewing = list(zip(df_chewing['start'].tolist(), df_chewing['end'].tolist()))

# checking that df_chewing is monotonic, no overlapping between chewing segments
# avoid human error in labeling
# for i in range(1, df_chewing.shape[0]):
#     diff = df_chewing['start'].iloc[i] - df_chewing['end'].iloc[i-1]

#     if not diff > pd.Timedelta(0):
#         bad = "Double check data!!! {}||{}||{}||{}".format(i, diff, df_chewing['start'].iloc[i],df_chewing['end'].iloc[i - 1])
#         raise ValueError(bad)

# segmentation_concat_list = []
# for i in range(inclusion.shape[0]):
# df_sensor = get_necklace_timestr(subj, inclusion['start'].iloc[i], inclusion['end'].iloc[i])

datafile = '/Users/shibozhang/Documents/SenseWhy/Data/203/InlabTrial/in_lab/Necklace/test.csv'
realtimefile = '/Users/shibozhang/Documents/SenseWhy/Data/203/InlabTrial/in_lab/Necklace/realtime_test.csv'
outfile = '/Users/shibozhang/Documents/SenseWhy/Data/203/InlabTrial/in_lab/Necklace/segments.csv'

df_sensor = pd.read_csv(datafile)
print(df_sensor)

# df_sensor = df_to_datetime_tz_aware(df_sensor,['Time'])
# df_sensor.to_csv(realtimefile, index=None)

# exit()

if df_sensor.empty:
    print("Skipping current inclusion interval")
    exit()


# time = df_sensor['Time'].as_matrix()
time = (df_sensor.index.astype(np.int64)/1e6).astype(int)

proximity = df_sensor['proximity'].as_matrix()

# plt.plot(proximity)
# plt.show()

# be careful to pick prominence (check data is normalized or not)
peaks_index = peak_detection(proximity, min_prominence=2)
peaks_time = time[peaks_index]

print(peaks_index)
print(peaks_time)

subsequences = periodic_subsequence(peaks_index, peaks_time, min_length=4, max_length=100,
                                    eps=0.1, alpha=0.45, low=400, high=1200)

print(subsequences)

segments = []
for index in subsequences:
    seq = time[index]
    segments.append(get_periodic_stat(seq))

df_segments = pd.DataFrame(segments, columns=['start', 'end', 'eps', 'pmin', 'pmax', 'length'])
# segmentation_concat_list.append(df_sub_segment)

# df_segments = pd.concat(segmentation_concat_list)
df_segments = df_segments.drop_duplicates().reset_index(drop=True)
print(df_segments)

df_segments.to_csv(outfile, index = None)

exit()
