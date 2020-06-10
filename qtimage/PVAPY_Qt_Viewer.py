#!/usr/bin/env python

from Qt_Viewer import Qt_Viewer
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
        self.channelName = 'TPYqtimageRecord'
        self.channel = Channel(self.channelName)
        self.connectCallbacksignal.connect(self.viewerconnectionCallback)
        self.monitorCallbacksignal.connect(self.viewermonitorCallback)
        self.callbackDoneEvent = Event()
        self.callbackDoneEvent.set()
        self.channel.setConnectionCallback(self.pvapyconnectioncallback)
        
    def setChannelName(self,channelName) :
        self.channelName = channelName
        self.channel = Channel(self.channelName)
        
    def getChannelName(self) :
        return self.channelName

    def start(self) : 
        if self.firstStart :
             self.firstStart = False
             data = dict()
             if self.isConnected==True :
                 data["status"] = "connected"
             else  :
                 data["status"] = "disconnected"
             
             self.viewerCallback(data)
        self.channel.monitor(self.pvapymonitorcallback,'field(argument{format,height,width},result.value)')
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
        data = {\
            "format" : arg['argument.format'],\
            "height": arg['argument.height'],\
            "width": arg['argument.width'],\
            "value": arg['result.value']\
        }
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
                self.viewerCallback(arg)    
            except Exception as error:
                arg["exception"] = repr(error)
                self.viewerCallback(arg)
            self.monitordata = None
        self.callbackDoneEvent.set()

if __name__ == '__main__':
    app = QApplication(list())
    PVAPYProvider = PVAPYProvider()
    nargs = len(sys.argv)
    if nargs>=2 :
        channelName = sys.argv[1]
        PVAPYProvider.setChannelName(channelName)
    PVAPYProvider.viewer = Qt_Viewer(PVAPYProvider,"PVAPY")
    sys.exit(app.exec_())


