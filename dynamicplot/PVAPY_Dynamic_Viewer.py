#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import Dynamic_Channel_Provider,getDynamicRecordName,DynamicRecordData
from pvaccess import *
import sys
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal

class PVAPYProvider(QObject,Dynamic_Channel_Provider) :
    callbacksignal = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)
        self.callbacksignal.connect(self.mycallback)
        self.callbackDoneEvent = Event()

    def start(self) :
        self.channel = Channel(getDynamicRecordName())
        self.channel.monitor(self.pvapycallback,
              'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass
    def pvapycallback(self,arg) :
        self.struct = arg;
        self.callbacksignal.emit()
        self.callbackDoneEvent.wait()
        self.callbackDoneEvent.clear()
    def callback(self,arg) :
        self.viewer.callback(arg)
    def mycallback(self) :
        struct = self.struct
        arg = dict()
        try :
            data = DynamicRecordData()
            data.name = struct['name']
            data.x = struct['x']
            data.y = struct['y']
            data.xmin = struct['xmin']
            data.xmax = struct['xmax']
            data.ymin = struct['ymin']
            data.ymax = struct['ymax']
            arg = dict()
            arg['value'] = data
            self.callback(arg)
            self.callbackDoneEvent.set()
            return
        except Exception as error:
            arg["exception"] = repr(error)
            self.callback(arg)
            self.callbackDoneEvent.set()

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

