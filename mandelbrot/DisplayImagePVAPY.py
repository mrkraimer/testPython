#!/usr/bin/env python
from PyQt5.QtWidgets import QApplication
import numpy as np
from DisplayImage import Viewer
import sys
from pvaccess import *

class MandelbrotCreate() :
   def __init__(self):
       self.channel = Channel("TPYmandelbrotRecord")
       self.isConnected = False
       self.callClient = False

   def start(self) :
       self.channel.setConnectionCallback(self.connectionCallback)

   def addClientConnectionCallback(self,clientConnectionCallback) :
       print('addClientConnectionCallback')
       self.clientConnectionCallback = clientConnectionCallback
       print('self.clientConnectionCallback=',self.clientConnectionCallback)
       self.clientConnectionCallback.connectionCallback(self.isConnected)
       self.callClient = True
      
   def connectionCallback(self,arg) :
       print('connectionCallback arg=',arg)
       self.isConnected = arg
       if self.callClient : self.clientConnectionCallback.connectionCallback(arg)

   def checkConnected(self) :
       return self.isConnected

   def createImage(self,arg) :
        xmin = arg[0]
        xinc = arg[1]
        ymin = arg[2]
        yinc = arg[3]
        width = arg[4]
        height =arg[5]
        nz = arg[6]
        chan = Channel("TPYmandelbrotRecord")
        argxmin = 'argument.xmin=' + str(xmin)
        argxinc = 'argument.xinc=' + str(xinc)
        argymin = 'argument.ymin=' + str(ymin)
        argyinc = 'argument.yinc=' + str(yinc)
        argwidth = 'argument.width=' + str(width)
        argheight = 'argument.height=' + str(height)
        argnz = 'argument.nz=' + str(nz)
        args = [argxmin,argxinc,argymin,argyinc,argwidth,argheight,argnz]
        result = chan.parsePutGet(args,"putField(argument)getField(result)",True)
        val =  result['result.value']
        if nz==3 :
            image = np.reshape(val,(height,width,3))
            image = np.transpose(image,(1,0,2))
        else :
            image = np.reshape(val,(height,width))
            image = np.transpose(image,(1,0))
        return image
        
if __name__ == '__main__':
    app = QApplication(list())
    mandelbrotCreate = MandelbrotCreate()
    viewer = Viewer(mandelbrotCreate)
    mandelbrotCreate.start()
    sys.exit(app.exec_())
