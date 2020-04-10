#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import Dynamic_Channel_Provider,getDynamicRecordName,DynamicRecordData
from pvaccess import *
import sys
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal
import numpy as np

class PVAPYProvider(QObject,Dynamic_Channel_Provider) :
    monitorCallbacksignal = pyqtSignal()
    connectCallbacksignal = pyqtSignal()
    def __init__(self):
        self.channel = Channel(getDynamicRecordName())
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)
        self.connectCallbacksignal.connect(self.myconnectionCallback)
        self.monitorCallbacksignal.connect(self.mymonitorCallback)
        self.callbackDoneEvent = Event()
        self.callbackDoneEvent.set()
        self.monitordata = None
        self.connectdata = None

    def start(self) : 
        self.channel.setConnectionCallback(self.pvapyconnectioncallback)
        self.channel.monitor(self.pvapymonitorcallback,'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass

    def viewerCallback(self,arg) :
        self.viewer.callback(arg)

    def pvapyconnectioncallback(self,arg) :
        data = dict()
        data["status"] = arg
        self.connectdata = data
        self.callbackDoneEvent.clear()
        self.connectCallbacksignal.emit()

    def myconnectionCallback(self) :
        try:
            arg = self.connectdata
            viewerarg =  dict()
            if arg["status"] == True :
                viewerarg["status"] = "connected"
            elif arg["status"] == False :
                viewerarg["status"] = "disconnected"
            else :
                viewerarg["status"] = "bad status"
            self.connectdata = None
            self.viewerCallback(viewerarg)
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

    def mymonitorCallback(self) :
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
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    PVAPYProvider = PVAPYProvider()
    channelName = ""
    nargs = len(sys.argv)
    if nargs>=2 :
        channelName = sys.argv[1]
        PVAPYProvider.setChannelName(channelName)
    PVAPYProvider.viewer = Dynamic_Viewer(PVAPYProvider,"PVAPY")
    sys.exit(app.exec_())


