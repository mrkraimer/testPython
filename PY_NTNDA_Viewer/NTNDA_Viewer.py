# NTNDA_Viewer.py
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
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
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout,QInputDialog
from PyQt5.QtWidgets import QRadioButton,QGroupBox
from PyQt5.QtCore import *
from PyQt5.QtGui import qRgb
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage
sys.path.append('../codecAD/')
from codecAD import CodecAD
sys.path.append('../channelToImageAD/')
from channelToImageAD import ChannelToImageAD
sys.path.append('../colorTable/')
from colorTable import ColorTable
sys.path.append('../showInfo/')
from showInfo import ShowInfo

import ctypes
import ctypes.util
import os
import math
        
class NTNDA_Viewer(QWidget) :
    def __init__(self,ntnda_Channel_Provider,providerName, parent=None):
        super(QWidget, self).__init__(parent)
        self.imageSize = 800
        self.isClosed = False
        self.provider = ntnda_Channel_Provider
        self.provider.NTNDA_Viewer = self
        self.setWindowTitle(providerName + "_NTNDA_Viewer")
        self.codecAD = CodecAD()
        self.channelToImage = ChannelToImageAD()
        self.colorTable = ColorTable()
        self.colorTable.setColorChangeCallback(self.colorChangeEvent)
        self.colorTable.setExceptionCallback(self.colorExceptionEvent)
        self.channelDict= self.channelToImage.channelDictCreate()
        self.numpyImage = NumpyImage(flipy=False,imageSize=self.imageSize)
        self.showInfo = ShowInfo()
        self.numpyImage.setZoomCallback(self.zoomEvent)
        self.numpyImage.setResizeCallback(self.resizeImageEvent)
        self.numpyImage.setMouseClickCallback(self.mouseClickEvent)
        self.manualLimits = False
        self.showLimits= False
        self.nImages = 0
        self.zoomScale = 1
        self.codecIsNone = True
# first row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        self.startButton = QPushButton('start')
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.startEvent)
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

        self.imageSizeLabel = QLabel("imageSize:")
        box.addWidget(self.imageSizeLabel)
        self.imageSizeText = QLineEdit()
        self.imageSizeText.setFixedWidth(60)
        self.imageSizeText.setEnabled(True)
        self.imageSizeText.setText(str(self.imageSize))
        self.imageSizeText.returnPressed.connect(self.imageSizeEvent)
        box.addWidget(self.imageSizeText)

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
        wid.setFixedHeight(30)
        self.firstRow = wid
# second row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)

        self.showInfoButton = QPushButton('showInfo')
        box.addWidget(self.showInfoButton)
        self.showInfoButton.setEnabled(True)
        self.showInfoButton.clicked.connect(self.showInfoEvent)

        self.showColorTableButton = QPushButton('showColorTable')
        self.showColorTableButton.setEnabled(True)
        self.showColorTableButton.clicked.connect(self.showColorTableEvent)
        box.addWidget(self.showColorTableButton)
              
        self.compressRatio = round(1.0)
        compressRatioLabel = QLabel('compressRatio:')
        box.addWidget(compressRatioLabel)
        self.compressRatioText = QLabel('1    ')
        box.addWidget(self.compressRatioText)
        self.codecName = ''
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
        wid.setFixedHeight(30)
        self.secondRow = wid
# third row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)

        box.addWidget(QLabel('channelLimits: '))
        self.channelLimitsText = QLabel()
        self.channelLimitsText.setFixedWidth(180)
        box.addWidget(self.channelLimitsText)
  
        box.addWidget(QLabel('imageLimits: '))
        self.imageLimitsText = QLabel()
        self.imageLimitsText.setFixedWidth(80)
        box.addWidget(self.imageLimitsText)

        self.resetButton = QPushButton('resetZoom')
        box.addWidget(self.resetButton)
        self.resetButton.setEnabled(True)
        self.resetButton.clicked.connect(self.resetEvent)
        self.zoomInButton = QPushButton('zoomIn')
        box.addWidget(self.zoomInButton)
        self.zoomInButton.setEnabled(True)
        self.zoomInButton.clicked.connect(self.zoomInEvent)
        self.zoomOutButton = QPushButton('zoomOut')
        box.addWidget(self.zoomOutButton)
        self.zoomOutButton.setEnabled(True)
        self.zoomOutButton.clicked.connect(self.zoomOutEvent)

        showbox = QHBoxLayout()
        self.x1Button = QRadioButton('x1')
        self.x1Button.toggled.connect(self.zoomScaleEvent)
        self.x1Button.setChecked(True)
        showbox.addWidget(self.x1Button)
        self.x2Button = QRadioButton('x2')
        self.x2Button.toggled.connect(self.zoomScaleEvent)
        showbox.addWidget(self.x2Button)
        self.x4Button = QRadioButton('x4')
        self.x4Button.toggled.connect(self.zoomScaleEvent)
        showbox.addWidget(self.x4Button)
        self.x8Button = QRadioButton('x8')
        self.x8Button.toggled.connect(self.zoomScaleEvent)
        showbox.addWidget(self.x8Button)
        self.x16Button = QRadioButton('x16')
        self.x16Button.toggled.connect(self.zoomScaleEvent)
        showbox.addWidget(self.x16Button)
        wid = QWidget()
        wid.setLayout(showbox)
        box.addWidget(wid)

        showbox = QHBoxLayout()
        groupbox=QGroupBox('(xmin,xmax,ymin,ymax)')
        self.zoomText =  QLabel('')
        self.zoomText.setFixedWidth(200)
        self.zoomText.setFixedHeight(15)
        showbox.addWidget(self.zoomText)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)

        wid =  QWidget()
        wid.setLayout(box)
        wid.setFixedHeight(80)
        self.thirdRow = wid
# fourth row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)

        showbox = QHBoxLayout()
        groupbox=QGroupBox('showLimits')
        self.showLimitsButton = QRadioButton('yes')
        self.showLimitsButton.toggled.connect(self.showLimitsEvent)
        self.noshowLimitsButton = QRadioButton('no')
        self.noshowLimitsButton.toggled.connect(self.noshowLimitsEvent)
        self.noshowLimitsButton.setChecked(True)
        showbox.addWidget(self.showLimitsButton)
        showbox.addWidget(self.noshowLimitsButton)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)

        showbox = QHBoxLayout()
        groupbox=QGroupBox('scaleType')
        self.autoScaleButton = QRadioButton('auto')
        self.autoScaleButton.toggled.connect(self.scaleEvent)
        self.autoScaleButton.setChecked(True)
        self.manualScaleButton = QRadioButton('manual')
        self.manualScaleButton.toggled.connect(self.scaleEvent)
        showbox.addWidget(self.autoScaleButton)
        showbox.addWidget(self.manualScaleButton)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)

        showbox = QHBoxLayout()
        groupbox=QGroupBox('manualLimits')
        showbox.addWidget(QLabel("min:"))
        self.minLimitText = QLineEdit()
        self.minLimitText.setFixedWidth(50)
        self.minLimitText.setEnabled(True)
        self.minLimitText.setText('0')
        self.minLimitText.returnPressed.connect(self.manualLimitsEvent)
        showbox.addWidget(self.minLimitText)
        showbox.addWidget(QLabel("max:"))
        self.maxLimitText = QLineEdit()
        self.maxLimitText.setFixedWidth(50)
        self.maxLimitText.setEnabled(True)
        self.maxLimitText.setText('255')
        self.maxLimitText.returnPressed.connect(self.manualLimitsEvent)
        showbox.addWidget(self.maxLimitText)
        groupbox.setLayout(showbox)
        wid.setFixedHeight(50)
        box.addWidget(groupbox)

        wid =  QWidget()
        wid.setLayout(box)
        wid.setFixedHeight(70)
        self.fourthRow = wid
# fifth row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        box.addWidget(QLabel())
        wid =  QWidget()
        wid.setLayout(box)
        self.fifthRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.secondRow,1,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.thirdRow,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.fourthRow,3,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.fifthRow,4,0,alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.subscription = None
        self.lasttime = time.time() -2
        self.arg = None
        self.show()

    def showInfoEvent(self) :
        self.showInfo.show()

    def colorChangeEvent(self) :
        self.display()

    def showColorTableEvent(self) :
        self.colorTable.show()

    def colorExceptionEvent(self,error) :
        self.statusText.setText(error)
        
    def resetEvent(self) :
        if self.channelDict['nx']==0 : return
        self.zoomText.setText('')
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
        self.zoomText.setText(str(zoomData))
        self.display()
                
    def resizeImageEvent(self,event,width,height) :
        self.imageSizeText.setText(str(width))
        self.numpyImage.setImageSize(width)
        self.resetEvent()

    def mouseClickEvent(self,event,imageDict) :
        self.showInfo.setImageInfo(imageDict)
                       
    def display(self) :
        if self.isClosed : return
        if type(self.channelDict["image"])==type(None) : return
        try :
            if self.channelDict["nz"]==3 :
                self.numpyImage.display(self.channelDict["image"])
            else :
                self.numpyImage.display(self.channelDict["image"],colorTable=self.colorTable.getColorTable())
        except Exception as error:
            self.statusText.setText(str(error))

    def closeEvent(self, event) :
        self.numpyImage.setOkToClose()
        self.numpyImage.close()
        self.colorTable.setOkToClose()
        self.colorTable.close()
        self.showInfo.setOkToClose()
        self.showInfo.close()

    def startEvent(self) :
        self.start()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")

    def scaleEvent(self) :
         if self.autoScaleButton.isChecked() :
            self.manualLimits = False
         elif self.manualScaleButton.isChecked() :
            self.manualLimits = True
         else :
            self.statusText.setText('why is no scaleButton enabled?')
         self.display()

    def stopEvent(self) :
        self.stop()

    def showLimitsEvent(self) :  
        self.showLimits = True
        
    def noshowLimitsEvent(self) :  
        self.showLimits = False

    def manualLimitsEvent(self) :
        try:
            low = int(self.minLimitText.text())
            high = int(self.maxLimitText.text())
            self.channelToImage.setManualLimits((low,high))
            self.display()
        except Exception as error:
            self.statusText.setText(str(error))

    def imageSizeEvent(self) :
        try:
            size = self.imageSizeText.text()
            try :
                value = int(size)
            except Exception as error:
                self.statusText.setText('value is not an integer')
                self.imageSizeText.setText(str(self.imageSize))
                return
            if value<128 :
                value = 128
                self.imageSizeText.setText(str(value))
            if value>1024 :
                value = 1024
                self.imageSizeText.setText(str(value))
            self.resetEvent()
            self.imageSize = value   
            self.numpyImage.setImageSize(self.imageSize)
        except Exception as error:
            self.statusText.setText(str(error))

            
    def channelNameEvent(self) :
        try:
            self.provider.setChannelName(self.channelNameText.text())
        except Exception as error:
            self.statusText.setText(str(error))
         
    def start(self) :
        self.provider.start()
        self.channelNameText.setEnabled(False)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.channelNameText.setEnabled(False)

    def stop(self) :
        self.provider.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.channelNameLabel.setStyleSheet("background-color:gray")
        self.channelNameText.setEnabled(True)
        self.channel = None
        self.imageRateText.setText('0')

    def callback(self,arg):
        if self.isClosed : return
        if type(arg)==type(None) : return
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
                    self.codecNameText.setText('none') 
                    self.compressRatioText.setText('1.0') 
        except Exception as error:
            self.statusText.setText(str(error))
            return
        try:
            self.channelToImage.channelToImage(data,dimArray,self.imageSize,\
                manualLimits=self.manualLimits,\
                showLimits=self.showLimits)
            channelDict= self.channelToImage.getChannelDict()
            callShowInfo = False
            self.channelDict["image"] = channelDict["image"]
            if self.channelDict["dtypeChannel"]!=channelDict["dtypeChannel"] :
                self.channelDict["dtypeChannel"] = channelDict["dtypeChannel"]
                callShowInfo = True
            if self.channelDict["dtypeImage"]!=channelDict["dtypeImage"] :
                self.channelDict["dtypeImage"] = channelDict["dtypeImage"]
            if self.channelDict["nx"]!=channelDict["nx"] :
                self.channelDict["nx"] = channelDict["nx"]
                callShowInfo = True
            if self.channelDict["ny"]!=channelDict["ny"] :
                self.channelDict["ny"] = channelDict["ny"]
                callShowInfo = True
            if self.channelDict["nz"]!=channelDict["nz"] :
                self.channelDict["nz"] = channelDict["nz"]
                callShowInfo = True
            if self.channelDict["compress"]!=channelDict["compress"] :
                self.channelDict["compress"] = channelDict["compress"]
                callShowInfo = True
            if  callShowInfo :
                self.showInfo.setChannelInfo(self.channelDict) 
            if self.showLimits :
                self.channelLimitsText.setText(str(self.channelToImage.getChannelLimits()))
                self.imageLimitsText.setText(str(self.channelToImage.getImageLimits()))
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

