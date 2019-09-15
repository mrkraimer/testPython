#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from pvaccess import *
from pvaccess import DOUBLE

min = 0.0
max = 1.0
npts = 100
inc = (max-min)/npts
t = np.arange(min, max, inc)
m = 5
n = 3
x = np.cos(m*2*np.pi*t)
y = np.sin(n*2*np.pi*t)

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
