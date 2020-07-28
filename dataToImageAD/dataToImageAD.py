# dataToImageAD.py
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
    Mark Rivers
latest date 2020.07.27

This provides python code to convert areaDetector NTNDArray data to 2d or 3d Image.
'''

import numpy as np
import math


class DataToImageAD() :
    def __init__(self,parent=None) :
        self.image = None
        self.dtypeChannel = None
        self.dtypeImage = None
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.imageDict = self.imageDictCreate()
        self.channelLimits = (0,255)
        self.imageLimits = (0,255)
        self.manualLimits = (0,255)

    def imageDictCreate(self) :
        return {"image" : None ,\
             "dtypeChannel" : None ,\
             "dtypeImage" : None  ,\
              "nx" : 0 ,\
              "ny" : 0 ,
               "nz" : 0 }

    def setManualLimits(self,manualLimits) :
        self.manualLimits = manualLimits

    def getImageDict(self) :
        return self.imageDict
 
    def getChannelLimits(self) :
        return self.channelLimits

    def getImageLimits(self) :
        return self.imageLimits

    def getManualLimits(self) :
        return self.manualLimits

    def reshape(self,data,dimArray,step) :
        nz = 1
        ndim = len(dimArray)
        if ndim ==2 :
            nx = dimArray[0]["size"]
            ny = dimArray[1]["size"]
            if step > 0 :
                nx = int(float(nx)/step)
                ny = int(float(ny)/step)
            image = np.reshape(data,(ny,nx))
        elif ndim ==3 :
            if dimArray[0]["size"]==3 :
                nz = dimArray[0]["size"]
                nx = dimArray[1]["size"]
                ny = dimArray[2]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(ny,nx,nz))
            elif dimArray[1]["size"]==3 :
                nz = dimArray[1]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[2]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(ny,nz,nx))
                image = np.swapaxes(image,2,1)
            elif dimArray[2]["size"]==3 :
                nz = dimArray[2]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[1]["size"]
                if step > 0 :
                    nx = int(float(nx)/step)
                    ny = int(float(ny)/step)
                image = np.reshape(data,(nz,ny,nx))
                image = np.swapaxes(image,0,2)
                image = np.swapaxes(image,0,1)
            else  :  
                raise Exception('no axis has dim = 3')
                return
        else :
                raise Exception('ndim not 2 or 3')
        return (image,nx,ny,nz)        
        
    def dataToImage(self,data,dimArray,imageSize,scaleType=1,showLimits=False,suppressBackground=False) :
        ndim = len(dimArray)
        if ndim!=2 and ndim!=3 :
            raise Exception('ndim not 2 or 3')
        nmax = 0
        nz = 0
        nx = 0
        ny = 0
        step = 1
        ndim = len(dimArray)
        if ndim >=2 :
            num = int(dimArray[0]["size"])
            if num>nmax : nmax = num
            num = int(dimArray[1]["size"])
            if num>nmax : nmax = num
            if ndim==3 :
                num = int(dimArray[2]["size"])
                if num>nmax : nmax = num
        if nmax>imageSize :
            retval = self.reshape(data,dimArray,1)
            image = retval[0]
            nx = retval[1]
            ny = retval[2]
            nz = retval[3]
            step = math.ceil(float(nmax)/imageSize)
            if nz==1 :
                image = image[::step,::step]
            else :
                image =  image[::step,::step,::]  
            data = image.flatten()
        dtype = data.dtype
        dataMin = np.min(data)
        dataMax = np.max(data)
        if scaleType == 0 :
            if dtype != np.uint8 and dtype != np.uint16 :
                raise Exception('noScale requires uint8 or uint16')
                return
        if scaleType == 1 :
            displayMin = dataMin
            displayMax = dataMax
        else :
            displayMin = self.manualLimits[0]
            displayMax = self.manualLimits[1]
        if scaleType != 0 :
            suppress = suppressBackground
            if dtype==np.uint8 or dtype==np.uint8 : suppress = False
            if suppress :
                xp = (displayMax/255,displayMax)
            else :
                xp = (displayMin, displayMax)
            fp = (0.0, 255.0)
            data = (np.interp(data,xp,fp)).astype(np.uint8)
        if showLimits :
            self.channelLimits = (dataMin,dataMax) 
            imageMin = np.min(data)
            imageMax = np.max(data)
            self.imageLimits = (imageMin,imageMax)
        retval = self.reshape(data,dimArray,step)
        image = retval[0]
        if step==1 : 
            nx = retval[1]
            ny = retval[2]
            nz = retval[3]
        self.imageDict["image"] = image
        self.imageDict["nx"] = nx
        self.imageDict["ny"] = ny
        self.imageDict["nz"] = nz
        self.imageDict["dtypeChannel"] = dtype
        self.imageDict["dtypeImage"] = image.dtype
        self.imageDict["dtypeChannel"] = dtype
        if image.dtype!=self.imageDict["dtypeImage"] :
            self.imageDict["dtypeImage"] = image.dtype
            if image.dtype==np.uint8 :
                self.manualLimits = (0,255)
            else :
                self.manualLimits = (0,65535)
        
