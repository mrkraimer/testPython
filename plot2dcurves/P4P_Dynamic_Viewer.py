#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import Dynamic_Channel_Provider,getDynamicRecordName,DynamicRecordData
from p4p.client.thread import Context
import sys
import time
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal

class P4PProvider(QObject,Dynamic_Channel_Provider) :
    callbacksignal = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)
        self.callbacksignal.connect(self.mycallback)
        self.callbackDoneEvent = Event()
        self.firstCallback = True
        self.isClosed = True
        self.monitorRateOnly = False
        self.ncallbacks = 0
        self.lastTime = time.time() 
        
    def start(self) :
        self.ctxt = Context('pva')
        self.firstCallback = True
        self.isClosed = False
        self.subscription = self.ctxt.monitor(
              getDynamicRecordName(),
              self.p4pcallback,
              request='field()',
              notify_disconnect=True)
    def stop(self) :
        self.isClosed = True
        self.ctxt.close()
    def done(self) :
        pass
    def callback(self,arg) :
        self.viewer.callback(arg)
    def p4pcallback(self,arg) :
        if self.monitorRateOnly :
            self.ncallbacks += 1
            timenow = time.time() 
            timediff = timenow - self.lastTime
            if timediff<1 : return
            print('rate=',round(self.ncallbacks/timediff))
            self.lastTime = timenow
            self.ncallbacks = 0
            return
        if self.isClosed : return
        self.struct = arg;
        self.callbacksignal.emit()
        self.callbackDoneEvent.wait()
        self.callbackDoneEvent.clear()
    def mycallback(self) :
        struct = self.struct
        arg = dict()
        try :
            argtype = str(type(struct))
            if argtype.find('Disconnected')>=0 :
                arg["status"] = "disconnected"
                self.callback(arg)
                self.firstCallback = True
                self.callbackDoneEvent.set()
                return
            if self.firstCallback :
                arg = dict()
                arg["status"] = "connected"
                self.callback(arg)
                self.firstCallback = False
                self.callback(arg)
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
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    p4pProvider = P4PProvider()
    channelName = ""
    nargs = len(sys.argv)
    if nargs>=2 :
        channelName = sys.argv[1]
        p4pProvider.setChannelName(channelName)
    p4pProvider.viewer = Dynamic_Viewer(p4pProvider,"P4P")
    sys.exit(app.exec_())

