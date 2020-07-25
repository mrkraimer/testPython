# DisplayImage.py
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QVBoxLayout,QGridLayout,QGroupBox
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject,QPoint,QRect,QSize

import sys,time
import numpy as np
import math
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage

class CurrentValues() :
    def __init__(self):
        self.pixeltype = pixeltype = "uint8"
        self.pixelmax = 256
        self.xmin = float(-2.5)
        self.xmax = float(1.5)
        self.ymin = float(-2.0)
        self.ymax = float(2.0)
        self.nz = 3
    def show(self) :
        print('self.xmin=',self.xmin,' self.xmax=',self.xmax)
        print('self.ymin=',self.ymin,' self.ymax=',self.ymax)
        print('self.nz=',self.nz)

        
class Viewer(QWidget) :
    def __init__(self,mandelbrot,parent=None):
        super(QWidget, self).__init__(parent)
        self.mandelbrot = mandelbrot
        self.imageSize = 600
        self.isClosed = False
        self.setWindowTitle("Viewer")
        self.currentValues = CurrentValues()
        self.imageDisplay = NumpyImage(windowTitle='mandelbrot',flipy=False,imageSize=self.imageSize)
        self.imageDisplay.setZoomCallback(self.zoomEvent,clientZoom=True)
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
        self.zoomButton.clicked.connect(self.zoomStartEvent)
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
        self.mandelbrot.addClientConnectionCallback(self)

    def connectionCallback(self,arg) :
        if arg==True :
            self.startButton.setStyleSheet("background-color:green")
        else :
            self.startButton.setStyleSheet("background-color:red")

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")
            
    def stopZoomEvent(self) :
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

    def zoomStartEvent(self) :
        self.stopZoom = False
        self.zoomActive = True
        xmin = self.currentValues.xmin
        xmax = self.currentValues.xmax
        ymin = self.currentValues.ymin
        ymax = self.currentValues.ymax
        rangex = (xmax-xmin)
        rangey = (ymax-ymin)
        nimages = self.nimages
        ratio = self.ratio
        rate = self.rate
        finalrangex = rangex*ratio
        delX = ((rangex-finalrangex)/float(nimages))/2.0
        finalrangey = rangey*ratio
        delY = ((rangey-finalrangey)/float(nimages))/2.0
        delayPerImage = 1.0/float(rate)
        for i in range(nimages) :
            if self.stopZoom : break
            xmin = xmin + delX
            xmax = xmax - delX
            ymin = ymin + delY
            ymax = ymax - delY
            self.currentValues.xmin = xmin
            self.currentValues.xmax = xmax
            self.currentValues.ymin = ymin
            self.currentValues.ymax = ymax
            begin = time.time()
            self.generateImage()
            end = time.time()
            timediff = end-begin
            delay = delayPerImage - timediff
            if delay>0.0 : time.sleep(delay)
        self.zoomActive = False

    def update(self,imageSize,mouseLocation) :
        xminPre = self.currentValues.xmin
        xmaxPre = self.currentValues.xmax
        xincPre = (xmaxPre-xminPre)/self.imageSize
        yminPre = self.currentValues.ymin
        ymaxPre = self.currentValues.ymax
        yincPre = (ymaxPre-yminPre)/self.imageSize
        xlow = mouseLocation[0]
        xhigh = mouseLocation[1]
        ylow = mouseLocation[2]
        yhigh = mouseLocation[3]
        nx = xhigh - xlow
        ny = yhigh - ylow
        npts = max(nx,ny)
        self.currentValues.xmin = xminPre + xincPre*xlow
        self.currentValues.xmax = self.currentValues.xmin+ xincPre*npts
        self.currentValues.ymin = yminPre + yincPre*ylow
        self.currentValues.ymax = self.currentValues.ymin + yincPre*npts

    def generateImage(self) :
        isConnected = self.mandelbrot.checkConnected()
        if isConnected :
            self.statusText.setText('generating image')
        else :
            self.statusText.setText('generating image even though not connected')
        QApplication.processEvents()
        arg = (self.currentValues.xmin,self.currentValues.xmax,\
              self.currentValues.ymin,self.currentValues.ymax,\
              self.imageSize,\
              self.currentValues.nz)
        try :
            self.pixarray = self.mandelbrot.createImage(arg)
        except Exception as error:
            self.statusText.setText(str(error))
            return
        self.imageDisplay.display(self.pixarray)
        self.updateXYtext()
        QApplication.processEvents()
        
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

    def zoomEvent(self,imageSize,mouseLocation) :
        if self.zoomActive: return
        success = True
        try :
            self.update(imageSize,mouseLocation)
        except Exception as error:
            print('catching exception=',error)
            success = False
            self.statusText.setText(str(error))
        if success :
            self.start()


