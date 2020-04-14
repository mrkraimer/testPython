from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
import sys,time
import numpy as np
import math

class InitialValues() :
    pixeltype = "uint8"
    pixelmax = 256
    xmin = float(-2.5)
    xmax = float(1.0)
    ymin = float(-1.0)
    ymax = float(1.0)
    maxsize = 800
    yxratio = (ymax-ymin)/(xmax-xmin)
    if yxratio>1.0 :
        height = int(maxsize)
        width = math.ceil(height*yxratio)
    else :
        width = int(maxsize)
        height = math.ceil(width*yxratio)
    print('yxratio=',yxratio,' height=',height, ' width=',width)
    xinc = (xmax-xmin)/float(width)
    yinc = (ymax-ymin)/float(height)



class Image_Display(RawImageWidget) :
    def __init__(self,width,height,parent=None, **kargs):
        RawImageWidget.__init__(self, parent=parent,scaled=False)
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("image")
        self.okToClose = False
        self.width = width
        self.height = height

    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            return

    def display(self,pixarray) :
        self.setGeometry(QRect(10, 300,self.width,self.height))
        self.setImage(pixarray)
    

class Dynamic_Viewer(QWidget) :
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
        ini = InitialValues()
        self.pixeltype = ini.pixeltype
        self.pixelmax = ini.pixelmax
        self.xmin = ini.xmin
        self.xmax = ini.xmax
        self.ymin = ini.ymin
        self.ymax = ini.ymax
        self.height = ini.height
        self.width = ini.width
        self.xinc = ini.xinc
        self.yinc = ini.yinc
        self.pixarray = np.full((self.width,self.height,3),self.pixelmax,dtype=self.pixeltype)
        
    def calcIntensity(self,x,y) :
        c = complex(x,y)
        z = complex(0.0,0.0)
        i = 0
        while abs(z) < 2 and i < self.pixelmax:
            z = z**2 + c
            i += 1
        # Color scheme is that of Julia sets
        color = (i % 8 * 32, i % 16 * 16, i % 32 * 8)
        return color

    def calcRow(self,pixy,y):
        for i in range(self.width) :
            pixx = i
            x = self.xmin + i*self.xinc
            color = self.calcIntensity(x,y)
            self.pixarray[pixx][pixy][0] = color[0]
            self.pixarray[pixx][pixy][1] = color[1]
            self.pixarray[pixx][pixy][2] = color[2]

    def calColumn(self):
        for i in range(self.height) :
            pixy = i
            y = self.ymin + i*self.yinc
            self.calcRow(pixy,y)
        self.imageDisplay = Image_Display(self.width,self.height)
        self.imageDisplay.display(self.pixarray)
        self.imageDisplay.show()
        
    def start(self) :
        self.calColumn()
        

if __name__ == '__main__':
    app = QApplication(list())
    viewer = Dynamic_Viewer()
    viewer.start()
    sys.exit(app.exec_())
