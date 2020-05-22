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
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap, QPainter,QImage,qRgb

import sys,time
import numpy as np
import math
            
def toQImage(image,pixelLevels) :
    gray_color_table = [qRgb(i, i, i) for i in range(256)]
    if image is None:
        return QImage()
        
    if len(pixelLevels)==0 :
        colorTable = gray_color_table
    elif  len(pixelLevels)!=2 :
        raise Exception('pixelLevels must of the form (int,int)')
    else :
        indmin = int(pixelLevels[0])
        indmax = int(pixelLevels[1])
        n = indmax -indmin +1
        colorTable = np.empty(n, dtype=np.uint32)
        for ind in range(n) :
            val = indmin + ind
            colorTable[ind] = qRgb(val,val,val)
    if image.dtype==np.uint8 or image.dtype==np.int8 :
        mv = memoryview(image.data)
        data = mv.tobytes()
        if len(image.shape) == 2:
            qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            qimage.setColorTable(colorTable)
            return  qimage

        elif len(image.shape) == 3:
            if image.shape[2] == 3:
                qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                return qimage
            elif image.shape[2] == 4:
                qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_ARGB32);
                return qimage
                
    if image.dtype==np.uint16 or image.dtype==np.int16 :
        # QImage::Format_RGB16
        raise Exception('int16 not yet implemented')
    if image.dtype==np.uint32 or image.dtype==np.int32 :
        # QImage::Format_ARGB32
        raise Exception('int32 not yet implemented')
    if image.dtype==np.uint64 or image.dtype==np.int64 :
        # QImage::Format_RGBA64
        raise Exception('int64 not yet implemented')
    if image.dtype==np.float32 :
        # ???
        raise Exception('float32 not yet implemented')
    if image.dtype==np.float64 :
        # ???
        raise Exception('float64 not yet implemented')
    raise Exception('illegal dtype')

class Worker(QThread):
    signal = pyqtSignal()
    def __init__(self):
        QThread.__init__(self)
        self.exiting = False
        self.image = None
        self.caller = None
        self.pixelLevels = []
        self.scale = int(0)
    def __del__(self):    
        self.exiting = True
        self.wait()
        
    def render(self,image,pixelLevels,caller):    
        self.image = image
        self.caller = caller
        self.pixelLevels = pixelLevels
        self.start()

    def run(self):
        if self.exiting :
           self.signal.emit()
           self.caller.imageDoneEvent.set()
           return
        qimage = toQImage(self.image,self.pixelLevels)
        if self.scale!=0 :
            scale = int(self.scale)
            numx = self.image.shape[1]
            numy = self.image.shape[0]
            if numy>numx :
                qimage = qimage.scaledToWidth(numx*scale)
            else :
                qimage = qimage.scaledToHeight(numy*scale)
    
        painter = QPainter(self.caller)
        painter.drawImage(0,0,qimage)
        while True :
            if painter.end() : break
        self.image = None
        self.pixelLevels = []
        self.scale = int(0)
        self.signal.emit()
        self.caller.imageDoneEvent.set()
        
class NumpyImageZoom() :
    def __init__(self):
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.scale = 1.0
        self.zoomImage = None       
        
    def reset(self) :
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.scale = 1.0
        self.zoomImage = None
        
    def setSize(self,xmax,ymax) :
        self.xmax = xmax
        self.ymax = ymax
        
    def newZoom(self,xsize,ysize,xmin,xmax,ymin,ymax) :
        xmin = self.xmin + int(xmin/self.scale)
        xmax = float(xsize - xmax)/self.scale
        xmax = self.xmax - int(xmax)
        ymin = self.ymin + int(ymin/self.scale)
        ymax = float(ysize - ymax)/self.scale
        ymax = self.ymax - int(ymax)
        nx = xmax -xmin
        excess = nx - int(nx/4)*4
        if excess!=0 : 
            xmax = int(xmax - excess)
        if xmax<=xmin : return False
        if ymax<=ymin : return False
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.isZoom = True
        return True
        
    def getData(self) :
        return (self.xmin,self.xmax,self.ymin,self.ymax)
        
    def scaleImage(self,image,scale) :
        delta = float(scale)
        self.scale = self.scale*delta
        
    def compressImage(self,image,compress) :
        self.image = image[::compress,::compress]
        ny = self.image.shape[0]
        nx = self.image.shape[1]     
        delta = 1.0/float(compress)
        self.scale = self.scale*delta
        return self.image                
        

    def createZoomImage(self,image) :
        zoomImage = image[self.ymin:self.ymax,self.xmin:self.xmax]
        self.zoomImage = zoomImage
        return self.zoomImage
    
        
class NumpyImage(QWidget) :
    def __init__(self,windowTitle='no title',flipy= True,maxsize=800):
        super(QWidget, self).__init__()
        self.setWindowTitle(windowTitle)
        self.maxsize = int(maxsize)
        self.flipy = flipy
        self.thread = Worker()
        self.thread.signal.connect(self.threadDone)
        self.imageDoneEvent = Event()
        self.imageDoneEvent.set()
        self.imageZoom = None
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientZoomCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.isHidden = True
        self.isClosed = False
        self.isActive = False
        self.image = None
        self.ny = 0
        self.nx = 0
        
    def setZoomCallback(self,clientCallback,clientZoom=False) :
        self.clientZoomCallback = clientCallback
        if not clientZoom :
            self.imageZoom  = NumpyImageZoom()
        
    def resetZoom(self) :
        self.imageZoom.reset()
        self.nx = 0
        self.ny = 0
            
    def display(self,pixarray,pixelLevels=[]) :
        self.waitForDone()
        self.imageDoneEvent.clear()
        self.isActive = True
        ny = pixarray.shape[0]
        nx = pixarray.shape[1]
        excess = nx - int(nx/4)*4
        if excess!= 0 :
            raise Exception('invalid width')
        if self.flipy :
            self.image = np.flip(pixarray,0)
        else :
            self.image = pixarray
        geometrySet = False
        if self.imageZoom!=None :
            if self.imageZoom.isZoom: 
                self.image = self.imageZoom.createZoomImage(self.image)
                ny = self.image.shape[0]
                nx = self.image.shape[1]
            else :
                self.imageZoom.setSize(nx,ny)
                maximum = max(ny,nx)
                if maximum>self.maxsize :
                    compress = math.ceil(float(maximum)/self.maxsize)
                    self.image = self.imageZoom.compressImage(self.image,compress)
                    ny = self.image.shape[0]
                    nx = self.image.shape[1]
                    excess = nx - int(nx/4)*4
                    if excess!=0 : print('excess=',excess)
        maximum = max(ny,nx)
        if maximum<int(float(self.maxsize/2)) :
             scale = math.ceil(float(self.maxsize/2)/maximum)
             self.thread.scale = scale
             if self.imageZoom!=None :
                 self.imageZoom.scaleImage(self.image,scale) 
             self.setGeometry(QRect(10, 300,nx*scale,ny*scale))
             geometrySet = True
             self.nx = int(nx*scale)
             self.ny = int(ny*scale)
        if not geometrySet :
            if self.ny!=ny or self.nx!=nx :
                self.ny = ny
                self.nx = nx     
            self.setGeometry(QRect(10, 300,self.nx,self.ny))
        self.pixelLevels = pixelLevels;
        self.update()
        if self.isHidden :
            self.isHidden = False
            self.show()

    def waitForDone(self) :
        if self.isClosed : return
        result = self.imageDoneEvent.wait(3.0)
        if not result : print('waitForDone timeout')

    def threadDone(self) :
        self.imageDoneEvent.set()
        self.isActive = False

    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            self.isHidden = True
            return
        self.isClosed = True

    def mousePressEvent(self,event) :
        if self.isActive : return
        if self.clientZoomCallback==None : return
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
        imageGeometry = self.geometry().getRect()
        xsize = imageGeometry[2]
        ysize = imageGeometry[3]
        xmin = self.mousePressPosition.x()
        xmax = self.mouseReleasePosition.x()
        if xmin>xmax : xmax,xmin = xmin,xmax
        if xmin<0 : xmin = 0
        if xmax>xsize : xmax = xsize
        if self.flipy :
            ymin = self.ny - self.mouseReleasePosition.y()
            ymax = self.ny - self.mousePressPosition.y()
        else :
            ymin = self.mousePressPosition.y()
            ymax = self.mouseReleasePosition.y()
        if ymin>ymax : ymax,ymin = ymin,ymax
        if ymin<0 : ymin = 0
        if ymax>ysize : ymax = ysize
        if ymin>=ymax :
            print('ymin>=ymax')
            return
        if xmin>=xmax :
            print('xmin>=xmax')
            return
        if self.imageZoom==None :
            self.clientZoomCallback((xsize,ysize),(xmin,xmax,ymin,ymax))
            return
        if self.imageZoom.newZoom(xsize,ysize,xmin,xmax,ymin,ymax) :
            self.clientZoomCallback(self.imageZoom.getData())


    def paintEvent(self, ev):
        if self.mousePressed : return
        self.thread.render(self.image,self.pixelLevels,self)
        self.thread.wait()
        
        
        
        

        

