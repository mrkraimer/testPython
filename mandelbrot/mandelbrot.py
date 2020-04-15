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
    yxratio = (ymax-ymin)/(xmax-xmin)
    if yxratio>1.0 :
        height = int(maxsize)
        width = math.ceil(height*yxratio)
    else :
        width = int(maxsize)
        height = math.ceil(width*yxratio)
    print('yxratio=',yxratio,' height=',height, ' width=',width)
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
        print('self.xmin=',self.xmin,' self.xmax=',self.xmax,' self.ymin=',self.ymin,' self.ymax=',self.ymax)
        print('self.height=',self.height,' self.width=',self.width,' self.xinc=',self.xinc,' self.yinc=',self.yinc)

    def update(self,pxmin,pxmax,pymin,pymax) :
        print('update pxmin=',pxmin,' pxmax=',pxmax,' pymin=',pymin,' pymax=',pymax)
        self.show()
        nx = pxmax - pxmin
        ny = pymax - pymin
        print('nx=',nx,' ny=',ny)
        yxratio = float(ny)/float(nx)
        if yxratio>1.0 :
            height = int(maxsize)
            width = math.ceil(height/yxratio)
        else :
            width = int(maxsize)
            height = math.ceil(width*yxratio)
        print('yxratio=',yxratio,' height=',height, ' width=',width)
        xmin = self.xmin + self.xinc*pxmin
#       for pixel direction is top to bottom
        ymin = self.ymax - self.yinc*pymax
        print('xmin=',xmin,' ymin=',ymin)
        xinc = self.xinc*(nx/float(width))
        yinc = self.yinc*(ny/float(height))
        print('xinc=',xinc,' yinc=',yinc)
        xmax = xmin + xinc*float(nx)
        ymax = ymin + yinc*float(ny)
        print('xmax=',xmax,' ymax=',ymax)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.height = height
        self.width = width
        self.xinc = xinc
        self.yinc = yinc
        self.show()


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


class Mandelbrot() :
    def __init__(self,currentValues,parent=None):
        self.pixeltype = currentValues.pixeltype
        self.pixelmax = currentValues.pixelmax
        self.xmin = currentValues.xmin
        self.xmax = currentValues.xmax
        self.ymin = currentValues.ymin
        self.ymax = currentValues.ymax
        self.height = currentValues.height
        self.width = currentValues.width
        self.xinc = currentValues.xinc
        self.yinc = currentValues.yinc
        self.pixarray = np.full((self.width,self.height,3),self.pixelmax,dtype=self.pixeltype)
        
    def calcIntensity(self,x,y) :
        c = complex(x,y)
        z = complex(0.0,0.0)
        i = 0
        while abs(z) < 2 and i < self.pixelmax:
            z = z**2 + c
            i += 1
        # Color scheme is that of Julia sets
        color = (i % 8 * 32, i % 16 * 16, i % 32 * 8)
        return color

    def calcRow(self,pixy,y):
        for i in range(self.width) :
            pixx = i
            x = self.xmin + i*self.xinc
            color = self.calcIntensity(x,y)
            self.pixarray[pixx][pixy][0] = color[0]
            self.pixarray[pixx][pixy][1] = color[1]
            self.pixarray[pixx][pixy][2] = color[2]

    def calc(self):
        for i in range(self.height) :
            pixy = i
            y = self.ymin + i*self.yinc
            self.calcRow(pixy,y)
        return self.pixarray

        
class Viewer(QWidget) :
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
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
        self.mandelbrot = Mandelbrot(self.currentValues)
        self.timeText.setText("0")
        self.repaint()
        begin = time.time()
        self.statusText.setText('calculating image')
        self.repaint()
        self.pixarray = self.mandelbrot.calc()
        self.statusText.setText('generating image')
        self.repaint()
        if self.imageDisplay!= None :
            self.imageDisplay.close()
        self.imageDisplay = ImageDisplay(self.currentValues.width,self.currentValues.height)
        self.imageDisplay.clientReleaseEvent(self.clientReleaseEvent)
        self.imageDisplay.display(self.pixarray)
        self.imageDisplay.show()
        end = time.time()
        timediff = str(round(end-begin))
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
        print('clientReleaseEvent')
        xmin = pressPosition.x()
        ymin = pressPosition.y()
        xmax = releasePosition.x()
        ymax = releasePosition.y()
        if xmin==xmax and ymin>=ymax : return
        if xmin>=xmax or ymin>=ymax :
            self.statusText.setText('illegal mouse move')
            return 
        print('calling update xmin=',xmin,' xmax=',xmax,' ymin=',ymin,' ymax=',ymax)
        self.currentValues.update(xmin,xmax,ymin,ymax) 
        self.generateImage()

if __name__ == '__main__':
    app = QApplication(list())
    viewer = Viewer()
    sys.exit(app.exec_())
