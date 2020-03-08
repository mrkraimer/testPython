#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from pvaccess import *
import numpy as np

npts = 1000
x = np.arange(npts,dtype="float64")
y = np.arange(npts,dtype="float64")
provider = Dynamic_Channel_Provider()
chan = Channel(provider.getChannelName())
val = chan.get()
struct = ChannelStructure()
struct.set(val)
struct.putName(str('circle'))
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
#    time.sleep(.002)
