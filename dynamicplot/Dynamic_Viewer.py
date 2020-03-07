# Dynamic_Viewer.py
import sys,time,signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import numpy as np
from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

import ctypes
import ctypes.util
import os

#from pvaccess import *
from pvaccess import PvObject,DOUBLE,STRING

size = int(600)

class ChannelStructure(object) :
    ''' a class for the data a channel must provide'''

    def __init__(self) :
        self.data = PvObject(\
        {   'name':STRING\
            ,'x':[DOUBLE]\
            ,'y':[DOUBLE]\
            ,'xmin':DOUBLE\
            ,'xmax':DOUBLE\
            ,'ymin':DOUBLE\
            ,'ymax':DOUBLE\
        })

    def set(self,data) :
        self.data = data
    def get(self) : 
        return self.data
    def putName(self,value) :
        self.data['name'] = value
    def getName(self) :
        return self.data['name']
    def putX(self,value) :
        self.data['x'] = value
    def getX(self) :
        return self.data['x']
    def putY(self,value) :
        self.data['y'] = value
    def getY(self) :
        return self.data['y']
    def putXmin(self,value) :
        self.data['xmin'] = value
    def getXmin(self) :
        return self.data['xmin']
    def putXmax(self,value) :
        self.data['xmax'] = value
    def getXmax(self) :
        return self.data['xmax']
    def putYmin(self,value) :
        self.data['ymin'] = value
    def getYmin(self) :
        return self.data['ymin']
    def putYmax(self,value) :
        self.data['ymax'] = value
    def getYmax(self) :
        return self.data['ymax']
    def computeLimits(self) :
        x = self.getX()
        y = self.getY()
        npts = len(x)
        if npts<1 :
            raise Exception('x length < 1')
        if npts!= len(y) :
            raise Exception('x and y do not have same length')
        xmin = x[0]
        xmax = xmin
        ymin = y[0]
        ymax = ymin
        for i in range(npts) :
            if x[i]>xmax : xmax = x[i]
            if x[i]<xmin : xmin = x[i]
            if y[i]>ymax : ymax = y[i]
            if y[i]<ymin : ymin = y[i]
        self.putXmin(xmin)
        self.putXmax(xmax)
        self.putYmin(ymin)
        self.putYmax(ymax)

class Dynamic_Channel_Provider(object) :
    '''
    Base class for monitoring an NTNDArray channel from an areaDetector IOC.
    The methods are called by NTNDA_Viewer.
    '''

    def __init__(self) :
        self.channelName = str('dynamicRecord')
    def getChannelName(self) :
        name = os.getenv('DYNAMIC_VIEWER_CHANNELNAME')
        if name== None : return self.channelName
        return str(name)
    def setChannelName(self,name) :
        self.channelName = str(name)
    def start(self) :
        ''' called to start monitoring.'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.start')
    def stop(self) :
        ''' called to stop monitoring.'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.stop')
    def done(self) :
        ''' called when NTNDA_Viewer is done.'''
        pass
    def callback(self,arg) :
        ''' must call NTNDA_Viewer.callback(arg).'''
        raise Exception('derived class must implement NTNDA_Channel_Provider.callback')
    

class Image_Display(RawImageWidget,QWidget) :
    def __init__(self,parent=None, **kargs):
        RawImageWidget.__init__(self, parent=parent,scaled=False)
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("image")
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.setGeometry(QRect(10, 300,size, size))

    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            return

    def display(self,image,pixelLevels) :
        self.setImage(image,levels=pixelLevels)
        self.update()
        
    def mousePressEvent(self,event) :
        self.mousePressPosition = QPoint(event.pos())
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,QSize()))
        self.rubberBand.show()
        self.mousePressed = True

    def mouseMoveEvent(self,event) :
        if not self.mousePressed : return
        self.rubberBand.setGeometry(QRect(self.mousePressPosition,event.pos()).normalized())

    def mouseReleaseEvent(self,event) :
        if not self.mousePressed : return
        self.mouseReleasePosition = QPoint(event.pos())
        if not self.clientCallback==None : 
            self.clientCallback(self.mousePressPosition,self.mouseReleasePosition)
        self.rubberBand.hide()
        self.mousePressed = False

    def clientReleaseEvent(self,clientCallback) :
        self.clientCallback = clientCallback

          
class Dynamic_Viewer(QWidget) :
    def __init__(self,data_Provider, providerName,parent=None):
        super(QWidget, self).__init__(parent)
        self.isClosed = False
        self.provider = data_Provider
        self.setWindowTitle(providerName +"_Data_Viewer")
        self.imageDisplay = Image_Display()
# first row
        self.startButton = QPushButton('start')
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.startEvent)
        self.startButton.setFixedWidth(40)
        self.isStarted = False
        self.stopButton = QPushButton('stop')
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stopEvent)
        self.stopButton.setFixedWidth(40)
        self.channelNameLabel = QLabel("channelName:")
        self.channelNameText = QLineEdit()
        self.channelNameText.setEnabled(True)
        self.channelNameText.setText(self.provider.getChannelName())
        self.channelNameText.editingFinished.connect(self.channelNameEvent)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(self.startButton)
        box.addWidget(self.stopButton)
        box.addWidget(self.channelNameLabel)
        box.addWidget(self.channelNameText)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
# second row
        self.nptsText = QLabel()
        self.nptsText.setFixedWidth(50)
        self.providerNameText = QLabel()
        self.providerNameText.setFixedWidth(100)
        self.clearButton = QPushButton('clear')
        self.clearButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearEvent)
        self.clearButton.setFixedWidth(40)
        self.statusText = QLineEdit()
        self.statusText.setText('nothing done so far')
        self.statusText.setFixedWidth(200)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        nptsLabel = QLabel("npts:")
        nptsLabel.setFixedWidth(50)
        self.nptsText.setText('0')
        providerNameLabel = QLabel("providerName:")
        providerNameLabel.setFixedWidth(100)
        self.providerNameText.setText('')
        box.addWidget(nptsLabel)
        box.addWidget(self.nptsText)
        box.addWidget(providerNameLabel)
        box.addWidget(self.providerNameText)
        box.addWidget(self.clearButton)
        statusLabel = QLabel("  status:")
        statusLabel.setFixedWidth(50)
        box.addWidget(statusLabel)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0)
        layout.addWidget(self.secondRow,1,0)
        self.setLayout(layout)
        self.setGeometry(QRect(10, 20, 600, 60))
        self.show()

    def closeEvent(self, event) :
        if self.isStarted : self.stop()
        self.isClosed = True
        self.imageDisplay.isClosed = True
        self.imageDisplay.okToClose = True
        self.imageDisplay.close()

    def startEvent(self) :
        self.start()

    def stopEvent(self) :
        self.stop()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")

    def channelNameEvent(self) :
        try:
            self.provider.setChannelName(self.channelNameText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def start(self) :
        self.provider.start()
        self.isStarted = True
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stop(self) :
        self.provider.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.isStarted = False

    def callback(self,arg):
        if self.isClosed : return
        value = arg.get("exception")
        if value!=None :
            self.statusText.setText('provider exception '+ value)
            return
        value = arg.get("status")
        if value!=None :
            if value=="disconnected" :
                self.channelNameLabel.setStyleSheet("background-color:red")
                self.statusText.setText('disconnected')
                return
            elif value=="connected" :
                self.channelNameLabel.setStyleSheet("background-color:green")
                self.statusText.setText('connected')
                return
            else :
                self.statusText.setText("unknown callback error")
                return
        value = ChannelStructure()
        value.set(arg['value'])
        if value==None :
             self.statusText.setText('bad callback')
             return
        x = value.getX()
        y = value.getY()
        if len(x)!=len(y) :
            self.statusText.setText('x and y have different lengths')
            return
        npts = len(x)
        self.nptsText.setText(str(npts))
        self.providerNameText.setText(str(value.getName()))
        pixarray = np.full((size,size),255,dtype="uint8")
        pixelLevels = (int(0),int(128))
        if len(x)==0 :
            self.imageDisplay.show()
            return
        xmin = value.getXmin()
        xmax = value.getXmax()
        ymin = value.getYmin()
        ymax = value.getYmax()
        if (xmax-xmin)>(ymax-ymin) :
            ratio = float(xmax -xmin)
        else :
            ratio = float(ymax -ymin)
        scale = float(size)/ratio
        for i in range(npts) :
            xnow = (x[i]-xmin)*scale
            if xnow<0 : xnow =0
            if xnow>= size : xnow = xnow -1
            ynow = (ymax - y[i])*scale
            if ynow<0 : ynow =0
            if ynow>= size : ynow = ynow -1
            pixarray[int(xnow)][int(ynow)] = 0
        self.imageDisplay.display(pixarray,pixelLevels)
        self.imageDisplay.show()

