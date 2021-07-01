#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import argparse

class Hyperbola() :
    def __init__(self,npts,size):
        mpl.rcParams['toolbar'] = 'None'
        self.size = size
        self.npts = npts
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot()
        #self.ax.xaxis.set_visible(False)
        #self.ax.yaxis.set_visible(False)
        #self.ax.spines['top'].set_visible(False)
        #self.ax.spines['right'].set_visible(False)
        #self.ax.spines['left'].set_visible(False)
        #self.ax.spines['bottom'].set_visible(False)
        self.ax.set_xlim(-size,size)
        self.ax.set_ylim(-size,size)

    def drawVertical(self,invert,offset,color) :
        self.t = np.linspace(-self.size,self.size,self.npts)
        self.x = self.t
        if not invert :
            self.y = np.sqrt((self.x*self.x + offset*offset))
        else :
            self.y = -np.sqrt((self.x*self.x + offset*offset))
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalRight(self,invert,offset,color) :
        if not invert :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = self.t
            self.x = np.sqrt((self.y*self.y + offset*offset))
        else :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = -self.t
            self.x = np.sqrt((self.y*self.y + offset*offset))
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalLeft(self,invert,offset,color) :
        if not invert :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = self.t
            self.x = -np.sqrt((self.y*self.y + offset*offset))
        else :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = -self.t
            self.x = -np.sqrt((self.y*self.y + offset*offset))
        self.ax.plot(self.x,self.y,color)
    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='offset -vb -vt -hr -hl : default all')
    parser.add_argument('offset', action="store")
    parser.add_argument('-vb', action="store_true")
    parser.add_argument('-vt', action="store_true")
    parser.add_argument('-hr', action="store_true")
    parser.add_argument('-hl', action="store_true")
    args = parser.parse_args()
    offset = float(args.offset)
    if offset<.1 or offset>.8 :
        print('offset must be between .1 and .8')
        exit()
    if not(args.vb) and not(args.vt) and not(args.hr) and not(args.hr) :
        args.vb = True; args.vt = True; args.hr = True; args.hl = True;
    hyperbola = Hyperbola(1000,1.01)
    if args.vb :
        hyperbola.drawVertical(True,offset,'dimgray')
    if args.vt : 
        hyperbola.drawVertical(False,offset,'black')
    if args.hr :    
        hyperbola.drawHorizontalRight(True,offset,'salmon')
        hyperbola.drawHorizontalRight(False,offset,'red')
    if args.hl : 
        hyperbola.drawHorizontalLeft(True,offset,'lime')
        hyperbola.drawHorizontalLeft(False,offset,'green')
    hyperbola.display()    
