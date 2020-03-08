#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from p4p.client.thread import Context
import numpy as np

min = 0.0
max = 1.0
npts = 4000
inc = (max-min)/npts
t = np.arange(min, max, inc)
m = 3
n = 1
x = np.cos(m*2*np.pi*t)
y = np.sin(n*2*np.pi*t)
provider = Dynamic_Channel_Provider()
ctxt = Context('pva')
val = ctxt.get(provider.getChannelName())
struct = ChannelStructure()
struct.set(val)
struct.putName(str('lissajous'))
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
    ctxt.put(provider.getChannelName(),struct.get())
