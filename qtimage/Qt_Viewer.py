# Qt_Viewer.py
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout,QInputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage,qRgb

import sys,time
import numpy as np
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage
        
class Qt_Viewer(QWidget) :
    def __init__(self,data_Provider, providerName,parent=None):
        super(QWidget, self).__init__(parent)
        self.isClosed = False
        self.provider = data_Provider
        self.setWindowTitle(providerName +"_Qt_Viewer")
        self.imageDisplay = NumpyImage(windowTitle='qtimage')
        self.formatChoices = None
        self.rgbTable = [qRgb(i/2, i, i/2) for i in range(256)]
# first row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        self.startButton = QPushButton('start')
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.startEvent)
        self.startButton.setFixedWidth(40)
        self.isStarted = False
        box.addWidget(self.startButton)
        self.stopButton = QPushButton('stop')
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stopEvent)
        self.stopButton.setFixedWidth(40)
        box.addWidget(self.stopButton)
        self.nImages = 0
        imageRateLabel = QLabel("imageRate:")
        box.addWidget(imageRateLabel)
        self.imageRateText = QLabel()
        self.imageRateText.setFixedWidth(40)
        box.addWidget(self.imageRateText)
        self.channelNameLabel = QLabel("channelName:")
        box.addWidget(self.channelNameLabel)
        self.channelNameText = QLineEdit()
        self.channelNameText.setFixedWidth(600)
        self.channelNameText.setEnabled(True)
        self.channelNameText.setText(self.provider.getChannelName())
        self.channelNameText.editingFinished.connect(self.channelNameEvent)
        box.addWidget(self.channelNameText)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
# second row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        self.formatButton = QPushButton('setFormat')
        self.formatButton.setEnabled(True)
        self.formatButton.clicked.connect(self.formatEvent)
        self.formatButton.setFixedWidth(80)
        box.addWidget(self.formatButton)
        formatLabel = QLabel("format:")
        box.addWidget(formatLabel)
        self.formatText = QLabel()
        self.formatText.setFixedWidth(120)
        box.addWidget(self.formatText)
        self.clearButton = QPushButton('clear')
        self.clearButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearEvent)
        self.clearButton.setFixedWidth(40)
        box.addWidget(self.clearButton)
        self.statusText = QLineEdit()
        self.statusText.setText('nothing done so far')
        self.statusText.setFixedWidth(500)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.secondRow,1,0,alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.setGeometry(QRect(10, 20, 800, 100))
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
        
    def formatEvent(self) : 
        items = self.formatChoices
        if items==None :
            self.statusText.setText('never connected')
            return
        isStarted = self.isStarted 
        if isStarted :  self.provider.stop()
        item, okPressed = QInputDialog.getItem(self, "Get item  ","Format:  ", items, 0, False)
        if okPressed and item:
            ind = self.formatChoices.index(item)
            self.statusText.setText(str(ind))
            self.provider.putInt(ind,'field(argument.format.index)')
        if isStarted : self.provider.start()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")
        
    def channelNameEvent(self) :
        try:
            self.provider.setChannelName(self.channelNameText.text())
        except Exception as error:
            self.statusText.setText(str(error))     

    def start(self) :
        self.isStarted = True
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.formatButton.setEnabled(False)
        self.channelNameText.setEnabled(False)
        self.provider.start()

    def stop(self) :
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.formatButton.setEnabled(True)
        self.channelNameText.setEnabled(True)
        self.isStarted = False
        self.provider.stop()

    def callback(self,arg):
        if self.isClosed : return
        if not self.isStarted : return
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
        Format = value['format']
        index = int(Format['index'])
        self.formatChoices = Format['choices']
        formatName = Format['choices'][index]
        self.formatText.setText(formatName)
        height = value['height']
        width = value['width']
        value = value['value']
        if formatName=='Grayscale8' :
            try :
                data = value[0]['uint8']
                image = np.reshape(data,(height,width))
                self.imageDisplay.display(image,Format=QImage.Format_Grayscale8)
            except Exception as error :
                self.statusText.setText('illegal dtype ' + str(error))
                return
        elif formatName=='Indexed8' :
            try :
                data = value[0]['uint8']
                image = np.reshape(data,(height,width))
                self.imageDisplay.display(\
                    image,Format=QImage.Format_Indexed8,colorTable=self.rgbTable)
            except Exception as error :
                self.statusText.setText('illegal dtype ' + str(error))
                return         
        elif formatName=='RGB888' :
            try:
                data = value[0]['uint8']
                image = np.reshape(data,(height,width,3))
                self.imageDisplay.display(image,Format=QImage.Format_RGB888)
            except Exception as error :
                self.statusText.setText('illegal dtype ' + str(error))
                return    
                
        elif formatName=='Grayscale16' :
            try :
                data = value[0]['uint16']
                image = np.reshape(data,(height,width))
                self.imageDisplay.display(image,Format=QImage.Format_Grayscale16)
            except Exception as error :
                self.statusText.setText('illegal dtype ' + str(error))
                return    
        else :
            self.statusText.setText('format ' + formatName + ' not yet supported')
            return
        self.nImages = self.nImages + 1
        self.timenow = time.time()
        timediff = self.timenow - self.lasttime
        if(timediff>1) :
            self.imageRateText.setText(str(round(self.nImages/timediff)))
            QApplication.processEvents()
            self.lasttime = self.timenow 
            self.nImages = 0

