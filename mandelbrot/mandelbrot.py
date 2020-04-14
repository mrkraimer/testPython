from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
import sys
import numpy as np

pixeltype = "uint8"
pixelmax = 256

class Image_Display(RawImageWidget) :
    def __init__(self,size,parent=None, **kargs):
        RawImageWidget.__init__(self, parent=parent,scaled=False)
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("image")
        self.okToClose = False
        self.setGeometry(QRect(10, 300,size, size))


    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            return
    def display(self,pixarray) :
        self.setImage(pixarray)
    

class Dynamic_Viewer(QWidget) :
    def __init__(self,size,parent=None):
        super(QWidget, self).__init__(parent)
        self.size = size
        self.imageDisplay = Image_Display(size)
        self.width = size
        self.height = size
        self.pixarray = np.full((size,size,3),0,dtype=pixeltype)
        

    def calcIntensity(self,x,y) :
        c = complex(x,y)
        z = complex(0.0,0.0)
        i = 0
        while abs(z) < 2 and i < pixelmax:
            z = z**2 + c
            i += 1
        # Color scheme is that of Julia sets
        color = (i % 8 * 32, i % 16 * 16, i % 32 * 8)
        return color


    def calcRow(self,pixy,y):
        xmin = float(-2.5)
        xmax = float(1.0)
        inc = (xmax-xmin)/float(self.width)
        for i in range(self.width) :
            pixx = i
            x = xmin + i*inc
            color = self.calcIntensity(x,y)
            self.pixarray[pixx][pixy][0] = color[0]
            self.pixarray[pixx][pixy][1] = color[1]
            self.pixarray[pixx][pixy][2] = color[2]

    def calColumn(self):
        ymin = float(-1.0)
        ymax = float(1.0)
        inc = (ymax-ymin)/float(self.height)
        for i in range(self.height) :
            pixy = i
            y = ymin + i*inc
            self.calcRow(pixy,y)
        self.imageDisplay.display(self.pixarray)
        self.imageDisplay.show()
        
    def start(self) :
        self.calColumn()
        



if __name__ == '__main__':
    app = QApplication(list())
    viewer = Dynamic_Viewer(600)
    viewer.start()
    sys.exit(app.exec_())
