#!/usr/bin/env python
from PyQt5.QtWidgets import QApplication
import numpy as np
from DisplayImage import Viewer
import sys
from pvaccess import Channel

class MandelbrotCreate() :
   def __init__(self,channelName):
       self.channelName = channelName
       self.channel = Channel(self.channelName)
       self.isConnected = False
       self.clientConnectionCallback = None

   def start(self) :
       self.channel.setConnectionCallback(self.connectionCallback)

   def addClientConnectionCallback(self,clientConnectionCallback) :
       print('addClientConnectionCallback')
       self.clientConnectionCallback = clientConnectionCallback
       print('self.clientConnectionCallback=',self.clientConnectionCallback)
       self.clientConnectionCallback.connectionCallback(self.isConnected)
      
   def connectionCallback(self,arg) :
       print('connectionCallback arg=',arg)
       self.isConnected = arg
       if self.clientConnectionCallback!=None : 
           self.clientConnectionCallback.connectionCallback(arg)

   def checkConnected(self) :
       return self.isConnected

   def createImage(self,arg) :
        xmin = arg[0]
        xmax = arg[1]
        ymin = arg[2]
        ymax = arg[3]
        imageSize = arg[4]
        nz = arg[5]
        argxmin = 'argument.xmin=' + str(xmin)
        argxmax = 'argument.xmax=' + str(xmax)
        argymin = 'argument.ymin=' + str(ymin)
        argymax = 'argument.ymax=' + str(ymax)
        argimageSize = 'argument.imageSize=' + str(imageSize)
        argnz = 'argument.nz=' + str(nz)
        args = [argxmin,argxmax,argymin,argymax,argimageSize,argnz]
        result = self.channel.parsePutGet(args,"putField(argument)getField(result)",True)
        val =  result['result.value']
        val = np.array(val,dtype='uint8')
        if nz==3 :
            image = np.reshape(val,(imageSize,imageSize,3))
        else :
            image = np.reshape(val,(imageSize,imageSize))
        return image
        
if __name__ == '__main__':
    app = QApplication(list())
    channelName = "TPYmandelbrotRecord"
    nargs = len(sys.argv)
    if nargs>=2 :
        channelName = sys.argv[1]
    mandelbrotCreate = MandelbrotCreate(channelName)
    viewer = Viewer(mandelbrotCreate)
    mandelbrotCreate.start()
    sys.exit(app.exec_())
