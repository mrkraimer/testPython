#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Figure8() :
    def __init__(self,npts,size):
        mpl.rcParams['toolbar'] = 'None'
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
        self.rmax = 2*np.pi
        self.dr = self.rmax/npts

    def drawVertical(self,xoffset,yoffset,xmax,ymax) :
        self.t = np.arange(0, self.rmax, self.dr)
        x =  xmax*np.sin(self.t)*np.cos(self.t) + xoffset
        y =  ymax*np.sin(self.t) + yoffset
        self.ax.plot(x,y,'black')

    def drawHorizantal(self,xoffset,yoffset,xmax,ymax) :
        self.t = np.arange(0, self.rmax, self.dr)
        y =  xmax*np.sin(self.t)*np.cos(self.t) + yoffset
        x =  ymax*np.sin(self.t) + xoffset
        self.ax.plot(x,y,'lime')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    figure8 = Figure8(1000,4)
    n = 5
    xoffset = [0,2,-2, 2,-2]
    yoffset = [0,2, 2,-2,-2]
    xmax = [1.0,1.00,1.00,1.0,1.0]
    ymax = [1.1,1.25,1.25,1.5,1.5]
    for i in range(n) :
        figure8.drawVertical(xoffset[i],yoffset[i],xmax[i],ymax[i])
        figure8.drawHorizantal(xoffset[i],yoffset[i],xmax[i],ymax[i])
    figure8.display()    
