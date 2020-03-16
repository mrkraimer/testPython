#!/usr/bin/env python

from Dynamic_Viewer import Dynamic_Viewer
from Dynamic_Common  import Dynamic_Channel_Provider,getDynamicRecordName,DynamicRecordData
from pvaccess import *
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

class PVAPYProvider(QObject,Dynamic_Channel_Provider) :
    def __init__(self):
        QObject.__init__(self)
        Dynamic_Channel_Provider.__init__(self)

    def start(self) :
        self.channel = Channel(getDynamicRecordName())
        self.channel.monitor(self.mycallback,'field()')
    def stop(self) :
        self.channel.stopMonitor()
    def done(self) :
        pass
    def mycallback(self,struct) :
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
            self.viewer.callback(arg)
            return
        except Exception as error:
            arg["exception"] = repr(error)
            self.viewer.callback(arg)

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

