#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

class Parabola() :
    def __init__(self,npts,size):
        mpl.rcParams['toolbar'] = 'None'
        self.size = size
        self.npts = npts
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot()
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.set_xlim(-size,size)
        self.ax.set_ylim(-size,size)

    def drawVertical(self,invert,color) :
        self.t = np.linspace(-self.size,self.size,self.npts)
        self.x = self.t
        if not invert :
            self.y = self.size*self.x**2
        else :
            self.y = -self.size*self.x**2
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalRight(self,invert,color) :
        if not invert :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = self.t
            self.x = self.size*self.t**2
        else :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = -self.t
            self.x = self.size*self.t**2
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalLeft(self,invert,color) :
        if not invert :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = self.t
            self.x = -self.size*self.t**2
        else :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = -self.t
            self.x = -self.size*self.t**2
        self.ax.plot(self.x,self.y,color)
    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    nargs = len(sys.argv)
    arg = 'all'
    if nargs>=2 :
        arg = sys.argv[1]
    parabola = Parabola(1000,1.01)
    if arg=='all' or arg=='vb' :
        parabola.drawVertical(True,'k')
    if arg=='all' or arg=='vt' :
        parabola.drawVertical(False,'k')
    if arg=='all' or arg=='hr' :
        parabola.drawHorizontalRight(True,'r')
        parabola.drawHorizontalRight(False,'r')
    if arg=='all' or arg=='hl' :
        parabola.drawHorizontalLeft(True,'r')
        parabola.drawHorizontalLeft(False,'r')
    parabola.display()    
