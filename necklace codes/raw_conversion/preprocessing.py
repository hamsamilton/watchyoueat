from __future__ import division
import os
import re
import pandas as pd
import struct
from imu import leanForward
from datetime import datetime
import numpy as np
import logging
import sys
import time
import datetime


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def hex_to_float(string):
    string = string.replace(' ', '0')
    assert(len(string) == 8)
    return struct.unpack('!f', bytes.fromhex(string))[0]


def hex_to_int(string):
    string = string.replace(' ', '0')
    assert(len(string) == 4)
    return struct.unpack('!H', bytes.fromhex(string))[0]

def raw2q(a ,b ):
    string=a + b
    s=struct.unpack('!h', bytes.fromhex(string))
    x=s[0]*(2**(-14))
    return x

def raw2acc(a ,b ):
    string=a + b
    s=struct.unpack('!h', bytes.fromhex(string))
    x=s[0]*(2**(-8))
    return x

def parse_binary(binstring):
    binstring = binstring.replace('\x00', 'T')

    chunk = re.split(((',| |:|T|-|/|    ')),binstring)
    chunk = list(filter(None, chunk))
    for i in range(len(chunk)):
        if len(chunk[i])==1:
            chunk[i]='0'+chunk[i]


    proximity=int(chunk[17])
    ambient=int(chunk[18])
    time = datetime.datetime(int(chunk[19]),int(chunk[20]),int(chunk[21]),int(chunk[22]),int(chunk[23]),int(chunk[24]),10000*int(chunk[25]))
    timeStamp=int(time.timestamp()*1000)
    cal = int(chunk[16])
    
    
    aX=raw2acc(chunk[1],chunk[0])
    aY=raw2acc(chunk[3],chunk[2])
    aZ=raw2acc(chunk[5],chunk[4])
    Qi = raw2q(chunk[7],chunk[6])
    Qj = raw2q(chunk[9],chunk[8])
    Qk = raw2q(chunk[11],chunk[10])
    Qreal = raw2q(chunk[13],chunk[12])
    lf = leanForward((Qreal, Qi, Qj, Qk))
    power=aX**2+aY**2+aZ**2
    
    result = {}
    result['Time'] = timeStamp
    result['proximity'] = proximity
    result['ambient'] = ambient
    result['qW'] = Qreal
    result['qX'] = Qi
    result['qY'] = Qj
    result['qZ'] = Qk
    result['aX'] = aX
    result['aY'] = aY
    result['aZ'] = aZ
    result['leanForward'] = lf
    result['power'] = power
    result['cal'] = cal
    header = ['Time', 'proximity', 'ambient', 'leanForward',
              'qW', 'qX', 'qY', 'qZ','aX','aY','aZ','power','cal']

    # comment: not necessary to pass header repetitively

    return result, header

# Todo:
# Comment: document this function
# Comment: open writing streaming once instead of opening it for each line
# Comment: read binary file from numpy will be faster
def raw_convert(filename,new):
    # Comment: add fixed headers here
    # header = ['Time', 'proximity', 'ambient', 'leanForward',
    #           'qW', 'qX', 'qY', 'qZ','aX','aY','aZ','power','cal']

    with open(filename) as f:
        for line in f:
            try:
                data,header = parse_binary(line)
            except Exception:
                #logging.exception(Exception)
                print('omitting one line of log file.')
                continue
            with open(new,'a') as f_out:
                if f_out.tell() ==0:
                    f_out.write(','.join(header) + '\n')

                for h in header:
                    f_out.write(str(data[h]))
                    if h !='cal':
                        f_out.write(',')
                f_out.write('\n')
        print('logged')
    print('finished')
    
