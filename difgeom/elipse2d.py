#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication

class Ellipse() :
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def show(self) : 
        a = self.a
        b = self.b
        c = self.c
        min = 0.0
        max = 2*np.pi
        npts = 500
        inc = (max-min)/npts
        t = np.arange(min, max, inc)
        limit = a
        if b>a : limit = b
        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        x = a*np.cos(t*c)
        y = b*np.sin(t*c)

        plt.xlim(-limit,limit)
        plt.ylim(-limit,limit)
        plt.axes().set_aspect('equal')
        plt.plot(x, y,scalex=False,scaley=False)
        plt.xlabel("value")
        plt.title("ellipse")

        dx = -a*c*np.sin(t*c)
        dy = b*c*np.cos(t*c)
        d2x = -a*c*c*np.cos(t*c)
        d2y = -b*c*c*np.sin(t*c)

        num = dx*d2y - d2x*dy
        deom = (dx*dx + dy*dy)**(3/2)
        curvature = num/deom
        radius = 1.0/curvature
        f, ax = plt.subplots()
        ax.plot(t,radius)
        ax.set_title('radius of curvature')
        ax.set(xlabel="radians")

        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = 1
    b = 2
    c = 1
    nargs = len(sys.argv)
    if nargs >= 2: a = float(sys.argv[1])
    if nargs >= 3: b = float(sys.argv[2])
    if nargs >= 4: c = float(sys.argv[3])
    ellipse = Ellipse(a,b,c)
    ellipse.show()
    junk = input("enter anything to exit")
    exit()
    sys.exit(app.exec_())
