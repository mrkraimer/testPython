# MandelbrotCreatePython.py
#from PyQt5.QtCore import QObject
import numpy as np

class MandelbrotCreatePython :

    def calcIntensity(self,x,y) :
        c = complex(x,y)
        z = complex(0.0,0.0)
        i = 0
        while abs(z) < 2 and i < 255 :
            z = z**2 + c
            i += 1
        # Color scheme is that of Julia sets
        color = (i % 8 * 32, i % 16 * 16, i % 32 * 8)
        return color

    def createImage(self,arg) :
        xmin = float(arg[0])
        xinc = float(arg[1])
        ymin = float(arg[2])
        yinc = float(arg[3])
        width = int(arg[4])
        height = int(arg[5])
        pixarray = np.full((width,height,3),255,dtype="uint8")
        for i in range(height) :
            y = ymin + i*yinc
            for j in range(width) :
                x = xmin + j*xinc
                color = self.calcIntensity(x,y)
                pixarray[j][i][0] = color[0]
                pixarray[j][i][1] = color[1]
                pixarray[j][i][2] = color[2]
        return pixarray

            
        
        
