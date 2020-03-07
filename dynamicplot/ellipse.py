#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure
from pvaccess import *
import numpy as np
import matplotlib.pyplot as plt
import time

min = 0.0
max = 1.0
npts = 2000
inc = (max-min)/npts
t = np.arange(min, max, inc)
a = 3.0
b = 2.0
x = a*np.cos(2*np.pi*t)
y = b*np.sin(2*np.pi*t)
chan = Channel('dynamicRecord')
struct = ChannelStructure()
struct.putName(str('ellipse'))
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
