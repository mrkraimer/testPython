#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Clover() :
    def __init__(self):
        pass
 
    def show(self,xmax,ymax,zmax,nrot) :
        # r is radians
        npts = 500
        rmax = 2*np.pi
        dr = rmax/npts
        t = np.arange(0, rmax, dr)
        x = xmax*np.sin(nrot*t)*np.cos(t)
        y = ymax*np.sin(nrot*t)*np.sin(t)
        z = np.arange(0, zmax, zmax/npts)
        plt.close("all")
        fig = plt.figure(figsize=(12,4))
        ax = fig.add_subplot(131,projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("clover")
        ax.plot3D(x, y, z, 'black')

        dx = np.gradient(x)
        dy = np.gradient(y)
        dz = np.gradient(z)
        d2x = np.gradient(dx)
        d2y = np.gradient(dy)
        d2z = np.gradient(dz)
        
        num = (d2z*dy - d2y*dz)**2 + (d2x*dz - d2z*dx)**2 +(d2y*dx - d2x*dy)**2
        num = num**(1/2)

        deom = (dx*dx + dy*dy + dz*dz)
        deom = deom**(3/2)
        curvature = num/deom
        ax = fig.add_subplot(132)
        ax.set_title('curvature')
        ax.set(xlabel="radians")
        ax.plot(t,curvature)
        
        radius = 1/curvature
        ax = fig.add_subplot(133)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")
        ax.plot(t,radius)
        plt.show()

class Viewer(QWidget) :
    def __init__(self,xmax,ymax,zmax,nrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.nrot = nrot
        self.clover = Clover()
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
        
        zmaxLabel = QLabel("zmax:")
        self.zmaxText = QLineEdit()
        self.zmaxText.setEnabled(True)
        self.zmaxText.setText(str(self.zmax))
        self.zmaxText.editingFinished.connect(self.zmaxEvent)


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
        box.addWidget(zmaxLabel)
        box.addWidget(self.zmaxText)
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

    def zmaxEvent(self) :
        try:
            self.zmax = float(self.zmaxText.text())
        except Exception as error:
            self.statusText.setText(str(error))


    def nrotEvent(self) :
        try:
            self.nrot = float(self.nrotText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def display(self):
        self.clover.show(self.xmax,self.ymax,self.zmax,self.nrot)

    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    xmax = 1
    ymax = 1
    zmax = 1
    nrot = 3
    nargs = len(sys.argv)
    if nargs >= 2: xmax = float(sys.argv[1])
    if nargs >= 3: ymax = float(sys.argv[2])
    if nargs >= 4: zmax = float(sys.argv[3])
    if nargs >= 5: nrot = float(sys.argv[4])
    viewer = Viewer(xmax,ymax,zmax,nrot)
    sys.exit(app.exec_())
