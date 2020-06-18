#!/usr/bin/env python
import numpy as np
from pvaccess import *
import sys,time

if __name__ == '__main__':
    chan = Channel('TPYqtpeakimageRecord')
    data = chan.get('peak')
    print('data=',data)
    x = 100
    y = 100
    intensity = 0.0
    num = 500
    for i in range(num) :
        x = x+1
        y = y+1
        intensity = 1.0/float(num)
        data['peak.x'] = x
        data['peak.y'] = y
        data['peak.intensity'] = 1.0*(float(i)/num)
        chan.put(data)
        time.sleep(.005)
