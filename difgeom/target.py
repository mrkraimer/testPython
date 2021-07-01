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

    def draw(self,radius,color) :
        circle = plt.Circle((0,0),radius,facecolor='None', edgecolor=color, lw=3)
        self.ax.add_patch(circle)

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    circle = Circle(1000,1.01)
    n = 3
    color = ['r','g','b']
    circle.draw(.03,'k')
    for i in range(n) :
        circle.draw(float((i+1)/n),color[i])
    circle.display()    
