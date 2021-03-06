#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import getDynamicRecordName,DynamicRecordData
from pvaccess import *
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal
import numpy as np
import sys

class PVAPYProvider(QObject) :
    monitorCallbacksignal = pyqtSignal()
    connectCallbacksignal = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        self.monitordata = None
        self.connectdata = None
        self.firstStart = True
        self.isConnected = False
        self.init()
    def init(self) :
        self.connectCallbacksignal.connect(self.connectionCallback)
        self.monitorCallbacksignal.connect(self.monitorCallback)
        self.callbackDoneEvent = Event()
        self.callbackDoneEvent.set()
        self.channel = Channel(getDynamicRecordName())
        self.channel.setConnectionCallback(self.pvapyconnectioncallback)

    def start(self) : 
        if self.firstStart :
             self.firstStart = False
             data = dict()
             if self.isConnected==True :
                 data["status"] = "connected"
             else  :
                 data["status"] = "disconnected"
             
             self.callViewerCallback(data)
        self.channel.monitor(self.pvapymonitorcallback,'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass

    def callViewerCallback(self,arg) :
        self.viewer.callback(arg)

    def pvapyconnectioncallback(self,arg) :
        if self.firstStart :
            self.isConnected = arg
            return
        data = dict()
        if arg==True :
            data["status"] = "connected"
        elif arg==False :
            data["status"] = "disconnected"
        else :
            data["exception"] = "bad pvapy connection callback =" + str(arg)
        self.connectdata = data
        self.callbackDoneEvent.clear()
        self.connectCallbacksignal.emit()

    def connectionCallback(self) :
        while self.connectdata is not None:
            try:
                arg = self.connectdata
                self.connectdata = None
                self.callViewerCallback(arg)
            except Exception as error:
                arg["exception"] = repr(error)
                self.callViewerCallback(arg)
        self.callbackDoneEvent.set()

    def pvapymonitorcallback(self,arg) :
        data = DynamicRecordData()
        data.name = arg['name']
        data.x = np.copy(arg['x'])
        data.y = np.copy(arg['y'])
        data.xmin = arg['xmin']
        data.xmax = arg['xmax']
        data.ymin = arg['ymin']
        data.ymax = arg['ymax']
        if self.monitordata==None:
            self.monitordata = data
            self.monitorCallbacksignal.emit()
            self.callbackDoneEvent.wait()
            self.callbackDoneEvent.clear()
            
        else:
            self.monitordata = data

    def monitorCallback(self) :
        while not self.monitordata==None :
            try:
                arg = dict()
                arg['value'] = self.monitordata
                self.callViewerCallback(arg)    
            except Exception as error:
                arg["exception"] = repr(error)
                self.callViewerCallback(arg)
            self.monitordata = None
        self.callbackDoneEvent.set()

if __name__ == '__main__':
    app = QApplication(list())
    PVAPYProvider = PVAPYProvider()
    PVAPYProvider.viewer = Dynamic_Viewer(PVAPYProvider,"PVAPY")
    sys.exit(app.exec_())


