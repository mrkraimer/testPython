#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from pvaccess import *
import numpy as np

min = 0.0
max = 1.0
npts = 2000
inc = (max-min)/npts
nloops = 3
t = np.arange(min, max, inc)
x = np.sin(nloops*2*np.pi*t)*np.cos(2*np.pi*t)
y = np.sin(nloops*2*np.pi*t)*np.sin(2*np.pi*t)
provider = Dynamic_Channel_Provider()
chan = Channel(provider.getChannelName())
val = chan.get()
struct = ChannelStructure()
struct.set(val)
struct.putName(str('clover'))
struct.putX(x)
struct.putY(y)
struct.computeLimits()

for ind in range(npts) :
    xarr = np.empty([ind])
    yarr = np.empty([ind])
    for i in range(ind) :
       xarr[i] = x[i]
       yarr[i] = y[i]
    struct.putX(xarr)
    struct.putY(yarr)
    chan.put(struct.get())
