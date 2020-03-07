#!/usr/bin/env python

import sys
import numpy as np
from Dynamic_Viewer import Data_Provider,Dynamic_Viewer
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

class LineProvider(QObject,Data_Provider) :
    def __init__(self):
        QObject.__init__(self)
        Data_Provider.__init__(self)
        self.dataName = "line"
    def getDataName(self) :
        return self.dataName
    def callback(self) :
        npts = 1000
        x = np.arange(npts)
        y = np.arange(npts)
        return { "x" : x, "y" : y}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dataProvider = LineProvider()
    viewer = Dynamic_Viewer(dataProvider)
    sys.exit(app.exec_())
