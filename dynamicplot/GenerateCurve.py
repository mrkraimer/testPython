# GenerateCurve.py

import numpy as np
import sys

def getCurveNames() :
    return ("line","circle","ellipse","clover","heart","lissajous","figureight")

def generateCurve(argv) :
    nargs = len(argv)
    if nargs==1 :
        print('argument must be one of: ',getCurveNames())
        exit()
    if nargs<2 : raise Exception('must specify curve name')
    name = sys.argv[1]
    if name==str("line") :
         npts = 1000
         x = np.arange(npts,dtype="float64")
         y = np.arange(npts,dtype="float64")
         return {"x":x,"y":y,"name":name}
    if name==str("circle") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         x = np.cos(2*np.pi*t)
         y = np.sin(2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    if name==str("ellipse") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         a = 3.0
         if nargs>=3 : a = float(sys.argv[2])
         b = 2.0
         if nargs>=4 : b = float(sys.argv[3])
         x = a*np.cos(2*np.pi*t)
         y = b*np.sin(2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    if name==str("clover") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         nloops = 3
         if nargs>=3 : nloops = float(sys.argv[2])
         print('nloops=',nloops)
         t = np.arange(min, max, inc)
         x = np.sin(nloops*2*np.pi*t)*np.cos(2*np.pi*t)
         y = np.sin(nloops*2*np.pi*t)*np.sin(2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    if name==str("heart") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         x = (1.0 - np.cos(2*np.pi*t)*np.cos(2*np.pi*t))*np.sin(2*np.pi*t)
         y = (1.0 - np.cos(2*np.pi*t)*np.cos(2*np.pi*t)*np.cos(2*np.pi*t))*np.cos(2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    if name==str("lissajous") :
         min = 0.0
         max = 1.0
         npts = 4000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         m = 3
         if nargs>=3 : m = float(sys.argv[2])
         n = 1
         if nargs>=4 : n = float(sys.argv[3])
         x = np.sin(n*2*np.pi*t)
         y = np.cos(m*2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    if name==str("figureight") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         a = 1
         if nargs>=3 : a = float(sys.argv[2])
         print('a=',a)
         t = np.arange(min, max, inc)
         x = a*np.sin(2*np.pi*t)*np.cos(2*np.pi*t)
         y = a*np.sin(2*np.pi*t)
         return {"x":x,"y":y,"name":name}
    raise Exception(name + ' not implemented')

if __name__ == '__main__':
    curveData = generateCurve(sys.argv)
    print('name=',curveData["name"],' len(x)=',len(curveData["x"]),' len(y)=',len(curveData["y"]))


