# MandelbrotCreatePython.py

import numpy as np

class MandelbrotCreatePython :

    def addClientConnectionCallback(self,clientConnectionCallback) :
        clientConnectionCallback.connectionCallback(True)
    def checkConnected(self) :
        return True
    
    def calcIntensity(self,x,y) :
        c = complex(x,y)
        z = complex(0.0,0.0)
        i = 0
        while abs(z) < 2 and i < 255 :
            z = z**2 + c
            i += 1
        return i

    def createImage(self,arg) :
        xmin = float(arg[0])
        xinc = float(arg[1])
        ymin = float(arg[2])
        yinc = float(arg[3])
        width = int(arg[4])
        height = int(arg[5])
        nz = int(3)
        if len(arg)==7 : nz = int(arg[6])
        if nz==1 :
            pixarray = np.full((width,height),255,dtype="uint8")
        else :
            pixarray = np.full((width,height,nz),255,dtype="uint8")
        for i in range(width) :
            x = xmin + i*xinc
            for j in range(height) :
                y = ymin + j*yinc
                intensity = self.calcIntensity(x,y)
                if nz == 1 :
                    # Color scheme is grayscale
                    pixarray[i][j] = 256 - intensity
                else :
                    # Color scheme is that of Julia sets
                    pixarray[i][j][0] = intensity % 8 * 32
                    pixarray[i][j][1] = intensity % 16 * 16
                    pixarray[i][j][2] = intensity % 32 * 8
        return pixarray

            
        
        
