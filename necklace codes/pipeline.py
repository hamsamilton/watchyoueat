import os
import sys
import numpy as np
sys.path.append('raw_conversion')
from preprocessing import raw_convert
from split_by_hour import split_by_hour
from resample import resample_folder
# from PASDAC import resample_folder
sys.path.append('../..')
from settings import settings

'''
The most important function here is the raw_convert, it parse the raw data from necklace to a csv file you can use. Remember to change 'rawFile' to the name of your raw file.
'''
if __name__ == "__main__":

    ROOT_DIR = settings['ROOT_DIR']
    console.log (ROOT_DIR)
    subj = str(sys.argv[1]) 
    # subj = settings['subj']

    # ==================================================================================
    rawFile = os.path.join(ROOT_DIR, 'RAW', subj, 'NECKLACE/NEC')
    csvFile = os.path.join(ROOT_DIR, 'RAW', subj, 'NECKLACE/NEC.csv')

    UNSAMPLE_DIR = os.path.join(ROOT_DIR, 'CLEAN', subj, 'NECKLACE/UNSAMPLED/')
    SAMPLE_DIR = os.path.join(ROOT_DIR, 'CLEAN', subj, 'NECKLACE/')
    # ==================================================================================

    raw_convert(rawFile, csvFile)
    split_by_hour(csvFile, UNSAMPLE_DIR)
    resample_folder(UNSAMPLE_DIR, SAMPLE_DIR, timeColHeader = 'Time', gapTolerance = 100, samplingRate = 20)

