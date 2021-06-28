#!/usr/bin/env python
from matplotlib.patches import Ellipse
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

class PLOT() :
    def __init__(self,size):
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

    def draw(self,xoffset,yoffset,width,height,color) :
        xy = (xoffset,yoffset)
        ellipse = mpl.patches.Ellipse(xy=xy, width=width, height=height,color=color,fill=False)
        self.ax.add_patch(ellipse)

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    ellipse = PLOT(1.01)
    n = 4
    width =  [.4,.6,.8,1.9]
    height = [.8,1.2,1.6,1.9]
    color = ['r','g','b','k']
    for i in range(n) :
        ellipse.draw(0,0,width[i],height[i],color[i])
    ellipse.display()    
