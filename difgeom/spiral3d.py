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
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

    def draw(self,rmax) :
        rmax = 2*np.pi*rmax
        dr = rmax/self.npts
        fact = 2.0/rmax
        t = np.arange(-rmax,0,dr)
        x = fact*t*np.cos(t)
        y = fact*t*np.sin(t)
        z = np.arange(-1, 0,1/self.npts)
        self.ax.plot3D(x,y,z,'lime')
        t = np.arange(0, rmax, dr)
        x = fact*t*np.cos(t)
        y = fact*t*np.sin(t)
        z = np.arange(0, 1,1/self.npts)
        self.ax.plot3D(x,y,z,'red')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    spiral = Spiral(500)
    spiral.draw(8)
    spiral.display()    
