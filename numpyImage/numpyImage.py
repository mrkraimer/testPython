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

class NotImplementedException:
    pass

gray_color_table = [qRgb(i, i, i) for i in range(256)]

def toQImage(im):
    if im is None:
        return QImage()

    if im.dtype == np.uint8:
        mv = memoryview(im.data)
        data = mv.tobytes()
        if len(im.shape) == 2:
            qim = QImage(data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return  qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                return qim
            elif im.shape[2] == 4:
                qim = QImage(data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim

    raise NotImplementedException

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

    def waitForDone(self) :
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
            self.clientCallback(self.mousePressPosition,self.mouseReleasePosition)

    def clientReleaseEvent(self,clientCallback) :
        self.clientCallback = clientCallback

    def paintEvent(self, ev):
        if self.mousePressed : return
        self.thread.render(self.image,self)
        self.thread.wait()
        
        
        
        

        

