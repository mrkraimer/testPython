#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout
from PyQt5.QtWidgets import QListWidget

class Clover() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x =  self.xmax*np.sin(self.nrot*self.t)*np.cos(self.t)
        return x
    def gety(self): 
        y =  self.ymax*np.sin(self.nrot*self.t)*np.sin(self.t)
        return y

class Elipse() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x =  self.xmax*np.cos(self.t)
        return x
    def gety(self): 
        y =  self.ymax*np.sin(self.t)
        return y

class Figure8() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x =  self.xmax*np.sin(self.t)*np.cos(self.t)
        return x
    def gety(self): 
        y =  self.ymax*np.sin(self.t)
        return y

class Heart() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x =  self.xmax*(1.0 - np.cos(self.t)*np.cos(self.t))*np.sin(self.t)
        return x
    def gety(self): 
        y =  self.ymax*(1.0 - np.cos(self.t)*np.cos(self.t)*np.cos(self.t))*np.cos(self.t)
        return y

class Lissajous() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x = np.sin(self.xmax*self.t)
        return x
    def gety(self): 
        y =  np.cos(self.ymax*self.t)
        return y

class Spiral() :
    def __init__(self,npts,xmax,ymax,nrot,parent=None):
        self.xmax = xmax
        self.ymax = ymax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        maxx = self.xmax/self.rmax
        x = maxx*self.t*np.cos(self.t)
        return x
    def gety(self): 
        maxy = self.ymax/self.rmax
        y = maxy*self.t*np.sin(self.t)
        return y

class CurveDraw() :
    def __init__(self):
        pass
 
    def show(self,curve,curveName) : 
        plt.close('all')
        t = curve.gett()
        x = curve.getx()
        y = curve.gety()
        
        fig = plt.figure(figsize=(12,4))
        ax = fig.add_subplot(131)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(curveName)
        ax.plot(x,y)

        ax = fig.add_subplot(132)
        dx = np.gradient(x)
        dy = np.gradient(y)
        d2x = np.gradient(dx)
        d2y = np.gradient(dy)
        num = np.absolute(dx*d2y - d2x*dy)
        deom = (dx*dx + dy*dy)**(3/2)
        curvature = num/deom
        for i in range(0,len(curvature)) :
            if curvature[i]<.1 : curvature[i] = .1
            if curvature[i]>10.0 : curvature[i] = 10.0
        ax.plot(t,curvature)
        ax.set_title("curvature")
        ax.set(xlabel="radians")
      
        radius = 1/curvature
        ax = fig.add_subplot(133)
        ax.plot(t,radius)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")
        plt.show()

class ChooseCurve(QListWidget) :
    def __init__(self,curveNames,callback,parent=None):
        super(QListWidget, self).__init__(parent)
        self.curveNames = curveNames
        self.callback = callback
        self.addItems(self.curveNames)
        self.setEnabled(True)
        self.itemClicked.connect(self.curveChoiceEvent)
    def curveChoiceEvent(self,item) :
        self.callback(item) 
         


class Viewer(QWidget) :
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
        self.npts = 1000
        self.curves = [Clover,Elipse,Figure8,Heart,Lissajous,Spiral]
        self.curveNames = ["clover","elipse","figure8","heart","lissajous","spiral"]
        self.xmaxInit= [1,1,1,1,2,1]
        self.ymaxInit= [1,1,1,1,3,1]
        self.nrotInit= [3,1,1,1,1,1]
        self.indCurve = 0;
        self.xmax = self.xmaxInit[self.indCurve]
        self.ymax = self.ymaxInit[self.indCurve]
        self.nrot = self.nrotInit[self.indCurve]
        self.curveDraw = CurveDraw()
        self.displayButton = QPushButton('display')
        self.displayButton.setEnabled(True)
        self.displayButton.clicked.connect(self.display)

        self.chooseCurve = ChooseCurve(self.curveNames,self.curveChoiceEvent)
        self.chooseCurveButton = QPushButton('chooseCurve')
        self.chooseCurveButton.setEnabled(True)
        self.chooseCurveButton.clicked.connect(self.chooseCurveEvent)

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
        box.addWidget(self.chooseCurveButton)
        box.addWidget(self.displayButton)
        box.addWidget(xmaxLabel)
        box.addWidget(self.xmaxText)
        box.addWidget(ymaxLabel)
        box.addWidget(self.ymaxText)
        box.addWidget(nrotLabel)
        box.addWidget(self.nrotText)
        self.setLayout(box)
        self.move(10,10)
        self.show()

    def chooseCurveEvent(self,item) :
        self.chooseCurve.show()

    def curveChoiceEvent(self,item) :
        try:
            self.chooseCurve.hide()
            value = item.text()
            for i in range(0,len(self.curveNames)) :
                if self.curveNames[i]==value :
                    self.indCurve = i
                    self.xmax = float(self.xmaxInit[i])
                    self.ymax = float(self.ymaxInit[i])
                    self.nrot = float(self.nrotInit[i])
                    self.xmaxText.setText(str(self.xmax))
                    self.ymaxText.setText(str(self.ymax))
                    self.nrotText.setText(str(self.nrot))
                    return

            raise Exception('did not find choice')
        except Exception as error:
            print(str(error))        

    def xmaxEvent(self) :
        try:
            self.xmax = float(self.xmaxText.text())
        except Exception as error:
            print(str(error))

    def ymaxEvent(self) :
        try:
            self.ymax = float(self.ymaxText.text())
        except Exception as error:
            print(str(error))

    def nrotEvent(self) :
        try:
            self.nrot = float(self.nrotText.text())
        except Exception as error:
            print(str(error))

    def display(self):
        curve = self.curves[self.indCurve]
        curve = curve(self.npts,self.xmax,self.ymax,self.nrot)
        curveName = self.curveNames[self.indCurve]
        self.curveDraw.show(curve,curveName)
       
    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Viewer()
    sys.exit(app.exec_())
