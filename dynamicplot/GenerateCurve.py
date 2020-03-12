# GenerateCurve.py

import numpy as np

def generateCurve(name) :
    if name==str("line") :
         npts = 1000
         x = np.arange(npts,dtype="float64")
         y = np.arange(npts,dtype="float64")
         return {"x":x,"y":y}
    if name==str("circle") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         x = np.cos(2*np.pi*t)
         y = np.sin(2*np.pi*t)
         return {"x":x,"y":y}
    if name==str("ellipse") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         a = 3.0
         b = 2.0
         x = a*np.cos(2*np.pi*t)
         y = b*np.sin(2*np.pi*t)
         return {"x":x,"y":y}
    if name==str("clover") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         nloops = 3
         t = np.arange(min, max, inc)
         x = np.sin(nloops*2*np.pi*t)*np.cos(2*np.pi*t)
         y = np.sin(nloops*2*np.pi*t)*np.sin(2*np.pi*t)
         return {"x":x,"y":y}
    if name==str("heart") :
         min = 0.0
         max = 1.0
         npts = 2000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         x = (1.0 - np.cos(2*np.pi*t)*np.cos(2*np.pi*t))*np.sin(2*np.pi*t)
         y = (1.0 - np.cos(2*np.pi*t)*np.cos(2*np.pi*t)*np.cos(2*np.pi*t))*np.cos(2*np.pi*t)
         return {"x":x,"y":y}
    if name==str("lissajous") :
         min = 0.0
         max = 1.0
         npts = 4000
         inc = (max-min)/npts
         t = np.arange(min, max, inc)
         m = 3
         n = 1
         x = np.cos(m*2*np.pi*t)
         y = np.sin(n*2*np.pi*t)
         return {"x":x,"y":y}
    raise Exception(name + ' not implemented')


