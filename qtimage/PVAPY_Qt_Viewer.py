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
        self.channelName = 'TPYqtpeakimageRecord'
        self.connectCallbacksignal.connect(self.connectionCallback)
        self.monitorCallbacksignal.connect(self.monitorCallback)
        self.callbackDoneEvent = Event()
        self.callbackDoneEvent.clear()
        self.channel = None
        self.isStarted = False
        
    def setChannelName(self,channelName) :
        if self.channel!=None and self.isStarted : self.stop()
        self.channel = None
        self.firstStart = True
        self.channelName = channelName
        
    def putInt(self,value,request) :
        if self.channel==None :
            data = dict()
            data["exception"] = "channel is None"
            self.viewerCallback(data)
            return
        self.channel.put(value,request)
        
    def getChannelName(self) :
        return self.channelName

    def start(self) : 
        if self.firstStart :
             self.channel = Channel(self.channelName)
             self.firstStart = False
             self.channel.setConnectionCallback(self.pvapyconnectioncallback)
        self.channel.monitor(self.pvapymonitorcallback,\
            'field(argument{format,height,width},result.value)')
    
    def stop(self) :
        self.isStarted = False;
        if self.channel==None : return
        self.channel.stopMonitor()

    def viewerCallback(self,arg) :
        self.viewer.callback(arg)
    
    def pvapyconnectioncallback(self,arg) :
        data = dict()
        if arg==True :
            data["status"] = "connected"
        elif arg==False :
            data["status"] = "disconnected"
        else :
            data["exception"] = "bad pvapy connection callback =" + str(arg)
        self.connectdata = data
        self.connectCallbacksignal.emit()
        self.callbackDoneEvent.wait()
        self.callbackDoneEvent.clear()
        

    def connectionCallback(self) :
        arg = self.connectdata
        self.connectdata = None
        self.viewerCallback(arg)
        self.callbackDoneEvent.set()
        self.connectdata = None

    def pvapymonitorcallback(self,arg) :
        if self.monitordata==None:
            data = {\
                "format" : arg['argument.format'],\
                "height": arg['argument.height'],\
                "width": arg['argument.width'],\
                "value": arg['result.value']\
            }
            self.monitordata = data
            self.monitorCallbacksignal.emit()
            self.callbackDoneEvent.wait()
            self.callbackDoneEvent.clear()
        else:
            self.monitordata = data

    def monitorCallback(self) :
        arg = dict()
        try:    
            arg['value'] = self.monitordata
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


