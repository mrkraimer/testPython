# Dynamic_Viewer.py
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

import sys,time
import numpy as np
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage


size = int(600)
  
class Dynamic_Viewer(QWidget) :
    def __init__(self,data_Provider, providerName,parent=None):
        super(QWidget, self).__init__(parent)
        self.isClosed = False
        self.provider = data_Provider
        self.setWindowTitle(providerName +"_Data_Viewer")
        self.imageDisplay = NumpyImage(flipy= True)
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
        nptsLabel = QLabel("npts:")
        nptsLabel.setFixedWidth(50)
        self.nptsText = QLabel()
        self.nptsText.setText('0')
        self.nptsText.setFixedWidth(50)
        imageNameLabel = QLabel("imageName:")
        imageNameLabel.setFixedWidth(100)
        self.imageNameText = QLabel()
        self.imageNameText.setText('')
        self.imageNameText.setFixedWidth(80)
        self.nImages = 0
        imageRateLabel = QLabel("imageRate:")
        self.imageRateText = QLabel()
        self.imageRateText.setFixedWidth(40)
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
        box.addWidget(self.stopButton)
        box.addWidget(nptsLabel)
        box.addWidget(self.nptsText)
        box.addWidget(imageNameLabel)
        box.addWidget(self.imageNameText)
        box.addWidget(imageRateLabel)
        box.addWidget(self.imageRateText)
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
        self.lasttime = time.time() -2
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
                self.startButton.setStyleSheet("background-color:red")
                self.statusText.setText('disconnected')
                return
            elif value=="connected" :
                self.startButton.setStyleSheet("background-color:green")
                self.statusText.setText('connected')
                return
            else :
                self.statusText.setText("unknown callback error")
                return
        value = arg.get("value")
        if value==None :
             self.statusText.setText('bad callback')
             return
        x = value.x
        y = value.y
        if len(x)!=len(y) :
            self.statusText.setText('x and y have different lengths')
            return
        npts = len(x)
        if npts==0 : return
        self.nptsText.setText(str(npts))
        self.imageNameText.setText(str(value.name))
        QApplication.processEvents()
        pixarray = np.full((size,size),255,dtype="uint8")
        xmin = value.xmin
        xmax = value.xmax
        ymin = value.ymin
        ymax = value.ymax
        if (xmax-xmin)>(ymax-ymin) :
            ratio = float(xmax -xmin)
        else :
            ratio = float(ymax -ymin)
        scale = float(size)/ratio
        for i in range(npts) :
            xnow = (x[i]-xmin)*scale
            if xnow<0 : xnow =0
            if xnow>= size : xnow = xnow -1
            ynow = (y[i]-ymin)*scale
            if ynow<0 : ynow =0
            if ynow>= size : ynow = ynow -1
            pixarray[int(ynow)][int(xnow)] = 0
        self.imageDisplay.display(pixarray)
        self.nImages = self.nImages + 1
        self.timenow = time.time()
        timediff = self.timenow - self.lasttime
        if(timediff>1) :
            self.imageRateText.setText(str(round(self.nImages/timediff)))
            QApplication.processEvents()
            self.lasttime = self.timenow 
            self.nImages = 0

