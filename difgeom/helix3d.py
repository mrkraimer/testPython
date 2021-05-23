#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Helix() :
    def __init__(self):
        pass
 
    def show(self,xmax,ymax,b) :
        plt.close('all')
        npts = 500
        t = np.linspace(0,b*npts,npts)
        limit = xmax
        if ymax>xmax : limit = ymax
        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        x = xmax*np.cos(t)
        y = ymax*np.sin(t)
        
        fig, ax = plt.subplots(ncols=1,tight_layout=True,subplot_kw={"projection": "3d"})
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("helix")
        ax.plot3D(x, y, t, 'black')

        dx = -xmax*np.sin(t)
        dy = ymax*np.cos(t)
        dz = np.full(npts,b)
        d2x = -xmax*np.cos(t)
        d2y = -ymax*np.sin(t)
        d2z = np.zeros(npts)

        num = (d2z*dy - d2y*dz)**2 + (d2x*dz - d2z*dx)**2 + (d2y*dx - d2x*dy)**2
        num = num**(1/2)
        deom = (dx*dx + dy*dy + dz*dz)
        deom = deom**(3/2)
        curvature = num/deom
        curvature = curvature
        f, ax1 = plt.subplots()
        ax1.plot(t,curvature)
        ax1.set_title('curvature')
        ax1.set(xlabel="radians")
        radius = 1/curvature
        f, ax = plt.subplots()
        ax.plot(t,radius)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")
        plt.close(1)
        plt.show()

class Viewer(QWidget) :
    def __init__(self,xmax,ymax,b,parent=None):
        super(QWidget, self).__init__(parent)
        self.xmax = xmax
        self.ymax = ymax
        self.b = b
        self.helix = Helix()
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

        bLabel = QLabel("b:")
        self.bText = QLineEdit()
        self.bText.setEnabled(True)
        self.bText.setText(str(self.b))
        self.bText.editingFinished.connect(self.bEvent)
        
        box = QHBoxLayout()
        box.addWidget(self.displayButton)
        box.addWidget(self.xmaxText)
        box.addWidget(self.ymaxText)
        box.addWidget(self.bText)
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

    def bEvent(self) :
        try:
            self.b = float(self.bText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def display(self):
        self.helix.show(self.xmax,self.ymax,self.b)

    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    xmax = 1
    ymax = 1
    b = .1
    nargs = len(sys.argv)
    if nargs >= 2: a = float(sys.argv[1])
    if nargs >= 3: b = float(sys.argv[2])
    if nargs >= 4: c = float(sys.argv[3])
    viewer = Viewer(xmax,ymax,b)
    sys.exit(app.exec_())
