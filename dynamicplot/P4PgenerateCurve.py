#!/usr/bin/env python
from GenerateCurve import generateCurve
from Dynamic_Common import getDynamicRecordName
from Dynamic_Viewer import ChannelStructure
from p4p.client.thread import Context
import numpy as np
import sys

if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs!=2 : raise Exception('must specify curve name')
    curveName = sys.argv[1]
    data = generateCurve(curveName)
    x = data["x"]
    y = data["y"]
    ctxt = Context('pva')
    val = ctxt.get(getDynamicRecordName())
    struct = ChannelStructure()
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
        data = {"x":xarr,"y":yarr}
        ctxt.put(getDynamicRecordName(),struct.get())
