#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Spiral() :
    def __init__(self,npts):
        mpl.rcParams['toolbar'] = 'None'
        self.npts = npts
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot(111,projection='3d')

    def draw(self,rmax) :
        self.rmax = 2*np.pi*rmax
        self.dr = self.rmax/self.npts
        self.t = np.arange(0, self.rmax, self.dr)
        fact = 1.0/self.rmax
        x = fact*self.t*np.cos(self.t)
        y = fact*self.t*np.sin(self.t)
        z = np.arange(0, 1,1/self.npts)
        self.ax.plot3D(x,y,z,'red')
        self.t = np.arange(-self.rmax,0, self.dr)
        x = fact*self.t*np.cos(self.t)
        y = fact*self.t*np.sin(self.t)
        self.ax.plot3D(x,y,z,'lime')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    spiral = Spiral(1000)
    spiral.draw(8)
    spiral.display()    
