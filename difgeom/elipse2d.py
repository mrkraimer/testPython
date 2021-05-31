#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Ellipse() :
    def __init__(self):
        pass
 
    def show(self,xmax,ymax,nrot) : 
        plt.close('all')
        min = 0.0
        max = 2*np.pi*nrot
        npts = 500
        inc = (max-min)/npts
        t = np.arange(min, max, inc)
        limit = xmax
        if ymax>xmax : limit = ymax
        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        x = xmax*np.cos(t)
        y = ymax*np.sin(t)

        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        plt.axes().set_aspect('equal')
        plt.plot(x, y,scalex=False,scaley=False)
        plt.xlabel("value")
        plt.title("ellipse")

        dx = -xmax*np.sin(t)
        dy = ymax*np.cos(t)
        d2x = -xmax*np.cos(t)
        d2y = -ymax*np.sin(t)

        num = np.absolute(dx*d2y - d2x*dy)
        deom = (dx*dx + dy*dy)**(3/2)
        curvature = num/deom
        f, ax = plt.subplots()
        ax.plot(t,curvature)
        ax.set_title('curvature')
        ax.set(xlabel="radians")
        radius = 1/curvature
        f, ax = plt.subplots()
        ax.plot(t,radius)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")
        plt.show()

class Viewer(QWidget) :
    def __init__(self,xmax,ymax,nrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.ellipse = Ellipse()
        self.displayButton = QPushButton('display')
        self.displayButton.setEnabled(True)
        self.displayButton.clicked.connect(self.display)

        xmaxLabel = QLabel("xmax:")
        self.xmaxText = QLineEdit()
        self.xmaxText.setEnabled(True)
        self.xmaxText.setText(str(self.xmax))
        self.xmaxText.editingFinished.connect(self.xmaxEvent)

        ymaxLabel = QLabel("ymax:")
        self.ymaxText = QLineEdit()
        self.ymaxText.setEnabled(True)
        self.ymaxText.setText(str(self.ymax))
        self.ymaxText.editingFinished.connect(self.ymaxEvent)

        nrotLabel = QLabel("nrot:")
        self.nrotText = QLineEdit()
        self.nrotText.setEnabled(True)
        self.nrotText.setText(str(self.nrot))
        self.nrotText.editingFinished.connect(self.nrotEvent)
        
        box = QHBoxLayout()
        box.addWidget(self.displayButton)
        box.addWidget(xmaxLabel)
        box.addWidget(self.xmaxText)
        box.addWidget(ymaxLabel)
        box.addWidget(self.ymaxText)
        box.addWidget(nrotLabel)
        box.addWidget(self.nrotText)
        self.setLayout(box)
        self.show()
        

    def xmaxEvent(self) :
        try:
            self.xmax = float(self.xmaxText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def ymaxEvent(self) :
        try:
            self.ymax = float(self.ymaxText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def nrotEvent(self) :
        try:
            self.nrot = float(self.nrotText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def display(self):
        self.ellipse.show(self.xmax,self.ymax,self.nrot)

    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    xmax = 1
    ymax = 1
    nrot = 1
    nargs = len(sys.argv)
    if nargs >= 2: a = float(sys.argv[1])
    if nargs >= 3: b = float(sys.argv[2])
    if nargs >= 4: c = float(sys.argv[3])
    viewer = Viewer(xmax,ymax,nrot)
    sys.exit(app.exec_())
