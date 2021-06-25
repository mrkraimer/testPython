#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Triangle() :
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
        

    def draw(self,x,y) :
        self.ax.plot(x,y,'black')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    triangle = Triangle(1.01)
    x = [0,1,-1,0]
    y = [1,-1,-1,1]
    triangle.draw(x,y)
    x1 = x
    y1 = y
    for i in range(len(x)) :
        x1[i] = x[i]/2
        y1[i] = y[i]/2
    triangle.draw(x1,y1)
    x2 = x
    y2 = y
    for i in range(len(x)) :
        x2[i] = x[i]/3
        y2[i] = y[i]/3
    triangle.draw(x2,y2)
    triangle.display()    
