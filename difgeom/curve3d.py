#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout
from PyQt5.QtWidgets import QListWidget

class Clover() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
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
    def getz(self): 
        z =  np.arange(0, self.zmax, self.zmax/self.npts)
        return z

class Elipse() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(0, self.rmax, self.dr)
        return self.t
    def getx(self):
        x = self.xmax*np.cos(self.t)
        return x
    def gety(self): 
        y =  self.ymax*np.sin(self.t)
        return y
    def getz(self): 
        z =  np.arange(0, self.zmax, self.zmax/self.npts)
        return z    

class Figure8() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
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
    def getz(self): 
        z =  np.arange(0, self.zmax, self.zmax/self.npts)
        return z    

class Heart() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
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
    def getz(self): 
        z =  np.arange(0, self.zmax, self.zmax/self.npts)
        return z    

class Lissajous() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
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
    def getz(self): 
        z =  np.arange(0, self.zmax, self.zmax/self.npts)
        return z

class Spiral() :
    def __init__(self,npts,xmax,ymax,zmax,nrot,parent=None):
        self.npts = npts
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.nrot = nrot
        self.rmax = 2*np.pi*nrot
        self.dr = self.rmax/npts
    def gett(self): 
        self.t = np.arange(-self.rmax, self.rmax, self.dr)
        return self.t
    def getx(self):
        maxx = self.xmax/self.rmax
        x = maxx*self.t*np.cos(self.t)
        return x
    def gety(self): 
        maxy = self.ymax/self.rmax
        y = maxy*self.t*np.sin(self.t)
        return y
    def getz(self): 
        z =  np.arange(-1,1, 1/self.npts)
        return z    

class CurveDraw() :
    def __init__(self):
        pass

    def draw(self,curve,curveName) : 
        plt.close(None)
        t = curve.gett()
        x = curve.getx()
        y = curve.gety()
        z = curve.getz()
        
        fig = plt.figure(1,figsize=(12,4))
        ax = fig.add_subplot(131,projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(curveName)
        ax.plot3D(x, y, z, 'black')

        ax = fig.add_subplot(132)
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

class DynamicDraw() :
    def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax,curveName):
        plt.close(None)
        self.curveName = curveName
        self.fig = plt.figure(2,figsize=(4,4))
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)
        self.ax.set_zlim(zmin,zmax)
        self.ax.set_title(curveName)
        plt.show()

    def draw(self,curve,num) :
        t = curve.gett()
        x = curve.getx()
        y = curve.gety()
        z = curve.getz()
        if self.curveName == 'spiral' : num = num*2
        x = x[0:num]
        y = y[0:num]
        z = z[0:num]
        self.ax.plot3D(x, y, z,'black')
        plt.draw()
        
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
        self.zmaxInit= [1,1,1,1,1,1]
        self.nrotInit= [3,1,1,1,1,8]
        self.indCurve = 0;
        self.xmax = self.xmaxInit[self.indCurve]
        self.ymax = self.ymaxInit[self.indCurve]
        self.zmax = self.zmaxInit[self.indCurve]
        self.nrot = self.nrotInit[self.indCurve]
        self.curveDraw = CurveDraw()
        self.displayButton = QPushButton('display')
        self.displayButton.setEnabled(True)
        self.displayButton.clicked.connect(self.display)

        self.dynamicButton = QPushButton('dynamic')
        self.dynamicButton.setEnabled(True)
        self.dynamicButton.clicked.connect(self.dynamic)

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
        box.addWidget(self.chooseCurveButton)
        box.addWidget(self.displayButton)
        box.addWidget(self.dynamicButton)
        box.addWidget(xmaxLabel)
        box.addWidget(self.xmaxText)
        box.addWidget(ymaxLabel)
        box.addWidget(self.ymaxText)
        box.addWidget(zmaxLabel)
        box.addWidget(self.zmaxText)
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
                    self.zmax = float(self.zmaxInit[i])
                    self.nrot = float(self.nrotInit[i])
                    self.xmaxText.setText(str(self.xmax))
                    self.ymaxText.setText(str(self.ymax))
                    self.zmaxText.setText(str(self.zmax))
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

    def zmaxEvent(self) :
        try:
            self.zmax = float(self.zmaxText.text())
        except Exception as error:
            print(str(error))

    def nrotEvent(self) :
        try:
            self.nrot = float(self.nrotText.text())
        except Exception as error:
            print(str(error))

    def display(self):
        curve = self.curves[self.indCurve]
        curve = curve(self.npts,self.xmax,self.ymax,self.zmax,self.nrot)
        curveName = self.curveNames[self.indCurve]
        self.curveDraw.draw(curve,curveName)

    def dynamic(self):
        curve = self.curves[self.indCurve]
        curve = curve(self.npts,self.xmax,self.ymax,self.zmax,self.nrot)
        curveName = self.curveNames[self.indCurve]
        t = curve.gett()
        x = curve.getx()
        y = curve.gety()
        z = curve.getz()
        xmin = x.min()
        xmax = x.max()
        ymin = y.min()
        ymax = y.max()
        zmin = z.min()
        zmax = z.max()
        dynamicDraw = DynamicDraw(xmin,xmax,ymin,ymax,zmin,zmax,curveName)
        inc = 8
        for i in range(inc,self.npts,inc) :
            QApplication.processEvents()
            dynamicDraw.draw(curve,i)

    def closeEvent(self, event) :
        QApplication.closeAllWindows()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Viewer()
    sys.exit(app.exec_())
