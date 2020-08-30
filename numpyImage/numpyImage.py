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
import copy


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
        self.__thread = self.__Worker(self.__imageSize,self.__ImageToQImage())
        self.__imageZoom = False
        self.__rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.__mousePressPosition = QPoint(0,0)
        self.__mouseReleasePosition = QPoint(0,0)
        self.__clientZoomCallback = None
        self.__clientMouseClickCallback = None
        self.__clientExceptionCallback = None
        self.__mousePressed = False
        self.__okToClose = False
        self.__isHidden = True
        self.__xoffsetZoom = 10
        self.__yoffsetZoom = 300
        self.__bytesPerLine = None
        self.__Format = None
        self.__colorTable = None
        self.__imageDict = {\
             'image' : None,
             'nx' : 0,
             'ny' : 0,
             'nz' : 0,
             }
             
        self.__mouseDict = { "mouseX" : 0 ,"mouseY" : 0 }
        self.__zoomList = list()
        self.__zoomDict = self.__createZoomDict()

    def __createZoomDict(self) :
        return {\
             'isZoom' : False,
             'nx' : 0,
             'ny' : 0,
             'xoffset' : 0,
             'yoffset' :0,
           }

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
            self.__imageZoom  = True

    def setMouseClickCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client called when mouse is released
        """
        self.__clientMouseClickCallback = clientCallback

    def setExceptionCallback(self,clientCallback) :
        """
        Parameters
        ----------
            clientCallback : client method
                 client called exceptiion occurs
        """
        self.__clientExceptionCallback = clientCallback

    def resetZoom(self) :
        """ reset to unzoomed image"""
        self.__zoomDict['isZoom'] = False
        self.__zoomDict['nx'] = 0
        self.__zoomDict['ny'] = 0
        self.__zoomDict['xoffset'] = 0
        self.__zoomDict['yoffset'] = 0
        self.__zoomList = list()

    def zoomIn(self,zoomScale):
        """
        Parameters
        ----------
            zoomScale : int
                 zoom in by zoomScale/255
        """
        nximage = self.__imageDict['nx']
        nyimage = self.__imageDict['ny']
        nx =  self.__zoomDict['nx']
        ny =  self.__zoomDict['ny']
        xoffset =  self.__zoomDict['xoffset']
        yoffset =  self.__zoomDict['yoffset']
        
        zoomDict = self.__createZoomDict()
        zoomDict['nx'] = nx
        zoomDict['ny'] = ny
        zoomDict['xoffset'] = xoffset
        zoomDict['yoffset'] = yoffset

        ratio = nx/nximage
        xoffset = xoffset + ratio*zoomScale
        nx = nx - (2.0*zoomScale)
        ratio = ny/nyimage
        yoffset = yoffset + ratio*zoomScale
        ny = ny -(2.0*zoomScale)
        if nx<10 or ny<10 :
            if self.__clientExceptionCallback!=None :
                self.__clientExceptionCallback('mouseZoom selected to small a subimage')
            return
        
        self.__zoomDict['nx'] = nx
        self.__zoomDict['ny'] = ny
        self.__zoomDict['xoffset'] = xoffset
        self.__zoomDict['yoffset'] = yoffset
        self.__zoomDict['isZoom'] = True
        self.__zoomList.append(zoomDict)
        return True

    def zoomBack(self):
        """
        Parameters
        ----------
            zoomScale : int
                 zoom out by zoomScale/255
        """
        num = len(self.__zoomList)
        if num==0 :
            if self.__clientExceptionCallback!=None :
                self.__clientExceptionCallback('zoomBack failed')
                return
            else :
                raise Exception('zoomBack failed') 
        self.__zoomDict = self.__zoomList[num-1]
        self.__zoomDict['isZoom'] = True
        self.__zoomList.pop()
        if num==1 :
            self.resetZoom()

    def setImageSize(self,imageSize) :
        """
        Parameters
        ----------
            imageSize : int
                 set image width and height
        """
        self.__imageSize = imageSize
        self.__thread.setImageSize(self.__imageSize)
        point = self.geometry().topLeft()
        self.__xoffsetZoom = point.x()
        self.__yoffsetZoom = point.y()
        if self.__isSeparateWindow :
            self.hide()
            self.setGeometry(QRect(self.__xoffsetZoom,\
                self.__yoffsetZoom,self.__imageSize,self.__imageSize))
            self.show()    

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
        if type(self.__imageDict['image'])==type(None) :
            if not self.__isSeparateWindow :
                 self.setFixedSize(self.__imageSize,self.__imageSize)
            else :
                 point = self.geometry().topLeft()
                 self.__xoffsetZoom = point.x()
                 self.__yoffsetZoom = point.y()
                 self.setGeometry(QRect(self.__xoffsetZoom,\
                 self.__yoffsetZoom,self.__imageSize,self.__imageSize))      
        if self.__flipy :
            image = np.flip(pixarray,0) 
            self.__imageDict['image'] = np.flip(pixarray,0)
        else :
            image = pixarray 
        nx = image.shape[1]
        ny = image.shape[0]
        nz = 1
        if len(image.shape)==3 :
             nz = image.shape[2]
        if nx!=self.__imageDict['nx'] or ny!=self.__imageDict['ny'] or nz!=self.__imageDict['nz'] :
            self.resetZoom()
            self.__imageDict['nx'] = nx
            self.__imageDict['ny'] = ny
            self.__imageDict['nz'] = nz 
        if self.__zoomDict['isZoom'] :
            nx = self.__zoomDict['nx']
            ny = self.__zoomDict['ny']
            xoffset = int(self.__zoomDict['xoffset'])
            endx = int(xoffset + nx)
            yoffset = int(self.__zoomDict['yoffset'])
            endy = int(yoffset + ny)
            image = image[yoffset:endy,xoffset:endx]
        else :
            self.__zoomDict['nx'] = nx
            self.__zoomDict['ny'] = ny
        self.__imageDict['image'] = image
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
            self.__xoffsetZoom = point.x()
            self.__yoffsetZoom = point.y()
            self.hide()
            self.__isHidden = True
            self.__firstDisplay = True
            return

    def mousePressEvent(self,event) :
        """
        This is a QWidget method.
        It is one of the methods for implemention zoom
        """
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
        if not self.__mousePressed : return
        self.__mousePressed = False
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
                delx = self.__imageDict['nx']/xsize
                dely = self.__imageDict['ny']/ysize
                mouseX = int(xmin*delx)
                mouseY = int(ymin*dely)   
                if self.__zoomDict['isZoom'] : 
                    nximage = self.__imageDict['nx']
                    nyimage = self.__imageDict['ny']
                    nx =  self.__zoomDict['nx']
                    ny =  self.__zoomDict['ny']
                    xoffset =  self.__zoomDict['xoffset']
                    yoffset =  self.__zoomDict['yoffset']
                    ratio = nx/nximage            
                    mouseX = mouseX*ratio + xoffset
                    ratio = ny/nyimage
                    mouseY = mouseY*ratio + yoffset
                self.__mouseDict['mouseX'] = mouseX
                self.__mouseDict['mouseY'] = mouseY
                self.__clientMouseClickCallback(self.__mouseDict)
            return
        if not self.__imageZoom :
            self.__clientZoomCallback((xsize,ysize),(xmin,xmax,ymin,ymax))
            return
        self.__newZoom(xsize,ysize,xmin,xmax,ymin,ymax)
        self.__clientZoomCallback()
            
    def paintEvent(self, ev):
        """
        This is the method that displays the QImage
        """
        if self.__mousePressed : return
        image = self.__imageDict['image']
        self.__thread.render(self,image,self.__bytesPerLine,self.__Format,self.__colorTable)
        self.__thread.wait()

    def __newZoom(self,xsize,ysize,xminMouse,xmaxMouse,yminMouse,ymaxMouse) :
        nximage = self.__imageDict['nx']
        nyimage = self.__imageDict['ny']
        nx =  self.__zoomDict['nx']
        ny =  self.__zoomDict['ny']
        xoffset =  self.__zoomDict['xoffset']
        yoffset =  self.__zoomDict['yoffset']
        
        zoomDict = self.__createZoomDict()
        zoomDict['nx'] = nx
        zoomDict['ny'] = ny
        zoomDict['xoffset'] = xoffset
        zoomDict['yoffset'] = yoffset

        ratiox = nx/nximage
        mouseRatiox = (xmaxMouse - xminMouse)/xsize
        ratioy = ny/nyimage
        mouseRatioy = (ymaxMouse - yminMouse)/ysize
        mouseRatio = mouseRatiox
        if mouseRatioy>mouseRatiox : mouseRatio = mouseRatioy
        nx = nximage*ratiox*mouseRatio
        offsetmouse = nximage*(xminMouse/xsize)*ratiox
        xoffset = xoffset+offsetmouse
        ny = nyimage*ratioy*mouseRatio
        if nx<10 or ny<10 :
            if self.__clientExceptionCallback!=None :
                self.__clientExceptionCallback('mouseZoom selected to small a subimage')
            return
        yoffset = yoffset+offsetmouse

        self.__zoomDict['nx'] = nx
        self.__zoomDict['ny'] = ny
        self.__zoomDict['xoffset'] = xoffset
        self.__zoomDict['yoffset'] = yoffset
        self.__zoomDict['isZoom'] = True
        self.__zoomList.append(zoomDict)

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

