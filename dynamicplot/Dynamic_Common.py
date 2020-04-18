# Dynamic_Common.py

import numpy as np
import os

def getDynamicRecordName() :
    name = os.getenv('DYNAMIC_RECORDNAME')
    if name== None : return(str('dynamicRecord'))
    return str(name)

def getAddRecordName() :
    name = os.getenv('ADD_RECORDNAME')
    if name== None : return(str('TPYaddRecord'))
    return str(name)

class DynamicRecordData(object) :
    def __init__(self) :
        self.name = str("unknown")
        self.x = np.zeros((0),dtype="float64")
        self.y = np.zeros((0),dtype="float64")
        self.xmin = float(0)
        self.xmax = float(0)
        self.ymin = float(0)
        self.ymax = float(0)

    def computeLimits(self) :
        x = self.x
        y = self.y
        npts = len(x)
        if npts<1 :
            raise Exception('x length < 1')
        if npts!= len(y) :
            raise Exception('x and y do not have same length')
        xmin = x[0]
        xmax = xmin
        ymin = y[0]
        ymax = ymin
        for i in range(npts) :
            if x[i]>xmax : xmax = x[i]
            if x[i]<xmin : xmin = x[i]
            if y[i]>ymax : ymax = y[i]
            if y[i]<ymin : ymin = y[i]
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

class Dynamic_Channel_Provider(object) :
    '''
    Base class for monitoring an NTNDArray channel from an areaDetector IOC.
    The methods are called by NTNDA_Viewer.
    '''

    def __init__(self) :
        pass
    def start(self) :
        ''' called to start monitoring.'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.start')
    def stop(self) :
        ''' called to stop monitoring.'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.stop')
    def done(self) :
        ''' called when NTNDA_Viewer is done.'''
        pass
    def callback(self,arg) :
        ''' must call NTNDA_Viewer.callback(arg).'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.callback')
