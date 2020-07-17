# DisplayImage.py
from PyQt5.QtWidgets import QWidget,QRubberBand
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from threading import Event
from PyQt5.QtGui import QPainter,QImage
import numpy as np
import math
import time

class ImageToQImage() :
    def __init__(self):
        self.error = str()
    def toQImage(self,image,bytesPerLine=None,Format=0,colorTable=None) :
        try :
            self.error = str('')
            if image is None:
                self.error = 'no image'
                return None
            mv = memoryview(image.data)
            data = mv.tobytes()  
            if Format>0 :
                if bytesPerLine==None :
                    qimage = QImage(data,image.shape[1], image.shape[0],Format)
                else :
                    qimage = QImage(data,image.shape[1], image.shape[0],bytesPerLine,Format)
                if colorTable!=None :
                    qimage.setColorTable(colorTable)
                return qimage    
            if image.dtype==np.uint8 :
                if len(image.shape) == 2:
                    nx = image.shape[1]
                    qimage = QImage(data, image.shape[1], image.shape[0],nx,QImage.Format_Grayscale8)
                    return  qimage
                elif len(image.shape) == 3:
                    if image.shape[2] == 3:
                        nx = image.shape[1]*3
                        qimage = QImage(data, image.shape[1], image.shape[0],nx,QImage.Format_RGB888)
                        return qimage
                    elif image.shape[2] == 4:
                        nx = image.shape[1]*4
                        qimage = QImage(data, image.shape[1], image.shape[0],nx, QImage.Format_RGBA8888)
                        return qimage
                self.error = 'nz must have length 3 or 4'
                return None    
            if image.dtype==np.uint16 :
                if len(image.shape) == 2:
                    nx = image.shape[1]*2
                    qimage = QImage(data, image.shape[1], image.shape[0],nx, QImage.Format_Grayscale16)
                    return  qimage
            self.error = 'unsupported dtype=' + str(image.dtype)
            return None
        except Exception as error:
            self.error = str(error)
            return None

class Worker(QThread):
    def __init__(self,imageSize):
        QThread.__init__(self)
        self.error = str('')
        self.imageToQImage = ImageToQImage()
        self.imageSize = imageSize
        
    def setImageSize(self,imageSize) :
        self.imageSize = imageSize
        
    def render(self,caller,image,bytesPerLine=None,Format=0,colorTable=None): 
        self.error = str('')
        self.image = image
        self.caller = caller
        self.Format = Format
        self.colorTable = colorTable
        self.bytesPerLine = bytesPerLine
        self.start()

    def run(self):
        qimage = self.imageToQImage.toQImage(\
            self.image,bytesPerLine=self.bytesPerLine,Format=self.Format,colorTable=self.colorTable)
        if qimage==None :
            self.error = self.imageToQImage.error
            self.caller.imageDoneEvent.set()
            return
        numx = self.image.shape[1]
        numy = self.image.shape[0]
        if numy>numx :
            qimage = qimage.scaledToHeight(self.imageSize)
        else :
            qimage = qimage.scaledToWidth(self.imageSize)
        painter = QPainter(self.caller)
        painter.drawImage(0,0,qimage)
        while True :
            if painter.end() : break
        self.image = None
        self.caller.imageDoneEvent.set()
        
class NumpyImageZoom() :
    def __init__(self,imageSize):
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        
    def setFullSize(self,nx,ny) :
        self.xmax = nx
        self.ymax = ny
        
    def reset(self) :
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.dtype = None

    def newZoom(self,xsize,ysize,xmin,xmax,ymin,ymax,dtype) :
        xscale = float((self.xmax-self.xmin)/xsize)
        yscale = float((self.ymax-self.ymin)/ysize)     
        delx = (xmax-xmin)*xscale
        dely = (ymax-ymin)*yscale
        if delx>dely :
            dely = delx
        else :
            delx = dely    
        xmin = self.xmin + int(xmin*xscale)
        xmax = int(xmin + delx)
        ymin = self.ymin + int(ymin*yscale)
        ymax = int(ymin + dely) 
        if xmax<=xmin : return False
        if ymax<=ymin : return False
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.isZoom = True
        return True

    def zoomInc(self,inc,imageSize) :
        if not self.isZoom : return False
        xmin = self.xmin + inc
        if xmin<0 : return False
        xmax = self.xmax - inc
        if xmax>imageSize : return False
        if (xmax-xmin)<2.0 : return False
        ymin = self.ymin + inc
        if ymin<0 : return False
        ymax = self.ymax - inc
        if ymax>imageSize : return False
        if (ymax-ymin)<2.0 : return False
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        return True

    def zoomIn(self,imageSize) :
        inc = 1
        return self.zoomInc(inc,imageSize)

    def zoomOut(self,imageSize) :
        inc = -1
        return self.zoomInc(inc,imageSize)

    def getData(self) :
        return (self.xmin,self.xmax,self.ymin,self.ymax)
        
    def createZoomImage(self,image) :
        return image[self.ymin:self.ymax,self.xmin:self.xmax]
    
class NumpyImage(QWidget) :
    def __init__(self,windowTitle='no title',flipy= False,imageSize=800):
        super(QWidget, self).__init__()
        self.setWindowTitle(windowTitle)
        self.imageSize = int(imageSize)
        self.flipy = flipy
        self.thread = Worker(self.imageSize)
        self.imageDoneEvent = Event()
        self.imageDoneEvent.set()
        self.imageZoom = None
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientZoomCallback = None
        self.clientMousePressCallback = None
        self.clientMouseReleaseCallback = None
        self.clientResizeCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.isHidden = True
        self.isClosed = False
        self.image = None
        self.xoffset = 10
        self.yoffset = 300
        self.firstDisplay = True
        
    def setZoomCallback(self,clientCallback,clientZoom=False) :
        self.clientZoomCallback = clientCallback
        if not clientZoom :
            self.imageZoom  = NumpyImageZoom(self.imageSize)
            
    def setMousePressCallback(self,clientCallback) :
        self.clientMousePressCallback = clientCallback
            
    def setMouseReleaseCallback(self,clientCallback) :
        self.clientMouseReleaseCallback = clientCallback

    def setResizeCallback(self,clientCallback) :
        self.clientResizeCallback = clientCallback                  
        
    def resetZoom(self) :
        self.imageZoom.reset()
        
    def zoomIn(self):
        if self.imageZoom==None : return False
        result =  self.imageZoom.zoomIn(self.imageSize)
        if result and self.clientZoomCallback!=None :
            self.clientZoomCallback(self.imageZoom.getData())
        return result

    def zoomOut(self):
        if self.imageZoom==None : return False
        result =  self.imageZoom.zoomOut(self.imageSize)
        if result and self.clientZoomCallback!=None :
            self.clientZoomCallback(self.imageZoom.getData())
        return result     
        
    def setImageSize(self,imageSize) :
        self.imageSize = imageSize
        self.thread.setImageSize(self.imageSize)
        point = self.geometry().topLeft()
        self.xoffset = point.x()
        self.yoffset = point.y()    
        self.setGeometry(QRect(self.xoffset, self.yoffset,self.imageSize,self.imageSize))    
           
            
    def display(self,pixarray,bytesPerLine=None,Format=0,colorTable=None) :
        if not self.imageDoneEvent.isSet :
            result = self.imageDoneEvent.wait(2.0)
            if not result : raise Exception('display timeout')
        self.imageDoneEvent.clear()
        if self.firstDisplay :
            self.setGeometry(QRect(self.xoffset, self.yoffset,self.imageSize,self.imageSize))
            self.firstDisplay = False
        if self.flipy :
            self.image = np.flip(pixarray,0)
        else :
            self.image = pixarray
        
        if self.imageZoom!=None :
            if self.imageZoom.isZoom:
                if len(self.image.shape)==2 and self.image.dtype==np.uint16 :
                    image = np.array(self.image,copy=True)
                    image = image/255
                    self.image = image.astype(np.uint8)
                self.image = self.imageZoom.createZoomImage(self.image)
                
            else :
               self.imageZoom.setFullSize(self.image.shape[1],self.image.shape[0])
        else:
            pass
        self.bytesPerLine = bytesPerLine
        self.Format = Format
        self.colorTable = colorTable
        self.update()
        if self.isHidden :
            self.isHidden = False
            self.show()
        
    def closeEvent(self,event) :
        if not self.okToClose :
            point = self.geometry().topLeft()
            self.xoffset = point.x()
            self.yoffset = point.y()
            self.hide()
            self.isHidden = True
            self.firstDisplay = True
            return
        self.isClosed = True

    def mousePressEvent(self,event) :
        if self.clientMousePressCallback!=None :
            self.clientMousePressCallback(event)
        if self.clientZoomCallback==None : return
        self.mousePressed = True
        self.mousePressPosition = QPoint(event.pos())
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,QSize()))
        self.rubberBand.show()
        
    def mouseMoveEvent(self,event) :
        if not self.mousePressed : return
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,event.pos()).normalized())

    def mouseReleaseEvent(self,event) :
        if self.clientMouseReleaseCallback!=None :
            self.clientMouseReleaseCallback(event)
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
        if ymin>=ymax : return
        if xmin>=xmax : return
        if self.imageZoom==None :
            self.clientZoomCallback((xsize,ysize),(xmin,xmax,ymin,ymax))
            return
        if self.imageZoom.newZoom(xsize,ysize,xmin,xmax,ymin,ymax,self.image.dtype) :
            self.clientZoomCallback(self.imageZoom.getData())

    def resizeEvent(self,event) :
        if self.clientResizeCallback!= None :
            time.sleep(.2)
            imageGeometry = self.geometry().getRect()
            xsize = imageGeometry[2]
            ysize = imageGeometry[3]
            self.clientResizeCallback(event,xsize,ysize)

    def paintEvent(self, ev):
        if self.mousePressed : return
        self.thread.render(self,self.image,self.bytesPerLine,self.Format,self.colorTable)
        self.thread.wait()

