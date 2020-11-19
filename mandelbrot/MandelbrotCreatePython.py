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
        xmax = float(arg[1])
        ymin = float(arg[2])
        ymax = float(arg[3])
        nx = int(arg[4])
        ny = int(arg[5])
        xinc = (xmax-xmin)/nx
        yinc = (ymax-ymin)/ny
        nz = int(3)
        if len(arg)==7 : nz = int(arg[6])
        if nz==1 :
            pixarray = np.full((ny,nx),255,dtype="uint8")
        else :
            pixarray = np.full((ny,nx,nz),255,dtype="uint8")
        for i in range(ny) :
            y = ymin + i*yinc
            for j in range(nx) :
                x = xmin + j*xinc
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

            
        
        
