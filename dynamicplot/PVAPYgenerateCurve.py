#!/usr/bin/env python
from GenerateCurve import generateCurve,getCurveNames
from Dynamic_Common import getDynamicRecordName,DynamicRecordData
from pvaccess import *
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
    chan = Channel(getDynamicRecordName())
    data = DynamicRecordData()
    data.name = curveName
    data.x = x
    data.y = y
    data.computeLimits()
    print('xmin=',data.xmin,' xmax=',data.xmax,' ymin=',data.ymin,' ymax=',data.ymax)
    npts = len(x)
    timestart = time.time()
    for ind in range(npts) :
        xarr = np.empty([ind])
        yarr = np.empty([ind])
        for i in range(ind) :
            xarr[i] = x[i]
            yarr[i] = y[i]
        if ind==0 :
            putdata = PvObject(\
            {   'name':STRING\
                ,'xmin':DOUBLE\
                ,'xmax':DOUBLE\
                ,'ymin':DOUBLE\
                ,'ymax':DOUBLE\
                ,'x':[DOUBLE]\
                ,'y':[DOUBLE]\
            })
            putdata['name'] = data.name
            putdata['xmin'] = data.xmin
            putdata['xmax'] = data.xmax
            putdata['ymin'] = data.ymin
            putdata['ymax'] = data.ymax
            putdata['x'] = np.arange(0,dtype="float64")
            putdata['y'] = np.arange(0,dtype="float64")
        else :
            putdata = PvObject({'x':[DOUBLE],'y':[DOUBLE]})
            putdata['x'] = xarr
            putdata['y'] = yarr
        chan.put(putdata)
    timenow = time.time()
    timediff = timenow - timestart
    print('putrate=',str(round(npts/timediff)),' per second')
