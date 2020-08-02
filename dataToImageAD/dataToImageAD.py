# dataToImageAD.py

import numpy as np
import math


class DataToImageAD() :
    '''
dataToImageAD provides python access to the data provided by areaDetector/ADSupport
It is meant for use by a callback from an NTNDArray record.
NTNDArray is implemented in areaDetector/ADCore.
NTNDArray has the following fields of interest to DataToImageAD:
    value            This contains a numpy array with a scalar dtype
    dimension        2d or 3d array description
      
Normal use is:
...
from dataToImageAD import DataToImageAD
...
    self.dataToImageAD = DataToImageAD()
    self.imageDict = self.dataToImage.imageDictCreate()
    
...
    try:
        self.dataToImage.dataToImage(data,dimArray,self.imageSize,...)
        imageDict = self.dataToImage.getImageDict()
        self.imageDict["image"] = imageDict["image"]
        ... other methods
...   
     
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
    Mark Rivers
latest date 2020.07.30
    '''
    def __init__(self,parent=None) :
        self.__image = None
        self.__imageDict = self.imageDictCreate()
        self.__channelLimits = (0,255)
        self.__imageLimits = (0,255)
        self.__manualLimits = (0,255)

    def imageDictCreate(self) :
        """
        Returns
        -------
        imageDict : dict
            imageDict["image"]        None
            imageDict["dtypeChannel"] None
            imageDict["dtypeImage"]   None
            imageDict["nx"]           0
            imageDict["ny"]           0
            imageDict["nz"]           0
        """
        return {"image" : None ,\
             "dtypeChannel" : None ,\
             "dtypeImage" : None  ,\
              "nx" : 0 ,\
              "ny" : 0 ,
               "nz" : 0 }

    def setManualLimits(self,manualLimits) :
        """
         Parameters
        -----------
            manualLimits : tuple
                 manualLimits[0] : lowManualLimit
                 manualLimits[1] : highManualLimit
        """
        self.__manualLimits = manualLimits

    def getImageDict(self) :
        """ 
        Returns
        -------
        imageDict : dict
            imageDict["image"]        numpy 2d or 3d array for the image
            imageDict["dtypeChannel"] dtype for data from the callback
            imageDict["dtypeImage"]   dtype for image
            imageDict["nx"]           nx for data from the callback
            imageDict["ny"]           ny for data from the callback
            imageDict["nz"]           nz (1,3) for (2d,3d) image
        
        """
        return self.__imageDict
 
    def getChannelLimits(self) :
        """ 
        Returns
        -------
        channelLimits : tuple
            channelLimits[0]    lowest value of data from the callback
            channelLimits[0]    highest value of data from the callback
        
        """
        return self.__channelLimits

    def getImageLimits(self) :
        """ 
        Returns
        -------
        imageLimits : tuple
            imageLimits[0]    lowest value of data from the image
            imageLimits[0]    highest value of data from the image
        
        """
        return self.__imageLimits

    def getManualLimits(self) :
        """
        Returns
        -------
            manualLimits : tuple
                 manualLimits[0] : lowManualLimit
                 manualLimits[1] : highManualLimit
        """
        return self.__manualLimits

    def reshape(self,data,dimArray) :
        """
         Parameters
        -----------
            data     : data from the callback
            dimArray : dimension from callback
        """
        nz = 1
        ndim = len(dimArray)
        if ndim ==2 :
            nx = dimArray[0]["size"]
            ny = dimArray[1]["size"]
            image = np.reshape(data,(ny,nx))
        elif ndim ==3 :
            if dimArray[0]["size"]==3 :
                nz = dimArray[0]["size"]
                nx = dimArray[1]["size"]
                ny = dimArray[2]["size"]
                image = np.reshape(data,(ny,nx,nz))
            elif dimArray[1]["size"]==3 :
                nz = dimArray[1]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[2]["size"]
                image = np.reshape(data,(ny,nz,nx))
                image = np.swapaxes(image,2,1)
            elif dimArray[2]["size"]==3 :
                nz = dimArray[2]["size"]
                nx = dimArray[0]["size"]
                ny = dimArray[1]["size"]
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
        """
         Parameters
        -----------
            data               : data from the callback
            dimArray           : dimension from callback
            imageSize          : width and height for the generated image
            scaleType          : (0,1,2) means (noScale,autoScale,manualScale)
            showLimits         : (False,True) means channelLimits and imageLimits (are not, are) updated
            suppressBackground : (False,True) means that background (will not,will) be done
        """
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
            displayMin = self.__manualLimits[0]
            displayMax = self.__manualLimits[1]
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
            self.__channelLimits = (dataMin,dataMax) 
            imageMin = np.min(data)
            imageMax = np.max(data)
            self.__imageLimits = (imageMin,imageMax)
        retval = self.reshape(data,dimArray)
        image = retval[0]
        nx = retval[1]
        ny = retval[2]
        nz = retval[3]
        nmax = 0
        if nx>nmax : nmax = nx
        if ny>nmax : nmax = ny
        if nmax > imageSize :
            step = math.ceil(float(nmax)/imageSize)
            if nz==1 :
                image = image[::step,::step]
            else :
                image =  image[::step,::step,::]   
        self.__imageDict["image"] = image
        self.__imageDict["nx"] = nx
        self.__imageDict["ny"] = ny
        self.__imageDict["nz"] = nz
        self.__imageDict["dtypeChannel"] = dtype
        self.__imageDict["dtypeImage"] = image.dtype
        self.__imageDict["dtypeChannel"] = dtype
        if image.dtype!=self.__imageDict["dtypeImage"] :
            self.__imageDict["dtypeImage"] = image.dtype
            if image.dtype==np.uint8 :
                self.__manualLimits = (0,255)
            else :
                self.__manualLimits = (0,65535)
        
