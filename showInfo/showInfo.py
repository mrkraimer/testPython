# showInfo.py

from PyQt5.QtWidgets import QWidget,QRubberBand
from PyQt5.QtWidgets import QLabel,QLineEdit
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
...
    
...   
     
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
latest date 2020.08.20
    '''
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
        self.__okToClose = False
        self.__isHidden = True
        self.__xoffset = None
        self.__yoffset = None

        masterbox = QVBoxLayout()
        masterbox.setContentsMargins(0,0,0,0)
        self.infoText = QLabel('status')
        masterbox.addWidget(self.infoText)

        channelbox = QVBoxLayout()
        channelbox.setContentsMargins(0,0,0,0)
        channelbox.addWidget(QLabel("ChannelInfo"))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("nx: "))
        self.channelnxText = QLabel('----')
        hbox.addWidget(self.channelnxText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("ny: "))
        self.channelnyText = QLabel('----')
        hbox.addWidget(self.channelnyText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("nz: "))
        self.channelnzText = QLabel('--')
        hbox.addWidget(self.channelnzText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("dtype: "))
        self.channeldtypeText = QLabel('--------')
        hbox.addWidget(self.channeldtypeText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("compress: "))
        self.channelcompressText = QLabel('----')
        hbox.addWidget(self.channelcompressText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        channelbox.addWidget(QLabel("mouseClick"))

        channelbox.addWidget(QLabel('channelLow'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.channellowText = QLabel("-------------")
        hbox.addWidget(self.channellowText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        channelbox.addWidget(QLabel('channelHigh'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.channelhighText = QLabel("-------------")
        hbox.addWidget(self.channelhighText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("x: "))
        self.channelmouseXText = QLabel('----')
        hbox.addWidget(self.channelmouseXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("y: "))
        self.channelmouseYText = QLabel('----')
        hbox.addWidget(self.channelmouseYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        channelbox.addWidget(QLabel('value'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.channelvalue1Text = QLabel("(-------------")
        hbox.addWidget(self.channelvalue1Text)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.channelvalue2Text = QLabel(",-------------")
        hbox.addWidget(self.channelvalue2Text)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.channelvalue3Text = QLabel(",-------------)")
        hbox.addWidget(self.channelvalue3Text)
        wid =  QWidget()
        wid.setLayout(hbox)
        channelbox.addWidget(wid)

        wid =  QWidget()
        wid.setLayout(channelbox)
        masterbox.addWidget(wid)

        imagebox = QVBoxLayout()
        imagebox.setContentsMargins(0,10,0,0)
        imagebox.addWidget(QLabel("ImageInfo"))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("width: "))
        self.imagewidthText = QLabel('----')
        hbox.addWidget(self.imagewidthText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("height: "))
        self.imageheightText = QLabel('----')
        hbox.addWidget(self.imageheightText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("dtype: "))
        self.imagedtypeText = QLabel('---------')
        hbox.addWidget(self.imagedtypeText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        imagebox.addWidget(QLabel("mouseClick"))

        imagebox.addWidget(QLabel('imageLow'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.imagelowText = QLabel("---")
        hbox.addWidget(self.imagelowText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        imagebox.addWidget(QLabel('imageHigh'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.imagehighText = QLabel("---")
        hbox.addWidget(self.imagehighText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("x: "))
        self.imagemouseXText = QLabel('----')
        hbox.addWidget(self.imagemouseXText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        hbox.addWidget(QLabel("y: "))
        self.imagemouseYText = QLabel('----')
        hbox.addWidget(self.imagemouseYText)
        wid =  QWidget()
        wid.setLayout(hbox)
        imagebox.addWidget(wid)

        imagebox.addWidget(QLabel('value'))
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10,0,0,0)
        self.imagevalueText = QLabel("(---.---.---)")
        hbox.addWidget(self.imagevalueText)
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
        height = self.height()
        self.setFixedHeight(height+170)
        self.setFixedWidth(320)

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
        self.channel = channelDict["channel"]
        self.image = channelDict["image"]
        self.nx = channelDict["nx"]
        self.ny = channelDict["ny"]
        self.nz = channelDict["nz"]
        self.compress = float(channelDict["compress"])
        self.channelnxText.setText(str(self.nx))
        self.channelnyText.setText(str(self.ny))
        self.channelnzText.setText(str(self.nz))
        self.channeldtypeText.setText(str(channelDict["dtypeChannel"]))
        self.channelcompressText.setText(str(self.compress))
        height = self.image.shape[0]
        width = self.image.shape[1]
        self.imagewidthText.setText(str(width))
        self.imageheightText.setText(str(height))
        self.imagedtypeText.setText(str(self.image.dtype))

    def setImageInfo(self,zoomDict,mouseDict) :
        self.__resetInfo()
        imageMin = np.min(self.image)
        imageMax = np.max(self.image)
        self.imagelowText.setText(str(imageMin))
        self.imagehighText.setText(str(imageMax))
        channelMin = np.min(self.channel)
        channelMax = np.max(self.channel)
        self.channellowText.setText(str(channelMin))
        self.channelhighText.setText(str(channelMax))
        mouseX = int(mouseDict["mouseX"])
        mouseY = int(mouseDict["mouseY"])
        self.imagemouseXText.setText(str(mouseX))
        self.imagemouseYText.setText(str(mouseY))
        mouseXchannel = int(mouseX*self.compress)
        mouseYchannel = int(mouseY*self.compress)
        self.channelmouseXText.setText(str(mouseXchannel))
        self.channelmouseYText.setText(str(mouseYchannel))
        if mouseXchannel>self.nx :
            self.__setInfo('mouseX out of bounds')
            return
        if mouseYchannel>self.ny :
            self.__setInfo('mouseY out of bounds')
            return   
        if self.nz==1 :
            value = self.image[mouseY,mouseX]
            self.imagevalueText.setText(str(value))
            value = self.channel[mouseYchannel,mouseXchannel]
            self.channelvalue1Text.setText(str(value))
            self.channelvalue2Text.setText("")
            self.channelvalue3Text.setText("")
        elif self.nz==3 :
            value1 = self.image[mouseY,mouseX,0]
            value2 = self.image[mouseY,mouseX,1]
            value3 = self.image[mouseY,mouseX,2]
            value = "[" + str(value1) + "," + str(value2) + "," + str(value3) + "]"
            self.imagevalueText.setText(str(value))
            value1 = self.channel[mouseYchannel,mouseXchannel,0]
            value2 = self.channel[mouseYchannel,mouseXchannel,1]
            value3 = self.channel[mouseYchannel,mouseXchannel,2]
            self.channelvalue1Text.setText("[ " +str(value1))
            self.channelvalue2Text.setText(", " +str(value2))
            self.channelvalue3Text.setText(", " +str(value3) + " ]")
            
        else :
            self.infoText.setText('nz must be 1 or 3')

    def __resetInfo(self) :
        self.infoText.setStyleSheet("background-color:green")
        self.infoText.setText('mouseClicked')

    def __setInfo(self,value) :
        self.infoText.setStyleSheet("background-color:red")
        self.infoText.setText(str(value))
      
