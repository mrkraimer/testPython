# ADViewer.py
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    ADViewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
    Mark Rivers
latest date 2020.07.21
    original development started 2019.12
'''

import sys,time,signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import numpy as np
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QGridLayout,QInputDialog
from PyQt5.QtWidgets import QRadioButton,QGroupBox
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import qRgb
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage
sys.path.append('../codecAD/')
from codecAD import CodecAD
sys.path.append('../dataToImageAD/')
from dataToImageAD import DataToImageAD
        
class ADViewer(QWidget) :
    def __init__(self,ntnda_Channel_Provider,providerName, parent=None):
        super(QWidget, self).__init__(parent)
        self.imageSize = 600
        self.isClosed = False
        self.provider = ntnda_Channel_Provider
        self.provider.ADViewer = self
        self.setWindowTitle(providerName + "_ADViewer")
        self.codecAD = CodecAD()
        self.dataToImage = DataToImageAD()
        self.imageDict = self.dataToImage.imageDictCreate()
        self.scaleType = 0
        self.nImages = 0
        self.colorTable = [qRgb(i,i,i) for i in range(256)]
        self.setColorTable = False
        self.zoomScale = 1
        self.codecIsNone = True
# first row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        self.startButton = QPushButton('start')
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.startEvent)
        self.isStarted = False
        box.addWidget(self.startButton)
        self.stopButton = QPushButton('stop')
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stopEvent)
        box.addWidget(self.stopButton)
        
        imageRateLabel = QLabel("imageRate:")
        box.addWidget(imageRateLabel)
        self.imageRateText = QLabel()
        self.imageRateText.setFixedWidth(40)
        box.addWidget(self.imageRateText) 
        if len(self.provider.getChannelName())<1 :
            name = os.getenv('EPICS_NTNDA_VIEWER_CHANNELNAME')
            if name!= None : self.provider.setChannelName(name)

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
        nxLabel = QLabel('nx: ')
        box.addWidget(nxLabel)
        self.nxText = QLabel('     ')
        box.addWidget(self.nxText)
        nyLabel = QLabel('ny: ')
        box.addWidget(nyLabel)
        self.nyText = QLabel('     ')
        box.addWidget(self.nyText)
        nzLabel = QLabel('nz: ')
        box.addWidget(nzLabel)
        self.nzText = QLabel('   ')
        box.addWidget(self.nzText)

        compressRatioLabel = QLabel('compressRatio:')
        box.addWidget(compressRatioLabel)
        self.compressRatioText = QLabel('1    ')
        box.addWidget(self.compressRatioText)

        codecNameLabel = QLabel('codec:')
        box.addWidget(codecNameLabel)
        self.codecNameText = QLabel('none   ')
        box.addWidget(self.codecNameText)
        self.clearButton = QPushButton('clear')
        self.clearButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearEvent)
        box.addWidget(self.clearButton)
        self.statusText = QLineEdit()
        self.statusText.setText('nothing done so far                    ')
        self.statusText.setFixedWidth(500)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
# third row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        
        box.addWidget(QLabel("channel dtype:"))
        self.dtypeChannelText = QLabel('      ')
        box.addWidget(self.dtypeChannelText)
        box.addWidget(QLabel(" "))
        box.addWidget(QLabel("image dtype:"))
        self.dtypeImageText = QLabel('      ')
        box.addWidget(self.dtypeImageText)
        
        box.addWidget(QLabel(" "))
        self.colorTableButton = QPushButton('colorTable')
        self.colorTableButton.setEnabled(True)
        self.colorTableButton.clicked.connect(self.colorTableEvent)
        self.useColorTable = False
        box.addWidget(self.colorTableButton)
        self.nocolorTableButton = QPushButton('nocolorTable')
        self.nocolorTableButton.setEnabled(False)
        self.nocolorTableButton.clicked.connect(self.nocolorTableEvent)
        box.addWidget(self.nocolorTableButton)

        box.addWidget(QLabel("red:"))
        self.redText = QLineEdit()
        self.redText.setFixedWidth(50)
        self.redText.setEnabled(True)
        self.redText.setText('1.0')
        self.redText.returnPressed.connect(self.colorLimitEvent)
        box.addWidget(self.redText)
        box.addWidget(QLabel("green:"))
        self.greenText = QLineEdit()
        self.greenText.setFixedWidth(50)
        self.greenText.setEnabled(True)
        self.greenText.setText('1.0')
        self.greenText.returnPressed.connect(self.colorLimitEvent)
        box.addWidget(self.greenText)
        box.addWidget(QLabel("blue:"))
        self.blueText = QLineEdit()
        self.blueText.setFixedWidth(50)
        self.blueText.setEnabled(True)
        self.blueText.setText('1.0')
        self.blueText.returnPressed.connect(self.colorLimitEvent)
        box.addWidget(self.blueText)

        wid =  QWidget()
        wid.setLayout(box)
        self.thirdRow = wid
# fourth row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)

        self.numpyImage = NumpyImage(flipy=False,imageSize=self.imageSize,isSeparateWindow=False)
        self.numpyImage.setZoomCallback(self.zoomEvent)
        box.addWidget(self.numpyImage)

        rightvbox = QVBoxLayout()
        remainingSize = self.imageSize

        vbox = QVBoxLayout()
        self.noScaleButton = QRadioButton('noScale')
        self.noScaleButton.setChecked(True)
        self.noScaleButton.toggled.connect(self.scaleEvent)
        self.autoScaleButton = QRadioButton('autoScale')
        self.autoScaleButton.toggled.connect(self.scaleEvent)
        vbox.addWidget(self.noScaleButton)
        vbox.addWidget(self.autoScaleButton)
        wid =  QWidget()
        wid.setLayout(vbox)
        wid.setFixedHeight(60)
        remainingSize = remainingSize - 60
        rightvbox.addWidget(wid)

        vbox = QVBoxLayout()
        self.resetButton = QPushButton('resetZoom')
        vbox.addWidget(self.resetButton)
        self.resetButton.setEnabled(True)
        self.resetButton.clicked.connect(self.resetEvent)
        self.zoomInButton = QPushButton('zoomIn')
        vbox.addWidget(self.zoomInButton)
        self.zoomInButton.setEnabled(True)
        self.zoomInButton.clicked.connect(self.zoomInEvent)
        self.zoomOutButton = QPushButton('zoomOut')
        vbox.addWidget(self.zoomOutButton)
        self.zoomOutButton.setEnabled(True)
        self.zoomOutButton.clicked.connect(self.zoomOutEvent)
        wid =  QWidget()
        wid.setLayout(vbox)
        wid.setFixedHeight(80)
        remainingSize = remainingSize - 80
        rightvbox.addWidget(wid)

        vbox = QVBoxLayout()
        self.x1Button = QRadioButton('x1')
        self.x1Button.toggled.connect(self.zoomScaleEvent)
        self.x1Button.setChecked(True)
        vbox.addWidget(self.x1Button)
        self.x2Button = QRadioButton('x2')
        self.x2Button.toggled.connect(self.zoomScaleEvent)
        vbox.addWidget(self.x2Button)
        self.x4Button = QRadioButton('x4')
        self.x4Button.toggled.connect(self.zoomScaleEvent)
        vbox.addWidget(self.x4Button)
        self.x8Button = QRadioButton('x8')
        self.x8Button.toggled.connect(self.zoomScaleEvent)
        vbox.addWidget(self.x8Button)
        self.x16Button = QRadioButton('x16')
        self.x16Button.toggled.connect(self.zoomScaleEvent)
        vbox.addWidget(self.x16Button)
        wid =  QWidget()
        wid.setLayout(vbox)
        wid.setFixedHeight(120)
        remainingSize = remainingSize - 120
        rightvbox.addWidget(wid)

        vbox = QVBoxLayout()
        label = QLabel("")
        vbox.addWidget(label)
        wid =  QWidget()
        wid.setLayout(vbox)
        wid.setFixedHeight(remainingSize)
        rightvbox.addWidget(wid)

        wid =  QWidget()
        wid.setLayout(rightvbox)
        wid.setFixedHeight(self.imageSize)
        box.addWidget(wid)

        wid =  QWidget()
        wid.setLayout(box)
        self.fourthRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.secondRow,1,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.thirdRow,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.fourthRow,3,0,alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.subscription = None
        self.lasttime = time.time() -2
        self.arg = None
        self.show()
        self.numpyImage.show()

    def resetEvent(self) :
        if type(self.imageDict["image"])==type(None) : return
        self.numpyImage.resetZoom()
        self.display()

    def zoomInEvent(self) :
        if not self.numpyImage.zoomIn(self.zoomScale) : 
            self.statusText.setText('zoomIn failed')
            return
        self.display()

    def zoomOutEvent(self) :
        if not self.numpyImage.zoomOut(self.zoomScale) : 
            self.statusText.setText('zoomOut failed')
            return   
        self.display()

    def scaleEvent(self) :
         if self.noScaleButton.isChecked() :
            self.scaleType = 0
         elif self.autoScaleButton.isChecked() :
            self.scaleType = 1
         else :
            self.statusText.setText('why is no scaleButton enabled?')
         self.display()    

    def zoomScaleEvent(self) :
        if self.x1Button.isChecked() :
            self.zoomScale = 1
        elif  self.x2Button.isChecked() :
            self.zoomScale = 2
        elif  self.x4Button.isChecked() :
            self.zoomScale = 4
        elif  self.x8Button.isChecked() :
            self.zoomScale = 8
        elif  self.x16Button.isChecked() :
            self.zoomScale = 16
        else :
            self.statusText.setText('why is no zoomScale enabled?')

    def zoomEvent(self,zoomData) :
        self.display()

    def display(self) :
        if self.isClosed : return
        if type(self.imageDict["image"])==type(None) : return
        try :
            if self.setColorTable :
                self.numpyImage.display(self.imageDict["image"],colorTable=self.colorTable)
            else :
                self.numpyImage.display(self.imageDict["image"])
        except Exception as error:
            self.statusText.setText(str(error))    

    def closeEvent(self, event) :
        self.isClosed = True
        self.numpyImage.setOkToClose()
        self.numpyImage.close()

    def startEvent(self) :
        self.start()

    def stopEvent(self) :
        self.stop()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")

    def colorTableEvent(self) :
        self.colorTableButton.setEnabled(False)
        self.nocolorTableButton.setEnabled(True)
        self.setColorTable = True
        self.display()

    def nocolorTableEvent(self) :
        self.colorTableButton.setEnabled(True)
        self.nocolorTableButton.setEnabled(False) 
        self.setColorTable = False
        self.display()    

    def colorLimitEvent(self) :
        try :
           red = float(self.redText.text())
           if red <0.0 : raise Exception('red is less than zero')
           green = float(self.greenText.text())
           if green <0.0 : raise Exception('green is less than zero')
           blue = float(self.blueText.text())
           if blue <0.0 : raise Exception('blue is less than zero')
           maxvalue = red
           if green>maxvalue : maxvalue = green
           if blue>maxvalue : maxvalue = blue
           if maxvalue<=0 :
               raise Exception('at least one of red,green,blue must be > 0')
           red = red/maxvalue
           green = green/maxvalue
           blue = blue/maxvalue
           colorTable = []
           for ind in range(256) :
               r = int(ind*red)
               g = int(ind*green)
               b = int(ind*blue)
               colorTable.append(qRgb(r,g,b))
           self.colorTable = colorTable  
           self.display()
        except Exception as error:
            self.statusText.setText(str(error))    

    def channelNameEvent(self) :
        try:
            self.provider.setChannelName(self.channelNameText.text())
        except Exception as error:
            self.statusText.setText(str(error))

    def start(self) :
        self.isStarted = True
        self.provider.start()
        self.channelNameText.setEnabled(False)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.channelNameText.setEnabled(False)

    def stop(self) :
        self.isStarted = False
        self.provider.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.channelNameLabel.setStyleSheet("background-color:gray")
        self.channelNameText.setEnabled(True)
        self.channel = None
        self.imageRateText.setText('0')

    def callback(self,arg):
        if type(arg)==type(None) : return
        if self.isClosed : return
        if not self.isStarted : return
        if len(arg)==1 :
            value = arg.get("exception")
            if value!=None :
                self.statusText.setText(str(value))
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
        try:
            data = arg['value']
            dimArray = arg['dimension']
            ndim = len(dimArray)
            if ndim!=2 and ndim!=3 :
                self.statusText.setText('ndim not 2 or 3')
                return            
            compressed = arg['compressedSize']
            uncompressed = arg['uncompressedSize']
            codec = arg['codec']
            codecName = codec['name']
            codecNameLength = len(codecName)
            if self.codecAD.decompress(data,codec,compressed,uncompressed) :
                self.codecIsNone = False
                self.codecNameText.setText(self.codecAD.getCodecName())
                data = self.codecAD.getData()
                self.compressRatioText.setText(str(self.codecAD.getCompressRatio()))
            else :
                if not self.codecIsNone :
                    self.codecIsNone = True
                    self.codecNameText.setText(self.codecAD.getCodecName()) 
                    self.compressRatioText.setText(str(self.codecAD.getCompressRatio()))
        except Exception as error:
            self.statusText.setText(str(error))
            return
        try:
            self.dataToImage.dataToImage(data,dimArray,self.imageSize,scaleType=self.scaleType)
            imageDict = self.dataToImage.getImageDict()
            self.imageDict["image"] = imageDict["image"]
            if self.imageDict["dtypeChannel"]!=imageDict["dtypeChannel"] :
                self.imageDict["dtypeChannel"] = imageDict["dtypeChannel"]
                self.dtypeChannelText.setText(str(self.imageDict["dtypeChannel"]))
            if self.imageDict["dtypeImage"]!=imageDict["dtypeImage"] :
                self.imageDict["dtypeImage"] = imageDict["dtypeImage"]
                self.dtypeImageText.setText(str(self.imageDict["dtypeImage"]))
            if self.imageDict["nx"]!=imageDict["nx"] :
                self.imageDict["nx"] = imageDict["nx"]
                self.nxText.setText(str(self.imageDict["nx"]))
            if self.imageDict["ny"]!=imageDict["ny"] :
                self.imageDict["ny"] = imageDict["ny"]
                self.nyText.setText(str(self.imageDict["ny"]))
            if self.imageDict["nz"]!=imageDict["nz"] :
                self.imageDict["nz"] = imageDict["nz"]
                self.nzText.setText(str(self.imageDict["nz"]))        
            self.display()
        except Exception as error:
            self.statusText.setText(str(error))
        self.nImages = self.nImages + 1
        self.timenow = time.time()
        timediff = self.timenow - self.lasttime
        if(timediff>1) :
            self.imageRateText.setText(str(round(self.nImages/timediff)))
            self.lasttime = self.timenow 
            self.nImages = 0

