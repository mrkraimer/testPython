#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

class Spiral() :
    def __init__(self,npts):
        mpl.rcParams['toolbar'] = 'None'
        self.npts = npts
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

    def draw(self,rmax,power) :
        rmax = 2*np.pi*rmax
        dr = rmax/self.npts
        fact = 2.0/rmax
        t = np.arange(-rmax,rmax,dr)
        x = fact*(t**(power))*np.cos(t)
        y = fact*(t**(power))*np.sin(t)
        z = np.arange(-1,1,1/self.npts)
        self.ax.plot3D(x,y,z,'lime')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    power = 1
    nargs = len(sys.argv)
    if nargs==2 :
        power = float(sys.argv[1])
    spiral = Spiral(500)
    spiral.draw(8,power)
    spiral.display()    
