from PyQt5.QtWidgets import QApplication
import numpy as np
from DisplayImage import Viewer
import sys
from pvaccess import *

class MandelbrotCreate :
   def createImage(self,arg) :
        xmin = arg[0]
        xinc = arg[1]
        ymin = arg[2]
        yinc = arg[3]
        width = arg[4]
        height =arg[5]
        chan = Channel("TPYmandelbrotRecord")
        argxmin = 'argument.xmin=' + str(xmin)
        argxinc = 'argument.xinc=' + str(xinc)
        argymin = 'argument.ymin=' + str(ymin)
        argyinc = 'argument.yinc=' + str(yinc)
        argwidth = 'argument.width=' + str(width)
        argheight = 'argument.height=' + str(height)
        args = [argxmin,argxinc,argymin,argyinc,argwidth,argheight]
        result = chan.parsePutGet(args,"putField(argument)getField(result)",True)
        val =  result['result.value']
        return np.reshape(val,(width,height,3))
        
if __name__ == '__main__':
    app = QApplication(list())
    mandelbrotCreate = MandelbrotCreate()
    viewer = Viewer(mandelbrotCreate)
    sys.exit(app.exec_())
