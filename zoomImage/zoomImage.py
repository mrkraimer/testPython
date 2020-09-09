#!/usr/bin/env python
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

author Marty Kraimer
    latest date 2020.03.02
    original development started 2019.12
'''


import sys
import time
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget,QRubberBand
from PyQt5.QtWidgets import QLabel,QLineEdit
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtCore import QPoint,QRect,QSize,QPointF
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPainter,QImage
from PyQt5.QtCore import *
import numpy as np
import math

class ZoomImage(QWidget) :
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)
        self.__okToClose = False
        self.__xoffset = 400
        self.__yoffset = 1
        self.channelDict = None
        self.zoomDict = None
        self.mouseDict = None
        self.imgplot = None
        self.showChannel = False

    def setShowChannel(self,value) :
        self.showChannel = value

    def setOrigin(self,y,x) :
        self.__yoffset = y
        self.__xoffset = x
        print(self.__yoffset,self.__xoffset)
        print(type(self.__yoffset),type(self.__xoffset))

    def update(self) :
        print(self.channelDict['image'].shape)
        if type(self.imgplot)!=type(None) : plt.close()
        if self.showChannel :
            image = self.channelDict['channel']
            expand = self.channelDict['compress']
        else :
            image = self.channelDict['image']
            expand = 1
        yoffset = int(self.zoomDict['yoffset']*expand)
        yend = int(self.zoomDict['ny']*expand + yoffset)
        xoffset = int(self.zoomDict['xoffset']*expand)
        xend = int(self.zoomDict['nx']*expand + xoffset)
        nz = self.channelDict['nz']
        if nz==1 :
            image = image[yoffset:yend,xoffset:xend]
        else :
            image = image[yoffset:yend,xoffset:xend,::]
        self.imgplot = plt.imshow(image)
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(self.__xoffset,self.__yoffset,600,600)
        plt.show()
        
    def showChannel(self,value) :
        self.showChannel = value

    def setOkToClose(self) :
        """ allow image window to be closed"""
        self.__okToClose = True

    def closeEvent(self,event) :
        """
        This is a QWidget method.
        It is only present to override until it is okToClose
        """
        if type(self.imgplot)!=type(None) : plt.close()
    def setChannelInfo(self,channelDict) :
        self.channelDict = channelDict

    def setZoomInfo(self,zoomDict,mouseDict) :
        self.zoomDict = zoomDict
        self.mouseDict = mouseDict
        self.update()
