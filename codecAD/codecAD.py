# codecAD.py
'''
Copyright - See the COPYRIGHT that is included with this distribution.
    NTNDA_Viewer is distributed subject to a Software License Agreement found
    in file LICENSE that is included with this distribution.

authors
    Marty Kraimer
    Mark Rivers
latest date 2020.07.27

This provides python access to the codec support that is provided by areaDetector/ADSupport
'''

import sys
import ctypes
import ctypes.util
import os
import numpy as np

class FindLibrary(object) :
    def __init__(self, parent=None):
        self.save = dict()
    def find(self,name) :
        lib = self.save.get(name)
        if lib!=None : return lib
        result = ctypes.util.find_library(name)
        if result==None : return None
        if os.name == 'nt':
            lib = ctypes.windll.LoadLibrary(result)
        else :
            lib = ctypes.cdll.LoadLibrary(result)
        if lib!=None : self.save.update({name : lib})
        return lib
        
class CodecAD() :
    def __init__(self, parent=None):
        self.codecName = 'none'
        self.data = None
        self.compressRatio = 1.0
        self.findLibrary = FindLibrary()

    def getCodecName(self) :
        return self.codecName

    def getData(self) :
        return self.data

    def getCompressRatio(self) :
        return self.compressRatio

    def decompress(self,data,codec,compressed,uncompressed) :
        self.codecName = codec['name']
        if len(self.codecName)==0 : 
            self.data = None
            self.codecName = 'none'
            self.compressRatio = 1.0
            return False
        typevalue = codec['parameters']
        if typevalue== 1 : dtype = "int8"; elementsize =int(1)
        elif typevalue== 5 : dtype = "uint8"; elementsize =int(1)
        elif typevalue== 2 : dtype = "int16"; elementsize =int(2)
        elif typevalue== 6 : dtype = "uint16"; elementsize =int(2)
        elif typevalue== 3 : dtype = "int32"; elementsize =int(4)
        elif typevalue== 7 : dtype = "uint32"; elementsize =int(4)
        elif typevalue== 4 : dtype = "int64"; elementsize =int(8)
        elif typevalue== 8 : dtype = "uint64"; elementsize =int(8)
        elif typevalue== 9 : dtype = "float32"; elementsize =int(4)
        elif typevalue== 10 : dtype = "float64"; elementsize =int(8)
        else : raise Exception('decompress mapIntToType failed')
        if self.codecName=='blosc':
            lib = self.findLibrary.find(self.codecName)
        elif self.codecName=='jpeg' :
            lib = self.findLibrary.find('decompressJPEG')
        elif self.codecName=='lz4' or self.codecName=='bslz4' :
            lib = self.findLibrary.find('bitshuffle')
        else : lib = None
        if lib==None : raise Exception('shared library ' +self.codecName + ' not found')
        inarray = bytearray(data)
        in_char_array = ctypes.c_ubyte * compressed
        out_char_array = ctypes.c_ubyte * uncompressed
        outarray = bytearray(uncompressed)
        if self.codecName=='blosc' : 
            lib.blosc_decompress(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif self.codecName=='lz4' :
            lib.LZ4_decompress_fast(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif self.codecName=='bslz4' :
            lib.bshuf_decompress_lz4(
                 in_char_array.from_buffer(inarray),
                 out_char_array.from_buffer(outarray),int(uncompressed/elementsize),
                 elementsize,int(0))
            data = np.array(outarray)
            data = np.frombuffer(data,dtype=dtype)
        elif self.codecName=='jpeg' :
            lib.decompressJPEG(
                 in_char_array.from_buffer(inarray),compressed,
                 out_char_array.from_buffer(outarray),uncompressed)
            data = np.array(outarray)
            data = data.flatten()
        else : raise Exception(self.codecName + " is unsupported codec")
        self.compressRatio = round(float(uncompressed/compressed))
        self.data = data
        return True
