#!/usr/bin/env python
from GenerateCurve import generateCurve,getCurveNames
from Dynamic_Common import getDynamicRecordName,DynamicRecordData
from p4p.client.thread import Context
import numpy as np
import sys,time
if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs==1 :
        print('argument must be one of: ',getCurveNames())
        exit()
    if nargs!=2 : raise Exception('must specify curve name')
    curveName = sys.argv[1]
    data = generateCurve(curveName)
    x = data["x"]
    y = data["y"]
    ctxt = Context('pva')
    data = DynamicRecordData()
    data.name = curveName
    data.x = x
    data.y = y
    data.computeLimits()
    print('xmin=',data.xmin,' xmax=',data.xmax,' ymin=',data.ymin,' ymax=',data.ymax)
    putdata = {"name":data.name,"xmin":data.xmin,"xmax":data.xmax,"ymin":data.ymin,"ymax":data.ymax}
    ctxt.put(getDynamicRecordName(),putdata)
    npts = len(x)
    timestart = time.time()
    for ind in range(npts) :
        xarr = np.empty([ind])
        yarr = np.empty([ind])
        for i in range(ind) :
           xarr[i] = x[i]
           yarr[i] = y[i]
        data.x = xarr
        data.y = yarr
        putdata = {"x":xarr,"y":yarr}
        ctxt.put(getDynamicRecordName(),putdata)
    timenow = time.time()
    timediff = timenow - timestart
    print('putrate=',str(round(npts/timediff)),' per second')
