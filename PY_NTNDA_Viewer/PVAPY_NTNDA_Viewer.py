#!/usr/bin/env python
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

author Marty Kraimer
    latest date 2020.03.02
    original development started 2019.12
'''

from NTNDA_Viewer import NTNDA_Viewer
from pvaccess import *
import sys
from threading import Event
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject,pyqtSignal

class PVAPYProvider(QObject) :
    monitorCallbacksignal = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        self.monitordata = None
        self.monitorCallbacksignal.connect(self.monitorCallback)
        self.callbackDoneEvent = Event()
        self.channelName = '13SIM1:Pva1:Image'
        self.isStarted = False
        
    def setChannelName(self,channelName) :
        self.channelName = channelName
        
    def getChannelName(self) :
        return self.channelName

    def start(self) :
        if self.isStarted : self.stop()
        self.isStarted = True
        self.channel = Channel(self.channelName)
        self.channel.monitor(self.pvapymonitorcallback,
              'field(value,dimension,codec,compressedSize,uncompressedSize)')
    def stop(self) :
        self.isStarted = False;
        self.channel.stopMonitor()
        
    def callViewerCallback(self,arg) :
        self.NTNDA_Viewer.callback(arg)
        
    def pvapymonitorcallback(self,arg) :
        if self.monitordata==None:
            self.monitordata = arg
            self.monitorCallbacksignal.emit()
            self.callbackDoneEvent.wait()
            self.callbackDoneEvent.clear()
        else:
            self.monitordata = arg
    
    def monitorCallback(self) :
        while not self.monitordata==None :
            try:
                arg = dict()
                val = self.monitordata['value'][0]
                if len(val) != 1 :
                    raise Exception('value length not 1')
                element = None
                for x in val :
                    element = x
                if element == None : 
                    raise Exception('value is not numpy  array')
                value = val[element]
                arg['value'] = value
                arg['dimension'] = self.monitordata['dimension']
                codec = self.monitordata['codec']
                codecName = codec['name']
                if len(codecName)<1 :
                    arg['codec'] = self.monitordata['codec']
                else :
                    parameters = codec['parameters']
                    typevalue = parameters[0]['value']
                    cod = dict()
                    cod['name'] = codecName
                    cod['parameters'] = typevalue
                    arg['codec'] = cod
                arg['compressedSize'] = self.monitordata['compressedSize']
                arg['uncompressedSize'] = self.monitordata['uncompressedSize']
                self.callViewerCallback(arg)    
            except Exception as error:
                arg = dict()
                arg["exception"] = repr(error)
                self.callViewerCallback(arg)
            self.monitordata = None
        self.callbackDoneEvent.set()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    PVAPYProvider = PVAPYProvider()
    nargs = len(sys.argv)
    if nargs>=2 :
        channelName = sys.argv[1]
        PVAPYProvider.setChannelName(channelName)
    viewer = NTNDA_Viewer(PVAPYProvider,"PVAPY")
    sys.exit(app.exec_())

