#!/usr/bin/env python
"""
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

author Marty Kraimer
    latest date 2020.03.02
    original development started 2019.12
"""


import sys
import time
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget, QRubberBand
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QPoint, QRect, QSize, QPointF
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import *
import numpy as np
import math


class ZoomImage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.__xoffset = 400
        self.__yoffset = 1
        self.channelDict = None
        self.zoomDict = None
        self.mouseDict = None
        self.imgplot = None
        self.showChannel = False

    def setShowChannel(self, value):
        self.showChannel = value

    def setOrigin(self, y, x):
        self.__yoffset = y
        self.__xoffset = x

    def update(self):
        point = plt.get_current_fig_manager().window.geometry().topLeft()
        if not point.isNull():
            self.__xoffset = point.x()
            self.__yoffset = point.y()
            plt.close()
        if self.showChannel:
            image = self.channelDict["channel"]
            expand = self.channelDict["compress"]
        else:
            image = self.channelDict["image"]
            expand = 1
        yoffset = int(self.zoomDict["yoffset"] * expand)
        yend = int(self.zoomDict["ny"] * expand + yoffset)
        xoffset = int(self.zoomDict["xoffset"] * expand)
        xend = int(self.zoomDict["nx"] * expand + xoffset)
        nz = self.channelDict["nz"]
        if nz == 1:
            image = image[yoffset:yend, xoffset:xend]
        else:
            image = image[yoffset:yend, xoffset:xend, ::]
        self.imgplot = plt.imshow(image)
        plt.get_current_fig_manager().window.setGeometry(
            self.__xoffset, self.__yoffset, 600, 600
        )
        plt.show()

    def showChannel(self, value):
        self.showChannel = value

    def closeEvent(self, event):
        """
        This is a QWidget method.

        """
        point = plt.get_current_fig_manager().window.geometry().topLeft()
        if not point.isNull():
            plt.close()

    def setChannelInfo(self, channelDict):
        self.channelDict = channelDict

    def setZoomInfo(self, zoomDict, mouseDict):
        self.zoomDict = zoomDict
        self.mouseDict = mouseDict
        self.update()
