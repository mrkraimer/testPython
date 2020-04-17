from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
import sys,time
import numpy as np
import math

maxsize = 600

class InitialValues() :
    pixeltype = "uint8"
    pixelmax = 256
    xmin = float(-2.5)
    xmax = float(1.0)
    ymin = float(-1.0)
#    ymin = float(-.1)
    ymax = float(1.0)
    # convert from x,y to pixel (width,height)
    yxratio = (ymax-ymin)/(xmax-xmin)
    if yxratio>1.0 :
        height = int(maxsize)
        width = math.ceil(height*yxratio)
    else :
        width = int(maxsize)
        height = math.ceil(width*yxratio)
    xinc = (xmax-xmin)/float(width)
    yinc = (ymax-ymin)/float(height)

class CurrentValues() :
    def __init__(self,parent=None):
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
    def show(self) :
        print('self.xmin=',self.xmin,' self.xmax=',self.xmax)
        print('self.ymin=',self.ymin,' self.ymax=',self.ymax)
        print('self.height=',self.height,' self.width=',self.width)
        print('self.xinc=',self.xinc,' self.yinc=',self.yinc)

    def update(self,pxmin,pxmax,pymin,pymax) :
        # convert from pixel(x,y) to (x,y)
        #  for pixel direction is top to bottom must flip
        temp = pymin
        pymin = self.height - pymax
        pymax = self.height - temp
        pixnx = pxmax - pxmin
        pixny = pymax - pymin
        yxratio = float(pixny)/float(pixnx)
        if yxratio>1.0 :
            height = int(maxsize)
            width = math.ceil(height/yxratio)
        else :
            width = int(maxsize)
            height = math.ceil(width*yxratio)
        xmin = self.xmin + self.xinc*pxmin
        ymin = self.ymin + self.yinc*pymin
        xinc = self.xinc*(pixnx/float(width))
        yinc = self.yinc*(pixny/float(height))
        xmax = xmin + xinc*float(pixnx)
        ymax = ymin + yinc*float(pixny)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.height = height
        self.width = width
        self.xinc = xinc
        self.yinc = yinc

class ImageDisplay(RawImageWidget,QWidget) :
    def __init__(self,width,height,parent=None, **kargs):
        RawImageWidget.__init__(self, parent=parent,scaled=False)
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("image")
        self.width = width
        self.height = height
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientCallback = None
        self.mousePressed = False

    def display(self,pixarray) :
        self.setGeometry(QRect(10, 300,self.width,self.height))
        self.setImage(np.flip(pixarray,1))

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
        
class Viewer(QWidget) :
    def __init__(self,mandelbrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.mandelbrot = mandelbrot
        self.isClosed = False
        self.setWindowTitle("Viewer")
        self.currentValues = CurrentValues()
        self.imageDisplay = None
# first row
        self.startButton = QPushButton('start')
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.startEvent)
        self.startButton.setFixedWidth(40)
        self.resetButton = QPushButton('reset')
        self.resetButton.setEnabled(True)
        self.resetButton.clicked.connect(self.resetEvent)
        self.resetButton.setFixedWidth(40)
        timeLabel = QLabel("time:")
        timeLabel.setFixedWidth(50)
        self.timeText = QLabel()
        self.timeText.setText('0')
        self.timeText.setFixedWidth(50)
        self.nImages = 0
        self.clearButton = QPushButton('clear')
        self.clearButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearEvent)
        self.clearButton.setFixedWidth(40)
        self.statusText = QLineEdit()
        self.statusText.setText('nothing done so far')
        self.statusText.setFixedWidth(500)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(self.startButton)
        box.addWidget(self.resetButton)
        box.addWidget(timeLabel)
        box.addWidget(self.timeText)
        box.addWidget(self.clearButton)
        statusLabel = QLabel("  status:")
        statusLabel.setFixedWidth(50)
        box.addWidget(statusLabel)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0)
        self.setLayout(layout)
        self.setGeometry(QRect(10, 20, 800, 60))
        self.show()

    def startEvent(self) :
        self.start()

    def resetEvent(self) :
        self.reset()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")

    def generateImage(self) :
        self.timeText.setText("0")
        self.repaint()
        begin = time.time()
        self.statusText.setText('calculating image')
        self.repaint()
        arg = (self.currentValues.xmin,self.currentValues.xinc,\
              self.currentValues.ymin,self.currentValues.yinc,\
              self.currentValues.width,self.currentValues.height)
        self.pixarray = self.mandelbrot.createImage(arg)
        self.statusText.setText('generating image')
        self.repaint()
        if self.imageDisplay!= None :
            self.imageDisplay.close()
        self.imageDisplay = ImageDisplay(self.currentValues.width,self.currentValues.height)
        self.imageDisplay.clientReleaseEvent(self.clientReleaseEvent)
        self.imageDisplay.display(self.pixarray)
        self.imageDisplay.show()
        end = time.time()
        timediff = str(round(end-begin,1))
        self.timeText.setText(timediff)
        self.statusText.setText('image generated')
        self.repaint()
        
    def start(self) :
        self.startButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.generateImage()
       
        self.startButton.setEnabled(True)
        self.resetButton.setEnabled(True)

    def reset(self) :
        self.currentValues = CurrentValues()

    def clientReleaseEvent(self,pressPosition,releasePosition) :
        xmin = pressPosition.x()
        ymin = pressPosition.y()
        xmax = releasePosition.x()
        ymax = releasePosition.y()
        if xmin==xmax and ymin>=ymax : return
        if xmin>=xmax or ymin>=ymax :
            self.statusText.setText('illegal mouse move')
            return
        self.currentValues.update(xmin,xmax,ymin,ymax) 
        self.generateImage()
