#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import argparse

class Parabola() :
    def __init__(self,npts,size):
        mpl.rcParams['toolbar'] = 'None'
        self.size = size
        self.npts = npts
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim(-size,size)
        self.ax.set_ylim(-size,size)

    def drawVertical(self,invert,color) :
        self.t = np.linspace(-self.size,self.size,self.npts)
        self.x = self.t
        if not invert :
            self.y = self.size*self.x**2
        else :
            self.y = -self.size*self.x**2
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalRight(self,invert,color) :
        if not invert :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = self.t
            self.x = self.size*self.t**2
        else :
            self.t = np.linspace(0,self.size,self.npts)
            self.y = -self.t
            self.x = self.size*self.t**2
        self.ax.plot(self.x,self.y,color)

    def drawHorizontalLeft(self,invert,color) :
        if not invert :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = self.t
            self.x = -self.size*self.t**2
        else :
            self.t = np.linspace(-self.size,0,self.npts)
            self.y = -self.t
            self.x = -self.size*self.t**2
        self.ax.plot(self.x,self.y,color)

    def drawAxis(self) :
        points = (-self.size,self.size)
        zeros = (0,0)
        self.ax.plot(points,zeros,'black',linestyle = 'dotted')
        self.ax.plot(zeros,points,'black',linestyle = 'dotted')

    def display(self) :
        plt.show()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='-vb -vt -hr -hl : default all')
    parser.add_argument('-vb', action="store_true")
    parser.add_argument('-vt', action="store_true")
    parser.add_argument('-hr', action="store_true")
    parser.add_argument('-hl', action="store_true")
    args = parser.parse_args()
    if not(args.vb) and not(args.vt) and not(args.hr) and not(args.hr) :
        args.vb = True; args.vt = True; args.hr = True; args.hl = True;
    parabola = Parabola(1000,1.01)
    if args.vb :
        parabola.drawVertical(True,'darkblue')
    if args.vt : 
        parabola.drawVertical(False,'blue')
    if args.hr :    
        parabola.drawHorizontalRight(True,'darkred')
        parabola.drawHorizontalRight(False,'red')
    if args.hl : 
        parabola.drawHorizontalLeft(True,'limegreen')
        parabola.drawHorizontalLeft(False,'green')
    parabola.drawAxis()
    parabola.display()    
