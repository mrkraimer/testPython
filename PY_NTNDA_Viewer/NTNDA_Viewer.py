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
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import *

sys.path.append('../numpyImage/')
from numpyImage import NumpyImage

import ctypes
import ctypes.util
import os
import math

def imageDictCreate() :
    return {"image" : None , "dtype" : "" , "nx" : 0 , "ny" : 0 ,  "nz" : 0 }


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
        self.imageDisplay = NumpyImage(windowTitle='image',flipy=False,maxsize=800)
        self.imageDisplay.setZoomCallback(self.zoomEvent)
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
           
        self.nImages = 0
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
        self.dtype = None
        dtypeLabel = QLabel('dtype: ')
        box.addWidget(dtypeLabel)
        self.dtypeText = QLabel('      ')
        box.addWidget(self.dtypeText)
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
        self.statusText.setFixedWidth(400)
        box.addWidget(self.statusText)
        wid =  QWidget()
        wid.setLayout(box)
        self.secondRow = wid
# third row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        zoomLabel = QLabel('zoom ')
        box.addWidget(zoomLabel)
        self.resetButton = QPushButton('reset')
        box.addWidget(self.resetButton)
        self.resetButton.setEnabled(True)
        self.resetButton.clicked.connect(self.resetEvent)
        zoomCordLabel = QLabel(' (xmin,xmax,ymin,ymax) = ')
        box.addWidget(zoomCordLabel)
        self.zoomText =  QLabel('')
        self.zoomText.setFixedWidth(600)
        box.addWidget(self.zoomText,alignment=Qt.AlignLeft)
        wid =  QWidget()
        wid.setLayout(box)
        self.thirdRow = wid
#fourth row
        box = QHBoxLayout()
        box.setContentsMargins(0,0,0,0)
        dataMinLabel = QLabel('dataMin: ')
        box.addWidget(dataMinLabel)
        self.dataMinText = QLabel('          ')
        self.dataMinText.setFixedWidth(100)
        box.addWidget(self.dataMinText)
        dataMaxLabel = QLabel('dataMax: ')
        box.addWidget(dataMaxLabel)
        self.dataMaxText = QLabel('          ')
        self.dataMaxText.setFixedWidth(100)
        box.addWidget(self.dataMaxText)
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

    def zoomEvent(self,zoomData) :
        self.zoomText.setText(str(zoomData))
        self.display()

    def newImage(self,imageDict):
        if self.isClosed : return
        self.imageDict["image"] = imageDict["image"]
        self.imageDict["nx"] = imageDict["nx"]
        self.imageDict["ny"] = imageDict["ny"]
        self.imageDict["nz"] = imageDict["nz"]
        if not str(imageDict["dtype"])==str(self.imageDict["dtype"]) :
            self.imageDict["dtype"] = imageDict["dtype"]
            dtype = self.imageDict["dtype"]
            
    def display(self) :
        if self.isClosed : return
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
        

    def callback(self,arg):
        if self.isClosed : return
        if not self.isStarted : return
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
            self.newImage(self.imageDict)
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
        ndim = len(dimArray)
        if ndim!=2 and ndim!=3 :
            raise Exception('ndim not 2 or 3')
            return
        dtype = data.dtype
        if dtype==np.uint8 :
            pass
        elif dtype==np.int8 :
            data = data.astype(np.uint8) 
        elif dtype==np.uint16 :
            if ndim==2 :
                pass
            else :
                data = data.astype(np.uint8)
        elif dtype==np.int16 :
            if ndim==2 :
                data = data.astype(np.uint16)
            else :
                data = data.astype(np.uint8)
        else :
            data=data.astype(np.uint8) 
        dataMin = int(np.min(data))
        dataMax = int(np.max(data))
        self.dataMinText.setText(str(dataMin))
        self.dataMaxText.setText(str(dataMax))
        QApplication.processEvents()
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

