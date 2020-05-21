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
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QSlider
from PyQt5.QtWidgets import QPushButton,QHBoxLayout,QGridLayout
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtCore import *

sys.path.append('../numpyImage/')
from numpyImage import NumpyImage

import ctypes
import ctypes.util
import os
import math

class NTNDA_Channel_Provider(object) :
    '''
    Base class for monitoring an NTNDArray channel from an areaDetector IOC.
    The methods are called by NTNDA_Viewer.
    '''

    def __init__(self) :
        self.channelName = None
    def setChannelName(self,channelName) :
        self.channelName = channelName
    def getChannelName(self) :
        return self.channelName
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


def imageDictCreate() :
    return {"image" : None , "dtype" : "" , "nx" : 0 , "ny" : 0 ,  "nz" : 0 }

class ImageControl(QWidget) :

    def __init__(self,statusText,parent=None, **kargs):
        super(QWidget, self).__init__(parent)
        self.isClosed = False
        self.statusText = statusText
        self.imageDisplay = NumpyImage(windowTitle='2d plot',flipy=False,maxsize=800)
        self.imageDisplay.setZoomCallback(self.zoomEvent)
        self.imageDict = imageDictCreate()
        self.pixelLevels = (int(0),int(255))
        self.npixelLevels = 255
        self.minimum = 0;
        self.low = 0
        self.high = self.npixelLevels
        self.maximum = self.npixelLevels
# first row
        minimumLabel = QLabel("minimum")
        minimumLabel.setFixedWidth(100)
        lowLabel = QLabel("low")
        lowLabel.setFixedWidth(90)
        titleLabel = QLabel("pixel intensity")
        titleLabel.setFixedWidth(110)
        highLabel = QLabel("high")
        highLabel.setFixedWidth(100)
        maximumLabel = QLabel("maximum")
        maximumLabel.setFixedWidth(80)
        zoomLabel = QLabel('||    zoom        (xmin,xmax,ymin,ymax)')
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(minimumLabel)
        box.addWidget(lowLabel);
        box.addWidget(titleLabel);
        box.addWidget(highLabel);
        box.addWidget(maximumLabel)
        box.addWidget(zoomLabel)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
#second row
        self.minimumText = QLineEdit()
        self.minimumText.setText('')
        self.minimumText.setEnabled(True)
        self.minimumText.setFixedWidth(100)
        self.minimumText.editingFinished.connect(self.minimumEvent)
        self.lowText = QLabel('')
        self.lowText.setFixedWidth(100)
        spaceLabel = QLabel('')
        spaceLabel.setFixedWidth(100)
        self.highText = QLabel('')
        self.highText.setFixedWidth(100)
        self.maximumText = QLineEdit()
        self.maximumText.setFixedWidth(80)
        self.maximumText.editingFinished.connect(self.maximumEvent)
        self.maximumText.setEnabled(True)
        self.maximumText.setText('')
        dividerLabel = QLabel('||')
        dividerLabel.setFixedWidth(20)
        self.resetButton = QPushButton('reset')
        self.resetButton.setFixedWidth(40)
        self.resetButton.setEnabled(True)
        self.resetButton.clicked.connect(self.resetEvent)
        self.zoomText =  QLabel('')
        self.zoomText.setFixedWidth(220)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(self.minimumText)
        box.addWidget(self.lowText)
        box.addWidget(spaceLabel)
        box.addWidget(self.highText)
        box.addWidget(self.maximumText)
        box.addWidget(dividerLabel)
        box.addWidget(self.resetButton)
        box.addWidget(self.zoomText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
#third row
        self.lowSlider = QSlider(Qt.Horizontal)
        self.lowSlider.setContentsMargins(0,0,0,0);
        self.lowSlider.setMinimum(0)
        self.lowSlider.setMaximum(self.npixelLevels)
        self.lowSlider.setValue(0)
        self.lowSlider.setTickPosition(QSlider.TicksBelow)
        self.lowSlider.setTickInterval(10)
        self.lowSlider.setFixedWidth(256)
        self.highSlider = QSlider(Qt.Horizontal)
        self.highSlider.setContentsMargins(0,0,0,0);
        self.highSlider.setMinimum(0)
        self.highSlider.setMaximum(self.npixelLevels)
        self.highSlider.setValue(self.npixelLevels)
        self.highSlider.setTickPosition(QSlider.TicksBelow)
        self.highSlider.setTickInterval(10)
        self.highSlider.setFixedWidth(256)
        box = QHBoxLayout()
        box.addStretch(0)
        box.setSpacing(0);
        box.setContentsMargins(0,0,0,0);
        box.setGeometry(QRect(0, 0, 500, 20))
        box.addWidget(self.lowSlider)
        box.addWidget(self.highSlider)
        wid =  QWidget()
        wid.setLayout(box)
        self.thirdRow = wid
#create window
        layout = QGridLayout()
        layout.setSpacing(0);
        layout.addWidget(self.firstRow,0,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.secondRow,1,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.thirdRow,2,0,alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.lowSlider.valueChanged.connect(self.lowSliderValueChange)
        self.highSlider.valueChanged.connect(self.highSliderValueChange)
        self.show()

    def resetEvent(self) :
        print('resetEvent 1')
        if self.imageDict['nx']==0 : return
        print('resetEvent 2')
        self.zoomText.setText('')
        self.imageDisplay.resetZoom()
        print('resetEvent 3')
        self.display()

    def zoomEvent(self,zoomData) :
        self.zoomText.setText(str(zoomData))
        self.display()

    def minimumEvent(self) :
        try:
            minimum = float(self.minimumText.text())
            if minimum>self.maximum :
                minimum = self.maximum
                self.minimumText.setText(str(minimum))
            self.minimum = minimum
            self.low = minimum
            self.lowText.setText(str(self.low))
            self.pixelLevels = (self.low,self.high)
            self.lowSlider.setValue(0)
            self.imageDisplay.display(self.imageDict["image"],pixelLevels=self.pixelLevels)
        except Exception as error:
            self.minimumText.setText(str(error))

    def maximumEvent(self) :
        try:
            maximum = float(self.maximumText.text())
            if maximum<self.minimum :
                maximum = self.minimum
                self.maximumText.setText(str(maximum))
            self.maximum = maximum
            self.high = maximum
            self.highText.setText(str(self.high))
            self.pixelLevels = (self.low,self.high)
            self.highSlider.setValue(self.npixelLevels)
            self.imageDisplay.display(self.imageDict["image"],pixelLevels=self.pixelLevels)
        except Exception as error:
            self.maximumText.setText(str(error))

    def lowSliderValueChange(self) :
        pixelRatio = float(self.lowSlider.value())/float(self.npixelLevels)
        valueRange = float(self.maximum) - float(self.minimum)
        value = pixelRatio*valueRange + self.minimum
        if value>self.maximum : value = self.maximum
        if value>self.high :
            self.high = value
            self.highText.setText(str(round(self.high)))
            self.highSlider.setValue(self.high)
        self.low= value
        self.lowText.setText(str(round(self.low)))
        self.pixelLevels = (self.low,self.high)
        self.imageDisplay.display(self.imageDict["image"],pixelLevels=self.pixelLevels)
        
    def highSliderValueChange(self) :
        pixelRatio = float(self.highSlider.value())/float(self.npixelLevels)
        valueRange = float(self.maximum) - float(self.minimum)
        value = pixelRatio*valueRange + self.minimum
        if value<self.minimum : value = self.minimum
        if value<self.low :
            self.low = value
            self.lowText.setText(str(round(self.low)))
            self.lowSlider.setValue(self.low)
        self.high = value
        self.highText.setText(str(round(self.high)))
        self.pixelLevels = (self.low,self.high)
        self.imageDisplay.display(self.imageDict["image"],pixelLevels=self.pixelLevels)

    def newImage(self,imageDict):
        if self.isClosed : return
        self.imageDict["image"] = imageDict["image"]
        self.imageDict["nx"] = imageDict["nx"]
        self.imageDict["ny"] = imageDict["ny"]
        self.imageDict["nz"] = imageDict["nz"]
        if not str(imageDict["dtype"])==str(self.imageDict["dtype"]) :
            self.imageDict["dtype"] = imageDict["dtype"]
            dtype = self.imageDict["dtype"]
            if dtype==str("int8") :
                self.pixelLevels = (int(-128),int(127))
            elif dtype==str("uint8") :
                self.pixelLevels = (int(0),int(255))
            elif dtype==str("int16") :
                self.pixelLevels = (int(-32768),int(32767))
            elif dtype==str("uint16") :
                self.pixelLevels = (int(0),int(65536))
            elif dtype==str("int32") :
                self.pixelLevels = (int(-2147483648),int(2147483647))
            elif dtype==str("uint32") :
                self.pixelLevels = (int(0),int(4294967296))
            elif dtype==str("int64") :
                self.pixelLevels = (int(-9223372036854775808),int(9223372036854775807))
            elif dtype==str("uint64") :
                self.pixelLevels = (int(0),int(18446744073709551615))
            elif dtype==str("float32") :
                self.pixelLevels = (float(0.0),float(1.0))
            elif dtype==str("float64") :
                self.pixelLevels = (float(0.0),float(1.0))
            else :
                raise Exception('unknown dtype' + dtype)
                return
            self.minimum = self.pixelLevels[0]
            self.minimumText.setText(str(self.minimum))
            self.low = self.minimum
            self.lowText.setText(str(self.low))
            self.maximum  = self.pixelLevels[1]
            self.maximumText.setText(str(self.maximum))
            self.high = self.maximum
            self.highText.setText(str(self.high))
            self.lowSlider.setValue(0)
            self.highSlider.setValue(self.npixelLevels)

    def display(self) :
        if self.isClosed : return
        self.imageDisplay.display(self.imageDict["image"],pixelLevels=self.pixelLevels)
        self.imageDisplay.show()
          
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
        self.isClosed = False
        self.provider = ntnda_Channel_Provider
        self.provider.NTNDA_Viewer = self
        self.setWindowTitle(providerName + "_NTNDA_Viewer")
        self.imageDict = imageDictCreate()
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
        if len(self.provider.getChannelName())<1 :
            name = os.getenv('EPICS_NTNDA_VIEWER_CHANNELNAME')
            if name!= None : self.provider.setChannelName(name)
        self.nImages = 0
        self.imageRateText = QLabel()
        self.imageRateText.setFixedWidth(40)
        self.channelNameLabel = QLabel("channelName:")
        self.channelNameText = QLineEdit()
        self.channelNameText.setEnabled(True)
        self.channelNameText.setText(self.provider.getChannelName())
        self.channelNameText.editingFinished.connect(self.channelNameEvent)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(self.startButton)
        box.addWidget(self.stopButton)
        imageRateLabel = QLabel("imageRate:")
        box.addWidget(imageRateLabel)
        box.addWidget(self.imageRateText)
        box.addWidget(self.channelNameLabel)
        box.addWidget(self.channelNameText)
        wid =  QWidget()
        wid.setLayout(box)
        self.firstRow = wid
# second row
        self.nxText = QLabel()
        self.nxText.setFixedWidth(50)
        self.nyText = QLabel()
        self.nyText.setFixedWidth(50)
        self.nzText = QLabel()
        self.nzText.setFixedWidth(20)
        self.dtype = None
        self.dtypeText = QLabel()
        self.dtypeText.setFixedWidth(50)
        self.codecName = ''
        self.codecNameText = QLabel()
        self.codecNameText.setFixedWidth(40)

        self.compressRatioText = QLabel()
        self.compressRatioText.setFixedWidth(40)
        self.compressRatio = round(1.0)
        self.compressRatioText.setText(str(self.compressRatio))
        self.clearButton = QPushButton('clear')
        self.clearButton.setEnabled(True)
        self.clearButton.clicked.connect(self.clearEvent)
        self.clearButton.setFixedWidth(40)
        self.statusText = QLineEdit()
        self.statusText.setText('nothing done so far')
        self.statusText.setFixedWidth(200)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        nxLabel = QLabel("nx:")
        nxLabel.setFixedWidth(20)
        self.nxText.setText('0')
        box.addWidget(nxLabel)
        box.addWidget(self.nxText)
        nyLabel = QLabel("ny:")
        nyLabel.setFixedWidth(20)
        self.nyText.setText('0')
        box.addWidget(nyLabel)
        box.addWidget(self.nyText)
        nzLabel = QLabel("nz:")
        nzLabel.setFixedWidth(20)
        self.nzText.setText('0')
        box.addWidget(nzLabel)
        box.addWidget(self.nzText)
        dtypeLabel = QLabel("dtype:")
        box.addWidget(dtypeLabel)
        box.addWidget(self.dtypeText)
        codecNameLabel = QLabel("codec:")
        box.addWidget(codecNameLabel)
        box.addWidget(self.codecNameText)
        self.codecNameText.setText("none")
        compressRatioLabel = QLabel("compressRatio:")
        box.addWidget(compressRatioLabel)
        box.addWidget(self.compressRatioText)
        box.addWidget(self.clearButton)
        statusLabel = QLabel("  status:")
        statusLabel.setFixedWidth(50)
        box.addWidget(statusLabel)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
# third row
        self.imageControl = ImageControl(self.statusText)
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0);
        box.addWidget(self.imageControl)
        wid =  QWidget()
        wid.setLayout(box)
        self.thirdRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0)
        layout.addWidget(self.secondRow,1,0)
        layout.addWidget(self.thirdRow,2,0)
        self.setLayout(layout)
        self.findLibrary = FindLibrary()
        self.subscription = None
        self.lasttime = time.time() -2
        self.arg = None
        self.show()
        self.imageControl.show()

    def closeEvent(self, event) :
        if self.isStarted : self.stop()
        self.isClosed = True
        self.imageControl.isClosed = True
        self.provider.done()
        self.imageControl.imageDisplay.okToClose = True
        self.imageControl.imageDisplay.close()

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
        self.channelNameText.setEnabled(False)
        self.isStarted = True
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
        self.isStarted = False

    def callback(self,arg):
        if self.isClosed : return
        if len(arg)==1 :
            value = arg.get("exception")
            if value!=None :
                self.statusText.setText(str(error))
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
            self.imageDict["dtype"] = data.dtype
            self.dtypeText.setText(str(self.imageDict["dtype"]))
        try:
            if codecNameLength != 0 : 
                data = self.decompress(data,codec,compressed,uncompressed)
            self.dataToImage(data,dimArray)
            self.imageControl.newImage(self.imageDict)
            self.imageControl.display()
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
        self.imageDict["dtype"] = dtype
        self.dtypeText.setText(str(self.imageDict["dtype"]))
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

    def dataToImage(self,data,dimArray) :
        ny = 0
        nx = 0
        nz = 1
        dtype = data.dtype
        ndim = len(dimArray)
        if ndim!=2 and ndim!=3 :
            raise Exception('ndim not 2 or 3')
            return
        if ndim ==2 :
            nx = dimArray[0]["size"]
            ny = dimArray[1]["size"]
            image = np.reshape(data,(ny,nx))
        elif ndim ==3 :
            if dimArray[0]["size"]==3 :
                nz = dimArray[0]["size"]
                nx = dimArray[1]["size"]
                ny = dimArray[2]["size"]
                image = np.reshape(data,(ny,nx,nz))
            elif dimArray[1]["size"]==3 :
                nz = dimArray[1]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[2]["size"]
                image = np.reshape(data,(ny,nz,nx))
                image = np.swapaxes(image,2,1)
            elif dimArray[2]["size"]==3 :
                nz = dimArray[2]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[1]["size"]
                image = np.reshape(data,(nz,ny,nx))
                image = np.swapaxes(image,0,2)
                image = np.swapaxes(image,0,1)
            else  :  
                raise Exception('no axis has dim = 3')
                return
        else :
                raise Exception('ndim not 2 or 3')
                
        if dtype!=self.imageDict["dtype"] :
            self.imageDict["dtype"] = dtype
            self.dtypeText.setText(str(self.imageDict["dtype"]))
        if nx!=self.imageDict["nx"] :
            self.imageDict["nx"] = nx
            self.nxText.setText(str(self.imageDict["nx"]))
        if ny!=self.imageDict["ny"] :
            self.imageDict["ny"] = ny
            self.nyText.setText(str(self.imageDict["ny"]))
        if nz!=self.imageDict["nz"] :
            self.imageDict["nz"] = nz
            self.nzText.setText(str(self.imageDict["nz"]))
        self.imageDict["image"] = image

