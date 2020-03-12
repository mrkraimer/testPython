#!/usr/bin/env python
from GenerateCurve import generateCurve
from Dynamic_Common import getDynamicRecordName
from Dynamic_Viewer import ChannelStructure
from pvaccess import *
import numpy as np
import sys

if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs!=2 : raise Exception('must specify curve name')
    curveName = sys.argv[1]
    data = generateCurve(curveName)
    x = data["x"]
    y = data["y"]
    chan = Channel(getDynamicRecordName())
    val = chan.get()
    struct = ChannelStructure()
    struct.set(val)
    struct.putName(curveName)
    struct.putX(x)
    struct.putY(y)
    struct.computeLimits()
    npts = len(x)
    for ind in range(npts) :
        xarr = np.empty([ind])
        yarr = np.empty([ind])
        for i in range(ind) :
           xarr[i] = x[i]
           yarr[i] = y[i]
        struct.putX(xarr)
        struct.putY(yarr)
        chan.put(struct.get())
