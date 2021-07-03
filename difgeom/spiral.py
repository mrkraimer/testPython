#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Spiral() :
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

    def draw(self,xoffset,yoffset,rmax) :
        self.rmax = 2*np.pi*rmax
        self.dr = self.rmax/self.npts
        self.t = np.arange(0, self.rmax, self.dr)
        fact = 1.0/self.rmax
        x = fact*self.t*np.cos(self.t) + xoffset
        y = fact*self.t*np.sin(self.t) + yoffset
        self.ax.plot(x,y,'black')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    spiral = Spiral(1000,3)
    n = 5
    xoffset = [0,2,2,-2,-2]
    yoffset = [0,2,-2,2,-2]
    rmax = [1,3,5,7,9]
    for i in range(n) :
        spiral.draw(xoffset[i],yoffset[i],rmax[i])
    spiral.display()    
