#!/usr/bin/env pythonpyt
from GenerateCurve import generateCurve,getCurveNames
from Dynamic_Common import getDynamicRecordName,DynamicRecordData
from p4p.client.thread import Context
import numpy as np
import sys,time
if __name__ == '__main__':
    curveData = generateCurve(sys.argv)
    x = curveData["x"]
    y = curveData["y"]
    ctxt = Context('pva')
    data = DynamicRecordData()
    data.x = x
    data.y = y
    data.name = curveData["name"]
    data.computeLimits()
    print('name=',data.name,' xmin=',data.xmin,' xmax=',data.xmax,' ymin=',data.ymin,' ymax=',data.ymax)
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
        if ind==0 :
            putdata = {"name":data.name,"xmin":data.xmin,"xmax":data.xmax,"ymin":data.ymin,"ymax":data.ymax,"x":x,"y":y}
        else :
            putdata = {"x":xarr,"y":yarr}
        ctxt.put(getDynamicRecordName(),putdata)
    timenow = time.time()
    timediff = timenow - timestart
    print('putrate=',str(round(npts/timediff)),' per second')
