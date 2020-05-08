# DisplayImage.py
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QVBoxLayout,QGridLayout,QGroupBox
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from threading import Event

from PyQt5.QtGui import QPixmap, QPainter,QImage,qRgb

import sys,time
import numpy as np
import math

def toQImage(image):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]
    if image is None:
        return QImage()

    if image.dtype==np.uint8 or image.dtype==np.int8:
        mv = memoryview(image.data)
        data = mv.tobytes()
        if len(image.shape) == 2:
            qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            qimage.setColorTable(gray_color_table)
            return  qimage

        elif len(image.shape) == 3:
            if image.shape[2] == 3:
                qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                return qimage
            elif image.shape[2] == 4:
                qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_ARGB32);
                return qimage

    raise Exception('illegal dtype')

class Worker(QThread):
    signal = pyqtSignal()
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.image = None
        self.caller = None
    def __del__(self):    
        self.exiting = True
        self.wait()
        
    def render(self,image,caller):    
        self.image = image
        self.caller = caller
        self.start()

    def run(self):
        if self.exiting :
           self.signal.emit()
           self.caller.imageDoneEvent.set()
           return
        qimage = toQImage(self.image)
        painter = QPainter(self.caller)
        painter.drawImage(0,0,qimage)
        while True :
            if painter.end() : break
        self.image = None
        self.signal.emit()
        self.caller.imageDoneEvent.set()
    


class NumpyImage(QWidget) :
    def __init__(self,windowTitle,parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowTitle(windowTitle)
        self.thread = Worker()
        self.thread.signal.connect(self.threadDone)
        self.imageDoneEvent = Event()
        self.imageDoneEvent.set()
        self.width = 0
        self.height = 0
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.isHidden = True
        self.isClosed = False

    def waitForDone(self) :
        if self.isClosed : return
        result = self.imageDoneEvent.wait(1.0)
        if not result : print('waitForDone timeout')

    def threadDone(self) :
        self.imageDoneEvent.set()

    def display(self,pixarray) :
        self.waitForDone()
        self.imageDoneEvent.clear()
        height = pixarray.shape[0]
        width = pixarray.shape[1]
        if self.width!=width or self.height!=height :
            self.width = width
            self.height = height
            self.setGeometry(QRect(10, 300,self.width,self.height))
        self.image = np.flip(pixarray,0)
        self.update()
        QApplication.processEvents()
        if self.isHidden :
            self.isHidden = False
            self.show()

    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            self.isHidden = True
            return
        self.isClosed = True

    def mousePressEvent(self,event) :
        self.mousePressed = True
        self.mousePressPosition = QPoint(event.pos())
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,QSize()))
        self.rubberBand.show()
        
    def mouseMoveEvent(self,event) :
        if not self.mousePressed : return
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,event.pos()).normalized())

    def mouseReleaseEvent(self,event) :
        if not self.mousePressed : return
        self.mouseReleasePosition = QPoint(event.pos())
        self.rubberBand.hide()
        self.mousePressed = False
        if not self.clientCallback==None : 
            imageGeometry = self.geometry().getRect()
            xsize = imageGeometry[2]
            ysize = imageGeometry[3]
            xmin = self.mousePressPosition.x()
            xmax = self.mouseReleasePosition.x()
            if xmin>xmax : xmax,xmin = xmin,xmax
            if xmin<0 : xmin = 0
            if xmax>xsize : xmax = xsize
            ymin = self.height - self.mouseReleasePosition.y()
            ymax = self.height - self.mousePressPosition.y()
            if ymin>ymax : ymax,ymin = ymin,ymax
            if ymin<0 : ymin = 0
            if ymax>ysize : ymax = ysize
            self.clientCallback((xsize,ysize),(xmin,xmax,ymin,ymax))

    def clientReleaseEvent(self,clientCallback) :
        self.clientCallback = clientCallback

    def paintEvent(self, ev):
        if self.mousePressed : return
        self.thread.render(self.image,self)
        self.thread.wait()
        
        
        
        

        

