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
    callbacksignal = pyqtSignal()
    def __init__(self):
        self.channel = Channel(getDynamicRecordName())
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)
        self.callbacksignal.connect(self.mycallback)
        self.callbackDoneEvent = Event()
        self.callbackDoneEvent.set()
        self.data = None

    def start(self) : self.channel.monitor(self.pvapycallback,'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass
    def callback(self,arg) :
        self.viewer.callback(arg)
    def pvapycallback(self,arg) :
        data = DynamicRecordData()
        data.name = arg['name']
        data.x = np.copy(arg['x'])
        data.y = np.copy(arg['y'])
        data.xmin = arg['xmin']
        data.xmax = arg['xmax']
        data.ymin = arg['ymin']
        data.ymax = arg['ymax']
        if not self.data:
            self.data = data
            self.callbackDoneEvent.clear()
            self.callbacksignal.emit()
        else:
            self.data = data

    def mycallback(self) :
        while self.data is not None:
            try:
                arg = dict()
                arg['value'] = self.data
                self.data = None
                self.callback(arg)
            except Exception as error:
                arg["exception"] = repr(error)
                self.callback(arg)
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


