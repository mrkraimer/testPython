# numpyImage.py

from PyQt5.QtWidgets import QWidget,QRubberBand
from PyQt5.QtWidgets import QLabel,QLineEdit
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPainter,QImage
from PyQt5.QtCore import *

import numpy as np
import math
import time


class NumpyImage(QWidget) :
    '''
___
Normal use is:
...
from numpyImage import NumpyImage
...
   self.imageSize = 600
   self.numpyImage = NumpyImage(imageSize=self.imageSize)
___
numpyImage privides two main services:
1) Converts a numpy array to a QImage and displays the resulting image.
   See method display for details.
2) Provides support for mouse action in the QImage.
   See methods setZoomCallback and resetZoom for details.
___   
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
latest date 2020.07.31
    '''
    def __init__(self,imageSize=800, flipy= False,isSeparateWindow=True):
        """
         Parameters
        ----------
            imageSize : int
                 image width and height
            flipy : True or False
                 should y axis (height) be flipped
            isSeparateWindow : True or False
                 is this a separate window or a widget within client window.  
        """
        super(QWidget, self).__init__()
        self.__imageSize = int(imageSize)
        self.__flipy = flipy
        self.__isSeparateWindow = isSeparateWindow
        self.__imageDict = self.imageDictCreate()
        self.__thread = self.__Worker(self.__imageSize,self.__ImageToQImage())
        self.__imageZoom = None
        self.__rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.__mousePressPosition = QPoint(0,0)
        self.__mouseReleasePosition = QPoint(0,0)
        self.__clientZoomCallback = None
        self.__clientMousePressCallback = None
        self.__clientMouseReleaseCallback = None
        self.__clientMouseClickCallback = None
        self.__clientResizeCallback = None
        self.__mousePressed = False
        self.__okToClose = False
        self.__isHidden = True
        self.__image = None
        self.__xoffset = 10
        self.__yoffset = 300
        self.__firstDisplay = True
        self.__bytesPerLine = None
        self.__Format = None
        self.__colorTable = None
        self.__expand = 1

    def imageDictCreate(self) :
        """
        Returns
        -------
        imageDict : dict
            imageDict["image"]        None
            imageDict["width"]        0
            imageDict["height"]       0
            imageDict["dtype"]        np.uint8
            imageDict["mouseX"]       0
            imageDict["mouseY"]       0
            imageDict["expand"]       1
        """
        return {"image" : None ,\
             "width" : 0 ,
             "height" : 0 ,
             "dtype" : "uint8"  ,
              "mouseX" : 0 ,
              "mouseY" : 0 ,
               "expand" : 1 }

    def setOkToClose(self) :
        """ allow image window to be closed"""
        self.__okToClose = True
               
    def setZoomCallback(self,clientCallback,clientZoom=False) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client mouse zoom allowed
            clientZoom : True of False
                 should client handle mouse zoom?
                 if False numpyImage handles mouse zoom
        """
        self.__clientZoomCallback = clientCallback
        if not clientZoom :
            self.__imageZoom  = self.__NumpyImageZoom(self.__imageSize)
            
    def setMousePressCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client called when mouse is pressed within image
        """
        self.__clientMousePressCallback = clientCallback
            
    def setMouseReleaseCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client called when mouse is released
        """
        self.__clientMouseReleaseCallback = clientCallback

    def setMouseClickCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client called when mouse is released
        """
        self.__clientMouseClickCallback = clientCallback

    def setResizeCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client is called when a resetZoom is issued.
        """
        self.__clientResizeCallback = clientCallback
        
    def resetZoom(self) :
        """ reset to unzoomed image"""
        self.__imageZoom.reset()
        
    def zoomIn(self,zoomScale):
        """
        Parameters
        ----------
            zoomScale : int
                 zoom in by zoomScale/255
        """
        if self.__imageZoom==None : return False
        result =  self.__imageZoom.zoomIn(zoomScale)
        if result and self.__clientZoomCallback!=None :
            self.__clientZoomCallback(self.__imageZoom.getData())
        return result

    def zoomOut(self,zoomScale):
        """
        Parameters
        ----------
            zoomScale : int
                 zoom out by zoomScale/255
        """
        if self.__imageZoom==None : return False
        result =  self.__imageZoom.zoomOut(zoomScale)
        if result and self.__clientZoomCallback!=None :
            self.__clientZoomCallback(self.__imageZoom.getData())
        return result     

    def setImageSize(self,imageSize) :
        """
        Parameters
        ----------
            imageSize : int
                 set image width and height
        """
        self.__imageSize = imageSize
        self.__thread.setImageSize(self.__imageSize)
        if self.__imageZoom!=None :
            self.__imageZoom.setImageSize(self.__imageSize)
        point = self.geometry().topLeft()
        self.__xoffset = point.x()
        self.__yoffset = point.y()
        self.setGeometry(QRect(self.__xoffset, self.__yoffset,self.__imageSize,self.__imageSize))

    def display(self,pixarray,bytesPerLine=None,Format=0,colorTable=None) :
        """
        Parameters
        ----------
            pixarray : numpy array
                 pixarray that is converted to QImage and displayed.
            bytesPerLine : int
                 If specified must be total bytes in second dimension of image
            Format: int
                 If this is >0 the QImage is created as follows:
                     if bytesPerLine==None :
                        qimage = QImage(data,image.shape[1], image.shape[0],Format)
                     else :
                         qimage = QImage(data,image.shape[1], image.shape[0],bytesPerLine,Format)
                     if colorTable!=None :
                         qimage.setColorTable(colorTable)
                     return qimage
                Otherwise the QImage is created as follows:
                     if pixarray has dtype uint8:
                          if 2d array :
                              if colorTable==None :
                                  create a QImage with format QImage.Format_Grayscale8
                              else :
                                  create a QImage with format QImage.Format_Indexed8
                          elif 3d array (ny,nx,nz) and nz is 3 or 4:
                              if nz==3 :
                                  create a QImage with format QImage.Format_RGB888
                              else :
                                  create a QImage with format QImage.Format_RGBA8888
                          else :
                              an exception is raised
                     elif pixarray has dtype uint16:
                         if 2d array :
                             create a QImage with format QImage.Format_Grayscale16
                         else :
                             an exception is raised
                else:
                    an exception is raised
                      
            colorTable: qRgb color table
                 Default is to let numpyImage decide     
        """
        if self.__firstDisplay :
            self.__firstDisplay = False
            self.setGeometry(QRect(self.__xoffset, self.__yoffset,self.__imageSize,self.__imageSize))
            if not self.__isSeparateWindow :
                 self.setFixedSize(self.__imageSize,self.__imageSize)
        if self.__flipy :
            self.__image = np.flip(pixarray,0)
        else :
            self.__image = pixarray
        
        if self.__imageZoom!=None :
            if self.__imageZoom.isZoom:
                if len(self.__image.shape)==2 and self.__image.dtype==np.uint16 :
                    image = np.array(self.__image,copy=True)
                    image = image/255
                    self.__image = image.astype(np.uint8)
                self.__image = self.__imageZoom.createZoomImage(self.__image)
                
            else :
               self.__imageZoom.setFullSize(self.__image.shape[1],self.__image.shape[0])
        else:
            pass

        self.__bytesPerLine = bytesPerLine
        self.__Format = Format
        self.__colorTable = colorTable
        self.update()
        if self.__isHidden :
            self.__isHidden = False
            self.show()

    def closeEvent(self,event) :
        """
        This is a QWidget method.
        It is only present to override until it is okToClose
        """
        if not self.__okToClose :
            point = self.geometry().topLeft()
            self.__xoffset = point.x()
            self.__yoffset = point.y()
            self.hide()
            self.__isHidden = True
            self.__firstDisplay = True
            return

    def mousePressEvent(self,event) :
        """
        This is a QWidget method.
        It is one of the methods for implemention zoom
        """
        if self.__clientMousePressCallback!=None :
            self.__clientMousePressCallback(event)
        if self.__clientZoomCallback==None : return
        self.__mousePressed = True
        self.__mousePressPosition = QPoint(event.pos())
        self.__rubberBand.setGeometry(QRect(self.__mousePressPosition,QSize()))
        self.__rubberBand.show()

    def mouseMoveEvent(self,event) :
        """
        This is a QWidget method.
        It is one of the methods for implemention zoom
        """
        if not self.__mousePressed : return
        self.__rubberBand.setGeometry(QRect(self.__mousePressPosition,event.pos()).normalized())

    def mouseReleaseEvent(self,event) :
        """
        This is a QWidget method.
        It is one of the methods for implemention zoom
        """
        if self.__clientMouseReleaseCallback!=None :
            self.__clientMouseReleaseCallback(event)
        if not self.__mousePressed : return
        self.__mouseReleasePosition = QPoint(event.pos())
        self.__rubberBand.hide()
        self.__mousePressed = False 
        imageGeometry = self.geometry().getRect()
        xsize = imageGeometry[2]
        ysize = imageGeometry[3]
        xmin = self.__mousePressPosition.x()
        xmax = self.__mouseReleasePosition.x()
        if xmin>xmax : xmax,xmin = xmin,xmax
        if xmin<0 : xmin = 0
        if xmax>xsize : xmax = xsize
        ymin = self.__mousePressPosition.y()
        ymax = self.__mouseReleasePosition.y()
        if ymin>ymax : ymax,ymin = ymin,ymax
        if ymin<0 : ymin = 0
        if ymax>ysize : ymax = ysize
        sizey = ymax - ymin
        sizex = xmax -xmin
        if sizey<=3 or sizex<=3 :
            if self.__clientMouseClickCallback!=None :
                self.__imageDict["image"] = self.__image
                self.__imageDict["width"] = xsize
                self.__imageDict["height"] = ysize
                self.__imageDict["mouseX"] = xmin
                self.__imageDict["mouseY"] = ymin
                self.__imageDict["expand"] = self.__expand
                self.__clientMouseClickCallback(event,self.__imageDict)
            return
        if self.__imageZoom==None :
            self.__clientZoomCallback((xsize,ysize),(xmin,xmax,ymin,ymax))
            return
        if self.__imageZoom.newZoom(xsize,ysize,xmin,xmax,ymin,ymax,self.__image.dtype) :
            self.__clientZoomCallback(self.__imageZoom.getData())

    def resizeEvent(self,event) :
        """
        This is a QWidget method.
        It used to set geometry
        """
        if self.__clientResizeCallback!= None :
            time.sleep(.2)
            imageGeometry = self.geometry().getRect()
            xsize = imageGeometry[2]
            ysize = imageGeometry[3]
            self.__clientResizeCallback(event,xsize,ysize)

    def paintEvent(self, ev):
        """
        This is the method that displays the QImage
        """
        if self.__mousePressed : return
        if type(self.__image)==type(None) : return
        self.__thread.render(self,self.__image,self.__bytesPerLine,self.__Format,self.__colorTable)
        self.__thread.wait()

    class __ImageToQImage() :
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
                        if colorTable==None :
                            qimage = QImage(data, image.shape[1], image.shape[0],nx,\
                                QImage.Format_Grayscale8)
                        else :
                            qimage = QImage(data,image.shape[1], image.shape[0],nx,
                                QImage.Format_Indexed8)
                            qimage.setColorTable(colorTable) 
                        return  qimage
                    elif len(image.shape) == 3:
                        if image.shape[2] == 3:
                            nx = image.shape[1]*3
                            qimage = QImage(data, image.shape[1],\
                                image.shape[0],nx,QImage.Format_RGB888)
                            return qimage
                        elif image.shape[2] == 4:
                            nx = image.shape[1]*4
                            qimage = QImage(data, image.shape[1],\
                                image.shape[0],nx, QImage.Format_RGBA8888)
                            return qimage
                    self.error = 'nz must have length 3 or 4'
                    return None
                if image.dtype==np.uint16 :
                    if len(image.shape) == 2:
                        nx = image.shape[1]*2
                        qimage = QImage(data, image.shape[1], \
                            image.shape[0],nx, QImage.Format_Grayscale16)
                        return  qimage
                self.error = 'unsupported dtype=' + str(image.dtype)
                return None
            except Exception as error:
                self.error = str(error)
                return None
    class __Worker(QThread):
        def __init__(self,imageSize,imageToQimage):
            QThread.__init__(self)
            self.error = str('')
            self.imageSize = imageSize
            self.imageToQImage = imageToQimage
            self.bytesPerLine = None

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
            self.setPriority(QThread.HighPriority)
            qimage = self.imageToQImage.toQImage(\
                self.image,\
                bytesPerLine=self.bytesPerLine,\
                Format=self.Format,\
                colorTable=self.colorTable)
            if qimage==None :
                self.error = self.imageToQImage.error
                return
            numx = self.image.shape[1]
            numy = self.image.shape[0]
            if numx!=self.imageSize or numx!=self.imageSize :
                if numy>numx :
                    qimage = qimage.scaledToHeight(self.imageSize)
                else :
                    qimage = qimage.scaledToWidth(self.imageSize)
            painter = QPainter(self.caller)
            painter.drawImage(0,0,qimage)
            while True :
                if painter.end() : break
            self.image = None

    class __NumpyImageZoom() :
        def __init__(self,imageSize):
            self.imageSize = imageSize
            self.isZoom = False
            self.xmin = 0
            self.xmax = 0
            self.ymin = 0
            self.ymax = 0
            self.nx = 0
            self.ny = 0

        def setImageSize(self,imageSize) :
            self.imageSize = imageSize
             
        def setFullSize(self,nx,ny) :
            self.xmax = nx
            self.ymax = ny
            self.nx = nx
            self.ny = ny
        
        
        def reset(self) :
            self.isZoom = False
            self.xmin = 0
            self.xmax = self.imageSize
            self.ymin = 0
            self.ymax = self.imageSize

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
            if xmax>self.nx : return False
            ymin = self.ymin + int(ymin*yscale)
            ymax = int(ymin + dely)
            if ymax>self.ny : return False
            if xmax<=xmin : return False
            if ymax<=ymin : return False
            self.xmin = xmin
            self.xmax = xmax
            self.ymin = ymin
            self.ymax = ymax
            self.isZoom = True
            return True

        def zoomInc(self,inc) :
            self.isZoom = True
            xmin = self.xmin + inc
            if xmin<0 : return False
            xmax = self.xmax - inc
            if xmax>self.nx : return False
            if xmax>self.imageSize : return False
            if (xmax-xmin)<2.0 : return False
            ymin = self.ymin + inc
            if ymin<0 : return False
            ymax = self.ymax - inc
            if ymax>self.ny : return False
            if ymax>self.imageSize : return False
            if (ymax-ymin)<2.0 : return False
            self.xmin = xmin
            self.xmax = xmax
            self.ymin = ymin
            self.ymax = ymax
            return True

        def zoomIn(self,zoomScale) :
            inc = 1*zoomScale
            return self.zoomInc(inc)

        def zoomOut(self,zoomScale) :
            inc = -1*zoomScale
            return self.zoomInc(inc)

        def getData(self) :
            return (self.xmin,self.xmax,self.ymin,self.ymax)
        
        def createZoomImage(self,image) :
            return image[self.ymin:self.ymax,self.xmin:self.xmax]

        
