#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import Dynamic_Channel_Provider,getDynamicRecordName,DynamicRecordData
from pvaccess import *
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal
import numpy as np
import sys

class PVAPYProvider(QObject,Dynamic_Channel_Provider) :
    monitorCallbacksignal = pyqtSignal()
    connectCallbacksignal = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)
        self.monitordata = None
        self.connectdata = None
        self.firstStart = True
        self.isConnected = False
        self.init()
    def init(self) :
        self.connectCallbacksignal.connect(self.viewerconnectionCallback)
        self.monitorCallbacksignal.connect(self.viewermonitorCallback)
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
             
             self.viewerCallback(data)
        self.channel.monitor(self.pvapymonitorcallback,'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass

    def viewerCallback(self,arg) :
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

    def viewerconnectionCallback(self) :
        while self.connectdata is not None:
            try:
                arg = self.connectdata
                self.connectdata = None
                self.viewerCallback(arg)
            except Exception as error:
                arg["exception"] = repr(error)
                self.viewerCallback(arg)
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
        if not self.monitordata:
            self.monitordata = data
            self.callbackDoneEvent.clear()
            self.monitorCallbacksignal.emit()
        else:
            self.monitordata = data

    def viewermonitorCallback(self) :
        while self.monitordata is not None:
            try:
                arg = dict()
                arg['value'] = self.monitordata
                self.monitordata = None
                self.viewerCallback(arg)
            except Exception as error:
                arg["exception"] = repr(error)
                self.viewerCallback(arg)
        self.callbackDoneEvent.set()

if __name__ == '__main__':
    app = QApplication(list())
    PVAPYProvider = PVAPYProvider()
    PVAPYProvider.viewer = Dynamic_Viewer(PVAPYProvider,"PVAPY")
    sys.exit(app.exec_())


