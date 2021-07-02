#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Heart() :
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

    def draw(self,xoffset,yoffset) :
        self.t = np.arange(0, self.rmax, self.dr)
        x =  (1.0 - np.cos(self.t)*np.cos(self.t))*np.sin(self.t) + xoffset
        y =  (1.0 - np.cos(self.t)*np.cos(self.t)*np.cos(self.t))*np.cos(self.t) + yoffset
        self.ax.plot(x,y,'black')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    heart = Heart(1000,3.3)
    n = 5
    xoffset = [0,2,2,-2,-2]
    yoffset = [.6,2.6,-1.4,2.6,-1.4]
    for i in range(n) :
        heart.draw(xoffset[i],yoffset[i])
    heart.display()    
