#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from pvaccess import *
import numpy as np
import matplotlib.pyplot as plt
import time

min = 0.0
max = 1.0
npts = 10000
inc = (max-min)/npts
t = np.arange(min, max, inc)
m = 5
n = 3
x = np.cos(m*2*np.pi*t)
y = np.sin(n*2*np.pi*t)
struct = ChannelStructure()
struct.putName(str('lissajous'))
struct.putX(x)
struct.putY(y)
struct.computeLimits()
provider = Dynamic_Channel_Provider()
chan = Channel(provider.getChannelName())
for ind in range(npts) :
    xarr = np.empty([ind])
    yarr = np.empty([ind])
    for i in range(ind) :
       xarr[i] = x[i]
       yarr[i] = y[i]
    struct.putX(xarr)
    struct.putY(yarr)
    chan.put(struct.get())
#    time.sleep(.001)
