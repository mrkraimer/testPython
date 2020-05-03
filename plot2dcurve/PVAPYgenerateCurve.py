#!/usr/bin/env python
from GenerateCurve import generateCurve
from Dynamic_Common import getDynamicRecordName,DynamicRecordData
import numpy as np
from pvaccess import *
import sys,time

if __name__ == '__main__':
    curveData = generateCurve(sys.argv)
    x = curveData["x"]
    y = curveData["y"]
    curveName = curveData["name"]
    chan = Channel(getDynamicRecordName())
    data = DynamicRecordData()
    data.name = curveName
    data.x = x
    data.y = y
    data.computeLimits()
    print('name=',curveName,' xmin=',data.xmin,' xmax=',data.xmax,' ymin=',data.ymin,' ymax=',data.ymax)
    npts = len(x)
    putdata = PvObject(\
    {   'name':STRING\
         ,'xmin':DOUBLE\
         ,'xmax':DOUBLE\
         ,'ymin':DOUBLE\
         ,'ymax':DOUBLE\
    })
    putdata['name'] = data.name
    putdata['xmin'] = data.xmin
    putdata['xmax'] = data.xmax
    putdata['ymin'] = data.ymin
    putdata['ymax'] = data.ymax
    chan.put(putdata)
    timestart = time.time()
    for ind in range(npts) :
        xarr = np.empty([ind])
        yarr = np.empty([ind])
        for i in range(ind) :
            xarr[i] = x[i]
            yarr[i] = y[i]
        putdata = PvObject({'x':[DOUBLE],'y':[DOUBLE]})
        putdata['x'] = list(xarr)
        putdata['y'] = list(yarr)
        chan.put(putdata)
    timenow = time.time()
    timediff = timenow - timestart
    print('putrate=',str(round(npts/timediff)),' per second')
