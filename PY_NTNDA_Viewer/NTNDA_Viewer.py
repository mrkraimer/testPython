# NTNDA_Viewer.py
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

author Marty Kraimer
    latest date 2020.03.02
    original development started 2019.12
'''

import sys,time,signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import numpy as np
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout,QInputDialog
from PyQt5.QtWidgets import QRadioButton,QGroupBox
from PyQt5.QtCore import *
sys.path.append('../numpyImage/')
from numpyImage import NumpyImage
import ctypes
import ctypes.util
import os
import math

def imageDictCreate() :
    return {"image" : None , "dtypeChannel" : None , "dtypeImage" : None  , "nx" : 0 , "ny" : 0 ,  "nz" : 0 }


class FindLibrary(object) :
    def __init__(self, parent=None):
        self.save = dict()
    def find(self,name) :
        lib = self.save.get(name)
        if lib!=None : return lib
        result = ctypes.util.find_library(name)
        if result==None : return None
        if os.name == 'nt':
            lib = ctypes.windll.LoadLibrary(result)
        else :
            lib = ctypes.cdll.LoadLibrary(result)
        if lib!=None : self.save.update({name : lib})
        return lib
        
class NTNDA_Viewer(QWidget) :
    def __init__(self,ntnda_Channel_Provider,providerName, parent=None):
        super(QWidget, self).__init__(parent)
        self.imageSize = 800
        self.isClosed = False
        self.provider = ntnda_Channel_Provider
        self.provider.NTNDA_Viewer = self
        self.setWindowTitle(providerName + "_NTNDA_Viewer")
        self.imageDict = imageDictCreate()
        self.imageDisplay = NumpyImage(windowTitle='image',flipy=False,imageSize=self.imageSize)
        self.imageDisplay.setZoomCallback(self.zoomEvent)
        self.imageDisplay.setMousePressCallback(self.mousePressEvent)
        self.imageDisplay.setMouseReleaseCallback(self.mouseReleaseEvent)
        self.imageDisplay.setResizeCallback(self.resizeImageEvent)
        self.limitType = 0
        self.limits = (0,255)
        self.showLimits = False
        self.suppressBackground = False
        self.nImages = 0
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
        self.secondRow = wid
# third row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        dtypeChannelLabel = QLabel('dtypeChannel: ')
        box.addWidget(dtypeChannelLabel)
        self.dtypeChannelText = QLabel('      ')
        box.addWidget(self.dtypeChannelText)
        dtypeImageLabel = QLabel('dtypeImage: ')
        box.addWidget(dtypeImageLabel)
        self.dtypeImageText = QLabel('      ')
        box.addWidget(self.dtypeImageText)
        zoomLabel = QLabel('zoom ')
        box.addWidget(zoomLabel)
        self.resetButton = QPushButton('reset')
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
        zoomCordLabel = QLabel(' (xmin,xmax,ymin,ymax) = ')
        box.addWidget(zoomCordLabel)
        self.zoomText =  QLabel('')
        self.zoomText.setFixedWidth(400)
        box.addWidget(self.zoomText,alignment=Qt.AlignLeft)
        wid =  QWidget()
        wid.setLayout(box)
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
        self.noScaleButton = QRadioButton('noScale')
        self.noScaleButton.setChecked(True)
        self.noScaleButton.toggled.connect(self.noScaleEvent)
        self.autoScaleButton = QRadioButton('autoScale')
        self.autoScaleButton.toggled.connect(self.autoScaleEvent)
        self.manualScaleButton = QRadioButton('manualScale')
        self.manualScaleButton.toggled.connect(self.manualScaleEvent)
        showbox.addWidget(self.noScaleButton)
        showbox.addWidget(self.autoScaleButton)
        showbox.addWidget(self.manualScaleButton)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)
        
        showbox = QHBoxLayout()
        groupbox=QGroupBox('suppressBackground')
        self.suppressBackgroundButton = QRadioButton('yes')
        self.suppressBackgroundButton.toggled.connect(self.suppressBackgroundEvent)
        self.nosuppressBackgroundButton = QRadioButton('no')
        self.nosuppressBackgroundButton.toggled.connect(self.nosuppressBackgroundEvent)
        self.nosuppressBackgroundButton.setChecked(True)
        showbox.addWidget(self.suppressBackgroundButton)
        showbox.addWidget(self.nosuppressBackgroundButton)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)
        
        showbox = QHBoxLayout()
        groupbox=QGroupBox('manualLimits')
        showbox.addWidget(QLabel("minimum:"))
        self.minLimitText = QLineEdit()
        self.minLimitText.setFixedWidth(60)
        self.minLimitText.setEnabled(True)
        self.minLimitText.setText('0')
        self.minLimitText.returnPressed.connect(self.minLimitEvent)
        showbox.addWidget(self.minLimitText)
        
        showbox.addWidget(QLabel("maximum:"))
        self.maxLimitText = QLineEdit()
        self.maxLimitText.setFixedWidth(60)
        self.maxLimitText.setEnabled(True)
        self.maxLimitText.setText('255')
        self.maxLimitText.returnPressed.connect(self.maxLimitEvent)
        showbox.addWidget(self.maxLimitText)
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)
        
        groupbox.setLayout(showbox)
        box.addWidget(groupbox)
        
        wid =  QWidget()
        wid.setLayout(box)
        self.fourthRow = wid
# fifth row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        channelLimitsLabel = QLabel('channelLimits: ')
        box.addWidget(channelLimitsLabel)
        self.channelLimitsText = QLabel()
        self.channelLimitsText.setFixedWidth(150)
        box.addWidget(self.channelLimitsText)
                
        imageLimitsLabel = QLabel('imageLimits: ')
        box.addWidget(imageLimitsLabel)
        self.imageLimitsText = QLabel()
        self.imageLimitsText.setFixedWidth(100)
        box.addWidget(self.imageLimitsText)

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
        self.findLibrary = FindLibrary()
        self.subscription = None
        self.lasttime = time.time() -2
        self.arg = None
        self.show()
        
    def resetEvent(self) :
        if self.imageDict['nx']==0 : return
        self.zoomText.setText('')
        self.imageDisplay.resetZoom()
        self.display()

    def zoomInEvent(self) :
        if self.isStarted :
            self.statusText.setText('zoomIn can only be done when stopped')
            return
        if not self.imageDisplay.zoomIn() : 
            self.statusText.setText('zoomIn failed')
            return
        self.display()

    def zoomOutEvent(self) :
        if self.isStarted :
            self.statusText.setText('zoomOut can only be done when stopped')
            return
        if not self.imageDisplay.zoomOut() : 
            self.statusText.setText('zoomOut failed')
            return   
        self.display()

    def zoomEvent(self,zoomData) :
        self.zoomText.setText(str(zoomData))
        self.display()

    def mousePressEvent(self,event) :
        if self.isStarted : self.provider.stop()

    def mouseReleaseEvent(self,event) :
        if self.isStarted : self.provider.start()
        
    def resizeImageEvent(self,event,width,height) :
        self.imageSizeText.setText(str(width))
        self.imageDisplay.setImageSize(width)
                 
    def display(self) :
        if self.isClosed : return
        if type(self.imageDict["image"])==type(None) : return
        try :
            self.imageDisplay.display(self.imageDict["image"])
        except Exception as error:
            self.statusText.setText(str(error))    

    def closeEvent(self, event) :
        if self.isStarted : self.stop()
        self.isClosed = True
        self.imageDisplay.okToClose = True
        self.imageDisplay.close()
        
    def startEvent(self) :
        self.start()

    def stopEvent(self) :
        self.stop()

    def clearEvent(self) :
        self.statusText.setText('')
        self.statusText.setStyleSheet("background-color:white")
        
    def noScaleEvent(self) :  
        self.limitType = 0
        self.display()
         
    def autoScaleEvent(self) :  
        self.limitType = 1
        self.display()
         
    def manualScaleEvent(self) :  
        self.limitType = 2
        self.display()
        
    def showLimitsEvent(self) :  
        self.showLimits = True
        
    def noshowLimitsEvent(self) :  
        self.showLimits = False

    def suppressBackgroundEvent(self) :  
        self.suppressBackground = True
        
    def nosuppressBackgroundEvent(self) :  
        self.suppressBackground = False        

    def minLimitEvent(self) :
        try:
            self.display()
        except Exception as error:
            self.statusText.setText(str(error))

    def imageSizeEvent(self,display=True) :
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
            self.imageDisplay.setImageSize(self.imageSize)
        except Exception as error:
            self.statusText.setText(str(error))

    def maxLimitEvent(self) :
        try:
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
        self.imageSizeText.setEnabled(False)
        self.zoomInButton.setEnabled(False)
        self.zoomOutButton.setEnabled(False)
        self.minLimitText.setEnabled(False)
        self.maxLimitText.setEnabled(False)

    def stop(self) :
        self.isStarted = False
        self.provider.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.channelNameLabel.setStyleSheet("background-color:gray")
        self.channelNameText.setEnabled(True)
        self.imageSizeText.setEnabled(True)
        self.zoomInButton.setEnabled(True)
        self.zoomOutButton.setEnabled(True)
        self.minLimitText.setEnabled(True)
        self.maxLimitText.setEnabled(True)
        self.channel = None
        self.imageRateText.setText('0')
    def callback(self,arg):
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
            compressed = arg['compressedSize']
            uncompressed = arg['uncompressedSize']
            codec = arg['codec']
            codecName = codec['name']
            codecNameLength = len(codecName)
        except Exception as error:
            self.statusText.setText(str(error))
            return
        ndim = len(dimArray)
        if ndim!=2 and ndim!=3 :
            self.statusText.setText('ndim not 2 or 3')
            return
        if codecNameLength == 0 : 
            codecName = 'none'
            if codecName!=self.codecName : 
                self.codecName = codecName
                self.codecNameText.setText(self.codecName)
            ratio = round(1.0)
            if ratio!=self.compressRatio :
                self.compressRatio = ratio
                self.compressRatioText.setText(str(self.compressRatio))
        try:
            if codecNameLength != 0 : 
                data = self.decompress(data,codec,compressed,uncompressed)
            self.dataToImage(data,dimArray)
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

    def decompress(self,data,codec,compressed,uncompressed) :
        codecName = codec['name']
        if codecName!=self.codecName : 
            self.codecName = codecName
            self.codecNameText.setText(self.codecName)
        typevalue = codec['parameters']
        if typevalue== 1 : dtype = "int8"; elementsize =int(1)
        elif typevalue== 5 : dtype = "uint8"; elementsize =int(1)
        elif typevalue== 2 : dtype = "int16"; elementsize =int(2)
        elif typevalue== 6 : dtype = "uint16"; elementsize =int(2)
        elif typevalue== 3 : dtype = "int32"; elementsize =int(4)
        elif typevalue== 7 : dtype = "uint32"; elementsize =int(4)
        elif typevalue== 4 : dtype = "int64"; elementsize =int(8)
        elif typevalue== 8 : dtype = "uint64"; elementsize =int(8)
        elif typevalue== 9 : dtype = "float32"; elementsize =int(4)
        elif typevalue== 10 : dtype = "float64"; elementsize =int(8)
        else : raise Exception('decompress mapIntToType failed')
        if codecName=='blosc':
            lib = self.findLibrary.find(codecName)
        elif codecName=='jpeg' :
            lib = self.findLibrary.find('decompressJPEG')
        elif codecName=='lz4' or codecName=='bslz4' :
            lib = self.findLibrary.find('bitshuffle')
        else : lib = None
        if lib==None : raise Exception('shared library ' +codecName + ' not found')
        inarray = bytearray(data)
        in_char_array = ctypes.c_ubyte * compressed
        out_char_array = ctypes.c_ubyte * uncompressed
        outarray = bytearray(uncompressed)
        if codecName=='blosc' : 
            lib.blosc_decompress(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif codecName=='lz4' :
            lib.LZ4_decompress_fast(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif codecName=='bslz4' :
            lib.bshuf_decompress_lz4(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),int(uncompressed/elementsize),
                 elementsize,int(0))
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif codecName=='jpeg' :
            lib.decompressJPEG(
                 in_char_array.from_buffer(inarray),compressed,
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = data.flatten()
        else : raise Exception(codecName + " is unsupported codec")
        ratio = round(float(uncompressed/compressed))
        if ratio!=self.compressRatio :
            self.compressRatio = ratio
            self.compressRatioText.setText(str(self.compressRatio))
        return data

    def reshape(self,data,dimArray,step) :
        nz = 1
        ndim = len(dimArray)
        if ndim ==2 :
            nx = dimArray[0]["size"]
            ny = dimArray[1]["size"]
            if step > 0 :
                nx = int(float(nx)/step)
                ny = int(float(ny)/step)
            image = np.reshape(data,(ny,nx))
        elif ndim ==3 :
            if dimArray[0]["size"]==3 :
                nz = dimArray[0]["size"]
                nx = dimArray[1]["size"]
                ny = dimArray[2]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(ny,nx,nz))
            elif dimArray[1]["size"]==3 :
                nz = dimArray[1]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[2]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(ny,nz,nx))
                image = np.swapaxes(image,2,1)
            elif dimArray[2]["size"]==3 :
                nz = dimArray[2]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[1]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(nz,ny,nx))
                image = np.swapaxes(image,0,2)
                image = np.swapaxes(image,0,1)
            else  :  
                raise Exception('no axis has dim = 3')
                return
        else :
                raise Exception('ndim not 2 or 3')
        return (image,nx,ny,nz)        
        
    def dataToImage(self,data,dimArray) :
        ndim = len(dimArray)
        if ndim!=2 and ndim!=3 :
            raise Exception('ndim not 2 or 3')
            return
        nmax = 0
        nz = 0
        nx = 0
        ny = 0
        step = 1
        ndim = len(dimArray)
        if ndim >=2 :
            num = int(dimArray[0]["size"])
            if num>nmax : nmax = num
            num = int(dimArray[1]["size"])
            if num>nmax : nmax = num
            if ndim==3 :
                num = int(dimArray[2]["size"])
                if num>nmax : nmax = num
        if nmax>self.imageSize :
            retval = self.reshape(data,dimArray,1)
            image = retval[0]
            nx = retval[1]
            ny = retval[2]
            nz = retval[3]
            step = math.ceil(float(nmax)/self.imageSize)
            if nz==1 :
                image = image[::step,::step]
            else :
                image =  image[::step,::step,::]  
            data = image.flatten()
        dtype = data.dtype
        dataMin = np.min(data)
        dataMax = np.max(data)
        if self.limitType == 0 :
            if dtype != np.uint8 and dtype != np.uint16 :
                raise Exception('noScale requires uint8 or uint16')
                return
        if self.limitType == 1 :
            displayMin = dataMin
            displayMax = dataMax
            self.limits = (dataMin, dataMax)
        else :
            displayMin = float(self.minLimitText.text())
            displayMax = float(self.maxLimitText.text())
            
        if self.limitType != 0 :
            suppress = self.suppressBackground
            if dtype==np.uint8 or dtype==np.uint8 : suppress = False
            if suppress :
                xp = (displayMax/255,displayMax)
            else :
                xp = (displayMin, displayMax)
            fp = (0.0, 255.0)
            data = (np.interp(data,xp,fp)).astype(np.uint8)
        if self.showLimits :
            self.channelLimitsText.setText(str((dataMin,dataMax)))
            imageMin = np.min(data)
            imageMax = np.max(data)
            self.imageLimitsText.setText(str((imageMin,imageMax))) 
        retval = self.reshape(data,dimArray,step)
        image = retval[0]
        if step==1 : 
            nx = retval[1]
            ny = retval[2]
            nz = retval[3]
        self.imageDict["image"] = image
        if dtype!=self.imageDict["dtypeChannel"] :
            self.imageDict["dtypeChannel"] = dtype
            self.dtypeChannelText.setText(str(self.imageDict["dtypeChannel"]))
        if image.dtype!=self.imageDict["dtypeImage"] :
            self.imageDict["dtypeImage"] = image.dtype
            self.dtypeImageText.setText(str(self.imageDict["dtypeImage"]))
            if image.dtype==np.uint8 :
                self.minLimitText.setText('0')
                self.maxLimitText.setText('255')
            else :
                self.minLimitText.setText('0')
                self.maxLimitText.setText('65535')
        reset = False     
        if nx!=self.imageDict["nx"] :
            self.imageDict["nx"] = nx
            self.nxText.setText(str(self.imageDict["nx"]))
            reset = True
        if ny!=self.imageDict["ny"] :
            self.imageDict["ny"] = ny
            self.nyText.setText(str(self.imageDict["ny"]))
            reset = True
        if nz!=self.imageDict["nz"] :
            self.imageDict["nz"] = nz
            self.nzText.setText(str(self.imageDict["nz"]))
            reset = True
        if reset: self.resetEvent()
        
