# showInfo.py

from PyQt5.QtWidgets import QWidget,QRubberBand
from PyQt5.QtWidgets import QLabel,QLabel
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPainter,QImage
from PyQt5.QtCore import *
import numpy as np
import math


class ShowInfo(QWidget) :
    '''

Normal use is:
...
from showInfo import ShowInfo
...
    self.showInfo = ShowInfo()
    self.imageDict = self.dataToImage.imageDictCreate()
    
...
    try:
        self.dataToImage.dataToImage(data,dimArray,self.imageSize,...)
        imageDict = self.dataToImage.getImageDict()
        self.imageDict["image"] = imageDict["image"]
        ... other methods
...   
     
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
latest date 2020.08.10
    '''
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
        self.__okToClose = False
        self.__isHidden = True
        self.__xoffset = None
        self.__yoffset = None
        

        masterbox = QVBoxLayout()

        channelbox = QVBoxLayout()
        channelbox.setContentsMargins(0,0,0,0)
        channelbox.addWidget(QLabel("ChannelInfo"))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("nx: "))
        self.channelnxText = QLabel()
        self.channelnxText.setFixedWidth(40)
        hbox.addWidget(self.channelnxText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("ny: "))
        self.channelnyText = QLabel()
        self.channelnyText.setFixedWidth(40)
        hbox.addWidget(self.channelnyText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("nz: "))
        self.channelnzText = QLabel()
        self.channelnzText.setFixedWidth(40)
        hbox.addWidget(self.channelnzText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)        

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("dtype: "))
        self.channeldtypeText = QLabel()
        self.channeldtypeText.setFixedWidth(60)
        hbox.addWidget(self.channeldtypeText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("compress: "))
        self.channelcompressText = QLabel()
        self.channelcompressText.setFixedWidth(40)
        hbox.addWidget(self.channelcompressText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)
        channelbox.addWidget(QLabel("updates on mouseClick"))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("mouseX: "))
        self.channelmouseXText = QLabel()
        self.channelmouseXText.setFixedWidth(60)
        hbox.addWidget(self.channelmouseXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("mouseY: "))
        self.channelmouseYText = QLabel()
        self.channelmouseYText.setFixedWidth(60)
        hbox.addWidget(self.channelmouseYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("x: "))
        self.channelXText = QLabel()
        self.channelXText.setFixedWidth(60)
        hbox.addWidget(self.channelXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("y: "))
        self.channelYText = QLabel()
        self.channelYText.setFixedWidth(60)
        hbox.addWidget(self.channelYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        wid =  QWidget()
        wid.setLayout(channelbox)
        masterbox.addWidget(wid)

        imagebox = QVBoxLayout()
        imagebox.setContentsMargins(0,10,0,0)
        imagebox.addWidget(QLabel("ImageInfo"))
        imagebox.addWidget(QLabel("updates on mouseClick"))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("width: "))
        self.imagewidthText = QLabel()
        self.imagewidthText.setFixedWidth(40)
        hbox.addWidget(self.imagewidthText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("height: "))
        self.imageheightText = QLabel()
        self.imageheightText.setFixedWidth(40)
        hbox.addWidget(self.imageheightText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("dtype: "))
        self.imagedtypeText = QLabel()
        self.imagedtypeText.setFixedWidth(40)
        hbox.addWidget(self.imagedtypeText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)


        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("expand: "))
        self.imagecompressText = QLabel()
        self.imagecompressText.setFixedWidth(40)
        hbox.addWidget(self.imagecompressText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)        

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("mouseX: "))
        self.imagemouseXText = QLabel()
        self.imagemouseXText.setFixedWidth(40)
        hbox.addWidget(self.imagemouseXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("mouseY: "))
        self.imagemouseYText = QLabel()
        self.imagemouseYText.setFixedWidth(40)
        hbox.addWidget(self.imagemouseYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)


        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("x: "))
        self.imageXText = QLabel()
        self.imageXText.setFixedWidth(60)
        hbox.addWidget(self.imageXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("y: "))
        self.imageYText = QLabel()
        self.imageYText.setFixedWidth(60)
        hbox.addWidget(self.imageYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)        

        wid =  QWidget()
        wid.setLayout(imagebox)
        masterbox.addWidget(wid)

        wid =  QWidget()
        wid.setLayout(masterbox)
        self.firstRow = wid
# initialize
        layout = QGridLayout()
        layout.setVerticalSpacing(0);
        layout.addWidget(self.firstRow,0,0,alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.setFixedHeight(self.height())
        self.setFixedWidth(200)

    def setOkToClose(self) :
        """ allow image window to be closed"""
        self.__okToClose = True

    def closeEvent(self,event) :
        """
        This is a QWidget method.
        It is only present to override until it is okToClose
        """
        if not self.__okToClose :
            point = self.geometry().topLeft()
            self.__xoffset = point.x()
            self.__yoffset = point.y()
            self.setGeometry(self.__xoffset,self.__yoffset,self.width(),self.height())
            self.hide()
            self.__isHidden = True
            return

    def setChannelInfo(self,channelDict) :
        self.channelnxText.setText(str(channelDict["nx"]))
        self.channelnyText.setText(str(channelDict["ny"]))
        self.channelnzText.setText(str(channelDict["nz"]))
        self.channeldtypeText.setText(str(channelDict["dtypeChannel"]))
        self.channelcompressText.setText(str(channelDict["compress"]))

    def setImageInfo(self,imageDict) :
        self.imagewidthText.setText(str(imageDict["width"]))
        self.imageheightText.setText(str(imageDict["height"]))
        self.imagedtypeText.setText(str(imageDict["dtype"]))
        self.imagemouseXText.setText(str(imageDict["mouseX"]))
        self.imagemouseYText.setText(str(imageDict["mouseY"]))
        image = imageDict["image"]
        print('must calc mouse position')
            
        
