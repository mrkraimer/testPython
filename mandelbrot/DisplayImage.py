from pyqtgraph.widgets.RawImageWidget import RawImageWidget
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QVBoxLayout,QGridLayout,QGroupBox
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
#from PyQt5.QtCore import *
from PyQt5.QtCore import QObject,QPoint,QRect,QSize

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
    nz = 3

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
        self.nz = ini.nz
    def show(self) :
        print('self.xmin=',self.xmin,' self.xmax=',self.xmax)
        print('self.ymin=',self.ymin,' self.ymax=',self.ymax)
        print('self.height=',self.height,' self.width=',self.width)
        print('self.xinc=',self.xinc,' self.yinc=',self.yinc)
        print('self.nz=',self.nz)

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
        xmax = xmin + self.xinc*float(pixnx)
        ymax = ymin + self.yinc*float(pixny)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.height = height
        self.width = width
        self.xinc = xinc
        self.yinc = yinc


class ImageDisplay(RawImageWidget,QWidget) :
    def __init__(self,parent=None, **kargs):
        RawImageWidget.__init__(self, parent=parent,scaled=False)
        super(QWidget, self).__init__(parent)
        self.setWindowTitle("image")
        self.width = 0
        self.height = 0
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.mousePressPosition = QPoint(0,0)
        self.mouseReleasePosition = QPoint(0,0)
        self.clientCallback = None
        self.mousePressed = False
        self.okToClose = False
        self.isHidden = True

    def closeEvent(self,event) :
        if not self.okToClose :
            self.hide()
            self.isHidden = True
            return

    def display(self,pixarray,width,height) :
        if self.width!=width or self.height!=height :
            self.width = width
            self.height = height
            self.setGeometry(QRect(10, 300,self.width,self.height))
        self.setImage(np.flip(pixarray,1))
        if self.isHidden :
            self.isHidden = False
            self.show()
        QApplication.processEvents()

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
        self.imageDisplay = ImageDisplay()
        self.imageDisplay.clientReleaseEvent(self.clientReleaseEvent)
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
        timeLabel.setFixedWidth(40)
        self.timeText = QLabel()
        self.timeText.setText('0')
        self.timeText.setFixedWidth(40)
        self.colorModeButton = QPushButton('color')
        self.colorModeButton.setEnabled(True)
        self.colorModeButton.clicked.connect(self.colorModeEvent)
        self.colorModeButton.setFixedWidth(40)
        self.zoomButton = QPushButton('zoom')
        self.zoomButton.setEnabled(True)
        self.zoomButton.clicked.connect(self.zoomEvent)
        self.zoomButton.setFixedWidth(40)
        self.zoomActive = False
        self.stopZoomButton = QPushButton('stopZoom')
        self.stopZoomButton.setEnabled(True)
        self.stopZoomButton.clicked.connect(self.stopZoomEvent)
        self.stopZoomButton.setFixedWidth(80)
        self.stopZoom = False
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
        box.addWidget(self.colorModeButton)
        box.addWidget(self.zoomButton)
        box.addWidget(self.stopZoomButton)
        box.addWidget(self.clearButton)
        statusLabel = QLabel("  status:")
        statusLabel.setFixedWidth(50)
        box.addWidget(statusLabel)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
# second row
        self.nimages = 100
        nimagesLabel = QLabel("nimages")
        self.nimagesText = QLineEdit()
        self.nimagesText.setEnabled(True)
        self.nimagesText.setText(str(self.nimages))
        self.nimagesText.setFixedWidth(40)
        self.nimagesText.editingFinished.connect(self.nimagesEvent)
        nimagesGroupBox = QGroupBox()
        nimagesGroupBox.setFixedWidth(80)
        nimageslayout = QVBoxLayout()
        nimageslayout.addWidget(nimagesLabel)
        nimageslayout.addWidget(self.nimagesText)
        nimagesGroupBox.setLayout(nimageslayout)

        self.ratio = .2
        ratioLabel = QLabel("ratio:")
        self.ratioText = QLineEdit()
        self.ratioText.setEnabled(True)
        self.ratioText.setText(str(self.ratio))
        self.ratioText.setFixedWidth(40)
        self.ratioText.editingFinished.connect(self.ratioEvent)
        ratioGroupBox = QGroupBox()
        ratioGroupBox.setFixedWidth(60)
        ratiolayout = QVBoxLayout()
        ratiolayout.addWidget(ratioLabel)
        ratiolayout.addWidget(self.ratioText)
        ratioGroupBox.setLayout(ratiolayout)

        self.rate = 60
        rateLabel = QLabel("rate:")
        self.rateText = QLineEdit()
        self.rateText.setEnabled(True)
        self.rateText.setText(str(self.rate))
        self.rateText.setFixedWidth(60)
        self.rateText.editingFinished.connect(self.rateEvent)
        rateGroupBox = QGroupBox()
        rateGroupBox.setFixedWidth(60)
        ratelayout = QVBoxLayout()
        ratelayout.addWidget(rateLabel)
        ratelayout.addWidget(self.rateText)
        rateGroupBox.setLayout(ratelayout)

        xminLabel = QLabel('xmin')
        self.xminText = QLabel(format(self.currentValues.xmin,'10.4e'))
        self.xminText.setFixedWidth(100)
        xminGroupBox = QGroupBox()
        xminGroupBox.setFixedWidth(120)
        xminlayout = QVBoxLayout()
        xminlayout.addWidget(xminLabel)
        xminlayout.addWidget(self.xminText)
        xminGroupBox.setLayout(xminlayout)
        

        xmaxLabel = QLabel('xmax')
        self.xmaxText = QLabel(format(self.currentValues.xmax,'10.4e'))
        self.xmaxText.setFixedWidth(100)
        xmaxGroupBox = QGroupBox()
        xmaxGroupBox.setFixedWidth(120)
        xmaxlayout = QVBoxLayout()
        xmaxlayout.addWidget(xmaxLabel)
        xmaxlayout.addWidget(self.xmaxText)
        xmaxGroupBox.setLayout(xmaxlayout)

        yminLabel = QLabel('ymin')
        self.yminText = QLabel(format(self.currentValues.ymin,'10.4e'))
        self.yminText.setFixedWidth(100)
        yminGroupBox = QGroupBox()
        yminGroupBox.setFixedWidth(120)
        yminlayout = QVBoxLayout()
        yminlayout.addWidget(yminLabel)
        yminlayout.addWidget(self.yminText)
        yminGroupBox.setLayout(yminlayout)

        ymaxLabel = QLabel('ymax')
        self.ymaxText = QLabel(format(self.currentValues.ymax,'10.4e'))
        self.ymaxText.setFixedWidth(100)
        ymaxGroupBox = QGroupBox()
        ymaxGroupBox.setFixedWidth(120)
        ymaxlayout = QVBoxLayout()
        ymaxlayout.addWidget(ymaxLabel)
        ymaxlayout.addWidget(self.ymaxText)
        ymaxGroupBox.setLayout(ymaxlayout)

        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(nimagesGroupBox)
        box.addWidget(ratioGroupBox)
        box.addWidget(rateGroupBox)
        box.addWidget(xminGroupBox)
        box.addWidget(xmaxGroupBox)
        box.addWidget(yminGroupBox)
        box.addWidget(ymaxGroupBox)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid

# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0)
        layout.addWidget(self.secondRow,1,0)
        self.setLayout(layout)
        self.setGeometry(QRect(10, 20, 800, 100))
        self.show()
            
    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")
            
    def stopZoomEvent(self) :
        print('stopZoomEvent')
        self.stopZoom = True


    def nimagesEvent(self) :
        try:
            self.nimages = int(self.nimagesText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def ratioEvent(self) :
        try:
            self.ratio = float(self.ratioText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def rateEvent(self) :
        try:
            self.rate = int(self.rateText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def closeEvent(self, event) :
        self.imageDisplay.okToClose = True
        self.imageDisplay.close()

    def startEvent(self) :
        self.start()

    def resetEvent(self) :
        self.reset()

    def colorModeEvent(self) :
        if self.currentValues.nz==3 :
            self.colorModeButton.setText('mono')
            self.currentValues.nz = 1;
        else :
            self.colorModeButton.setText('color')
            self.currentValues.nz = 3;

    def zoomEvent(self) :
        self.stopZoom = False
        self.zoomActive = True
        startxmin = self.currentValues.xmin
        startxmax = self.currentValues.xmax
        startxinc = self.currentValues.xinc
        startymin = self.currentValues.ymin
        startymax = self.currentValues.ymax
        startyinc = self.currentValues.yinc
        width = self.currentValues.width
        height = self.currentValues.height
        xmin = startxmin
        xmax = startxmax
        xinc = startxinc
        ymin = startymin
        ymax = startymax
        yinc = startyinc
        rangex = (xmax-xmin)
        rangey = (ymax-ymin)
        nimages = self.nimages
        ratio = self.ratio
        rate = self.rate
        print('nimages=',nimages,' ratio=',ratio,' rate=',rate)
        finalrangex = rangex*ratio
        delX = ((rangex-finalrangex)/float(nimages))/2.0
        finalrangey = rangey*ratio
        delY = ((rangey-finalrangey)/float(nimages))/2.0
        delayPerImage = 1.0/float(rate)
        for i in range(nimages) :
            if self.stopZoom : break
            xmin = xmin + delX
            xmax = xmax - delX
            xinc = (xmax-xmin)/float(width)
            ymin = ymin + delY
            ymax = ymax - delY
            yinc = (ymax-ymin)/float(height)
            self.currentValues.xmin = xmin
            self.currentValues.xmax = xmax
            self.currentValues.xinc = xinc
            self.currentValues.ymin = ymin
            self.currentValues.ymax = ymax
            self.currentValues.yinc = yinc
            begin = time.time()
            self.generateImage()
            end = time.time()
            timediff = end-begin
            delay = delayPerImage - timediff
            if delay>0.0 : time.sleep(delay)
        self.currentValues.xmin = startxmin
        self.currentValues.xmax = startxmax
        self.currentValues.xinc = startxinc
        self.currentValues.ymin = startymin
        self.currentValues.ymax = startymax
        self.currentValues.yinc = startyinc
        self.zoomActive = False


    def generateImage(self) :
        isConnected = self.mandelbrot.checkConnected()
        if isConnected :
            self.startButton.setStyleSheet("background-color:green")
            self.statusText.setText('calculating image')
        else :
            self.startButton.setStyleSheet("background-color:red")
            self.statusText.setText('calculating image even though not connected')
        self.repaint()
        arg = (self.currentValues.xmin,self.currentValues.xinc,\
              self.currentValues.ymin,self.currentValues.yinc,\
              self.currentValues.width,self.currentValues.height,\
              self.currentValues.nz)
        self.pixarray = self.mandelbrot.createImage(arg)
        self.statusText.setText('generating image')
        self.repaint()
        self.imageDisplay.display(self.pixarray,self.currentValues.width,self.currentValues.height)
        self.statusText.setText('image generated')
        self.repaint()
        
    def start(self) :
        self.timeText.setText("0")
        self.startButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        begin = time.time()
        self.generateImage()
        end = time.time()
        timediff = str(round(end-begin,2))
        self.timeText.setText(timediff)
        self.startButton.setEnabled(True)
        self.resetButton.setEnabled(True)

    def updateXYtext(self) :
        self.xminText.setText(format(self.currentValues.xmin,'10.4e'))
        self.xmaxText.setText(format(self.currentValues.xmax,'10.4e'))
        self.yminText.setText(format(self.currentValues.ymin,'10.4e'))
        self.ymaxText.setText(format(self.currentValues.ymax,'10.4e'))

    def reset(self) :
        self.currentValues = CurrentValues()
        self.start()
        self.updateXYtext()

    def clientReleaseEvent(self,pressPosition,releasePosition) :
        if self.zoomActive: return
        xmin = pressPosition.x()
        ymin = pressPosition.y()
        xmax = releasePosition.x()
        ymax = releasePosition.y()
        if xmin==xmax and ymin>=ymax : return
        if xmin>=xmax or ymin>=ymax :
            self.statusText.setText('illegal mouse move')
            return
        self.currentValues.update(xmin,xmax,ymin,ymax) 
        self.start()
        self.updateXYtext()


