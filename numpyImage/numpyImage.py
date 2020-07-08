# DisplayImage.py
from PyQt5.QtWidgets import QWidget,QRubberBand,QApplication
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from threading import Event
from PyQt5.QtGui import QPainter,QImage
import numpy as np
import math

def compute32bitExcess(nx,dtype) :
    div = 0
    if dtype==np.uint8 or dtype==np.int8 :
        div = 4
    elif dtype==np.uint16 or dtype==np.int16 :
        div = 2
    else : return 0
    excess = nx - int(nx/div)*div
    if excess<0 or excess>3 :
        print('compute32bitExcess nx=',int(nx),' div=',div)
    return excess

class ImageToQImage() :
    def __init__(self):
        self.error = str()
    def toQImage(self,image,Format=0,colorTable=None) :
        try :
            self.error = str('')
            if image is None:
                self.error = 'no image'
                return None
            mv = memoryview(image.data)
            data = mv.tobytes()  
            if Format>0 :
                qimage = QImage(data,image.shape[1], image.shape[0],Format)
                if colorTable!=None :
                    qimage.setColorTable(colorTable)
                return qimage    
            if image.dtype==np.uint8 :
                if len(image.shape) == 2:
                    qimage = QImage(data, image.shape[1], image.shape[0],QImage.Format_Grayscale8)
                    return  qimage
                elif len(image.shape) == 3:
                    if image.shape[2] == 3:
                        qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                        return qimage
                    elif image.shape[2] == 4:
                        qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_RGBA8888)
                        return qimage
                self.error = 'nz must have length 3 or 4'
                return None    
            if image.dtype==np.uint16 :
                if len(image.shape) == 2:
                    qimage = QImage(data, image.shape[1], image.shape[0], QImage.Format_Grayscale16)
                    return  qimage
            self.error = 'unsupported dtype=' + str(image.dtype)
            return None
        except Exception as error:
            self.error = str(error)
            return None

class Worker(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.scale = int(0)
        self.error = str('')
        self.imageToQImage = ImageToQImage()
        
    def setScale(self,scale) :
        self.scale = scale    
        
    def render(self,caller,image,Format=0,colorTable=None):  
        self.error = str('')
        self.image = image
        self.caller = caller
        self.Format = Format
        self.colorTable = colorTable
        self.start()

    def run(self):
        qimage = self.imageToQImage.toQImage(self.image,Format=self.Format,colorTable=self.colorTable)
        if qimage==None :
            self.error = self.imageToQImage.error
            self.caller.imageDoneEvent.set()
            return
        if self.scale!=int(0) :
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
        self.scale = int(0)
        self.caller.imageDoneEvent.set()
        
class NumpyImageZoom() :
    def __init__(self):
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.scale = 1.0     
        
    def reset(self) :
        self.isZoom = False
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.scale = 1.0
        self.dtype = None
        
    def setSize(self,ymax,xmax) :
        self.ymax = ymax
        self.xmax = xmax
        
    def newZoom(self,xsize,ysize,xmin,xmax,ymin,ymax,dtype) :
        xmin = self.xmin + int(xmin/self.scale)
        xmax = float(xsize - xmax)/self.scale
        xmax = self.xmax - int(xmax)
        ymin = self.ymin + int(ymin/self.scale)
        ymax = float(ysize - ymax)/self.scale
        ymax = self.ymax - int(ymax)
        nx = xmax -xmin
        excess = compute32bitExcess(nx,dtype)
        if excess!=0 :  xmax = int(xmax - excess)
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
        
    def scaleImage(self,scale) :
        self.scale = scale
        
#    def compressImage(self,image,compress) :
#        self.scale = 1.0/compress
#        self.ymax = image.shape[0]
#        self.xmax = image.shape[1]
#        image = image[::compress,::compress]
#        return image                
        
    def createZoomImage(self,image) :
        return image[self.ymin:self.ymax,self.xmin:self.xmax]
    
        
class NumpyImage(QWidget) :
    def __init__(self,windowTitle='no title',flipy= False,maxsize=800):
        super(QWidget, self).__init__()
        self.setWindowTitle(windowTitle)
        self.maxsize = int(maxsize)
        self.flipy = flipy
        self.thread = Worker()
        self.imageDoneEvent = Event()
        self.imageDoneEvent.set()
        self.imageZoom = None
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientZoomCallback = None
        self.clientMousePressCallback = None
        self.clientMouseReleaseCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.isHidden = True
        self.isClosed = False
        self.image = None
        self.ny = 0
        self.nx = 0
        self.xoffset = 10
        self.yoffset = 300
        
    def setZoomCallback(self,clientCallback,clientZoom=False) :
        self.clientZoomCallback = clientCallback
        if not clientZoom :
            self.imageZoom  = NumpyImageZoom()
            
    def setMousePressCallback(self,clientCallback) :
        self.clientMousePressCallback = clientCallback
            
    def setMouseReleaseCallback(self,clientCallback) :
        self.clientMouseReleaseCallback = clientCallback           
        
        
    def resetZoom(self) :
        self.imageZoom.reset()
        self.nx = 0
        self.ny = 0
            
    def display(self,pixarray,Format=0,colorTable=None) :
        if not self.imageDoneEvent.isSet :
            result = self.imageDoneEvent.wait(2.0)
            if not result : raise Exception('display timeout')
        self.imageDoneEvent.clear()
        ny = pixarray.shape[0]
        nx = pixarray.shape[1]
        if self.flipy :
            self.image = np.flip(pixarray,0)
        else :
            self.image = pixarray
        maximum = max(ny,nx)
        if maximum>self.maxsize :
            compress = math.ceil(float(maximum)/self.maxsize)
            self.image = self.image[::compress,::compress]
            ny = self.image.shape[0]
            nx = self.image.shape[1]
        else:
            pass    
        if self.imageZoom!=None :
            if self.imageZoom.isZoom: 
                self.image = self.imageZoom.createZoomImage(self.image)
                ny = self.image.shape[0]
                nx = self.image.shape[1]
                maximum = max(ny,nx)
                if maximum<int(float(self.maxsize/2)) :
                    scale = math.ceil(float(self.maxsize/2)/maximum)
                else :
                    scale = 1.0
                self.thread.setScale(scale)
                self.imageZoom.scaleImage(scale)
                nx = int(nx*scale)
                ny = int(ny*scale)
            else :
                self.imageZoom.setSize(ny,nx)
        else:
            pass
        
        excess = compute32bitExcess(nx,self.image.dtype)
        if excess!=0 :
            nx = nx - excess
            if len(self.image.shape)==2 :
                self.image = self.image[:,:nx]
            else :
                self.image = self.image[:,:nx,:]
        if self.ny!=ny or self.nx!=nx :
            self.ny = ny
            self.nx = nx     
        self.setGeometry(QRect(self.xoffset, self.yoffset,self.nx,self.ny))
        self.Format = Format
        self.colorTable = colorTable
        self.update()
        if self.isHidden :
            self.isHidden = False
            self.show()
        QApplication.processEvents()
        
    def closeEvent(self,event) :
        if not self.okToClose :
            point = self.geometry().topLeft()
            self.xoffset = point.x()
            self.yoffset = point.y()
            self.hide()
            self.isHidden = True
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


    def paintEvent(self, ev):
        if self.mousePressed : return
        self.thread.render(self,self.image,self.Format,self.colorTable)
        self.thread.wait()

