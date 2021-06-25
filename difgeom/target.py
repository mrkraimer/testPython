#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Circle() :
    def __init__(self,npts,size):
        mpl.rcParams['toolbar'] = 'None' 
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
        self.tmax = 2*np.pi
        self.dt = self.tmax/npts
        self.t = np.arange(0, self.tmax, self.dt)

    def draw(self,radius) :
        x =  radius*np.cos(self.t)
        y =  radius*np.sin(self.t)
        self.ax.plot(x,y,'black')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    circle = Circle(1000,1.01)
    n = 3
    for i in range(1,n+1) :
        circle.draw(float(i/n))
    circle.display()    
