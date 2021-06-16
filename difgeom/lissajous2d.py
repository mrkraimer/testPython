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
 
    def show(self,xmul,ymul,nrot) : 
        plt.close('all')
        # r is radians
        npts = 2000
        rmax = 2*np.pi*nrot
        dr = rmax/npts
        t = np.arange(0, rmax, dr)

        #plt.xlim(-1.0,1.0)
        #plt.ylim(-1.0,1.0)
        x = np.sin(xmul*t)
        y = np.cos(ymul*t)
        fig = plt.figure(figsize=(12,4))
        ax = fig.add_subplot(131)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("lissajous")
        ax.plot(x,y)

        ax = fig.add_subplot(132)
        dx = np.gradient(x)
        dy = np.gradient(y)
        d2x = np.gradient(dx)
        d2y = np.gradient(dy)
        num = np.absolute(dx*d2y - d2x*dy)
        deom = (dx*dx + dy*dy)**(3/2)
        curvature = num/deom
        ax.plot(t,curvature)
        ax.set_title("curvature")
        ax.set(xlabel="radians")
      
        radius = 1/curvature
        ax = fig.add_subplot(133)
        ax.plot(t,radius)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")
        plt.show()

class Viewer(QWidget) :
    def __init__(self,xmul,ymul,nrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.xmul = xmul
        self.ymul = ymul
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

    def nrotEvent(self) :
        try:
            self.nrot = float(self.nrotText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def display(self):
        self.lissajous.show(self.xmul,self.ymul,self.nrot)
        
    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    xmul = 1
    ymul = 3
    nrot = 1
    nargs = len(sys.argv)
    if nargs >= 2: a = float(sys.argv[1])
    if nargs >= 3: b = float(sys.argv[2])
    if nargs >= 4: c = float(sys.argv[3])
    viewer = Viewer(xmul,ymul,nrot)
    sys.exit(app.exec_())
