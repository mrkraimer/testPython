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
       self.clientConnectionCallback = clientConnectionCallback
       self.clientConnectionCallback.connectionCallback(self.isConnected)
      
   def connectionCallback(self,arg) :
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
        nx =  arg[4]
        ny =  arg[5]
        nz = arg[6]
        expz = arg[7]
        argxmin = 'argument.xmin=' + str(xmin)
        argxmax = 'argument.xmax=' + str(xmax)
        argymin = 'argument.ymin=' + str(ymin)
        argymax = 'argument.ymax=' + str(ymax)
        argnx = 'argument.nx=' + str(nx)
        argny = 'argument.ny=' + str(ny)
        argnz = 'argument.nz=' + str(nz)
        argexpz = 'argument.expz=' + str(expz)
        args = [argxmin,argxmax,argymin,argymax,argnx,argny,argnz,argexpz]
        result = self.channel.parsePutGet(args,"putField(argument)getField(result)",True)
        val =  result['result.value']
        val = np.array(val,dtype='uint8')
        if nz==3 :
            image = np.reshape(val,(ny,nx,3))
        else :
            image = np.reshape(val,(ny,nx))
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
