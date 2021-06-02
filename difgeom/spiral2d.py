#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Spiral() :
    def __init__(self):
        pass
 
    def curve(self,xmax,ymax,nrot) : 
        plt.close('all')
        # r is radians
        npts = 500
        rmax = 2*np.pi*nrot
        dr = rmax/npts
        t = np.arange(0, rmax, dr)
        limit = xmax
        if ymax>xmax : limit = ymax
        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        #x = xmax*(t/rmax)*np.cos(t)
        #x = (xmax/rmax)*t*np.cos(t)
        maxx = xmax/rmax
        x = maxx*t*np.cos(t)
        maxy = ymax/rmax
        y = maxy*t*np.sin(t)
        plt.axes().set_aspect('equal')
        plt.plot(x, y,scalex=False,scaley=False)
        plt.xlabel("value")
        plt.title("spiral")
        plt.show()

    def curvature(self,xmax,ymax,nrot) : 
        plt.close('all')
        # r is radians
        npts = 500
        rmax = 2*np.pi*nrot
        dr = rmax/npts
        t = np.arange(0, rmax, dr)
        #x = xmax*(t/rmax)*np.cos(t)
        #x = (xmax/rmax)*t*np.cos(t)
        maxx = xmax/rmax
        x = maxx*t*np.cos(t)
        maxy = ymax/rmax
        y = maxy*t*np.sin(t)

        dx = np.gradient(x)
        dy = np.gradient(y)
        d2x = np.gradient(dx)
        d2y = np.gradient(dy)
        num = np.absolute(dx*d2y - d2x*dy)
        deom = (dx*dx + dy*dy)**(3/2)
        curvature = num/deom
        curvature[0] = curvature[2]
        curvature[1] = curvature[2]
        curvature[npts-1] = curvature[npts-3]
        curvature[npts-2] = curvature[npts-3]
        plt.plot(t,curvature)
        plt.title("curvature")
        plt.xlabel("radians")
      
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
        self.spiral = Spiral()
        self.curveButton = QPushButton('curve')
        self.curveButton.setEnabled(True)
        self.curveButton.clicked.connect(self.curve)
        self.curvatureButton = QPushButton('curvature')
        self.curvatureButton.setEnabled(True)
        self.curvatureButton.clicked.connect(self.curvature)

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
        box.addWidget(self.curveButton)
        box.addWidget(self.curvatureButton)
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

    def curve(self):
        self.spiral.curve(self.xmax,self.ymax,self.nrot)
        
    def curvature(self):
        self.spiral.curvature(self.xmax,self.ymax,self.nrot)

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
