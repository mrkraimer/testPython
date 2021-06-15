#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Lissajous() :
    def __init__(self):
        pass
 
    def show(self,xmul,ymul,zmax,nrot) :
        # r is radians
        npts = 500
        rmax = 2*np.pi
        dr = rmax/npts
        t = np.arange(0, rmax, dr)
        limit = xmul
        if ymul>xmul : limit = ymul
        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        x = np.sin(xmul*t)
        y = np.cos(ymul*t)
        z = np.arange(0, zmax, zmax/npts)
        fig = plt.figure()
        plt.close('all')
        ax = plt.axes(projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("lissajous")
        ax.plot3D(x, y, z, 'black')
        plt.show()

class Viewer(QWidget) :
    def __init__(self,xmul,ymul,zmax,nrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.xmul = xmul
        self.ymul = ymul
        self.zmax = zmax
        self.nrot = nrot
        self.lissajous = Lissajous()
        self.displayButton = QPushButton('display')
        self.displayButton.setEnabled(True)
        self.displayButton.clicked.connect(self.display)

        xmulLabel = QLabel("xmul:")
        self.xmulText = QLineEdit()
        self.xmulText.setEnabled(True)
        self.xmulText.setText(str(self.xmul))
        self.xmulText.editingFinished.connect(self.xmulEvent)

        ymulLabel = QLabel("ymul:")
        self.ymulText = QLineEdit()
        self.ymulText.setEnabled(True)
        self.ymulText.setText(str(self.ymul))
        self.ymulText.editingFinished.connect(self.ymulEvent)
        
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
        box.addWidget(xmulLabel)
        box.addWidget(self.xmulText)
        box.addWidget(ymulLabel)
        box.addWidget(self.ymulText)
        box.addWidget(zmaxLabel)
        box.addWidget(self.zmaxText)
        box.addWidget(nrotLabel)
        box.addWidget(self.nrotText)
        self.setLayout(box)
        self.show()
        

    def xmulEvent(self) :
        try:
            self.xmul = float(self.xmulText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def ymulEvent(self) :
        try:
            self.ymul = float(self.ymulText.text())
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
        self.lissajous.show(self.xmul,self.ymul,self.zmax,self.nrot)

    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    xmul = 1
    ymul = 3
    zmax = 1
    nrot = 1
    nargs = len(sys.argv)
    if nargs >= 2: xmul = float(sys.argv[1])
    if nargs >= 3: ymul = float(sys.argv[2])
    if nargs >= 4: zmax = float(sys.argv[3])
    if nargs >= 5: nrot = float(sys.argv[4])
    viewer = Viewer(xmul,ymul,zmax,nrot)
    sys.exit(app.exec_())
