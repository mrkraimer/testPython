#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from pvaccess import *
from pvaccess import DOUBLE

min = 0.0
max = 1.0
npts = 1000
inc = (max-min)/npts
t = np.arange(min, max, inc)
x = (1.0-np.cos(2*np.pi*t))*np.cos(2*np.pi*t)
y = (1.0-np.cos(2*np.pi*t))*np.sin(2*np.pi*t)
chan = Channel("x")
pv = chan.get("value")
arr = pv['value']
pv["value"] = x
chan.put(pv)
chan = Channel("y")
pv = chan.get("value")
arr = pv['value']
pv["value"] = y
chan.put(pv)
