#!/usr/bin/env python
from MandelbrotCreatePython import MandelbrotCreatePython
from PyQt5.QtWidgets import QApplication
from DisplayImage import Viewer
import sys

if __name__ == '__main__':
    app = QApplication(list())
    mandelbrotCreate = MandelbrotCreatePython()
    viewer = Viewer(mandelbrotCreate)
    sys.exit(app.exec_())
