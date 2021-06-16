#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton,QHBoxLayout

class Wireframe(QWidget) :
    def __init__(self):
        pass
        
    def closeEvent(self, event) :
        QApplication.closeAllWindows()    
 
    def show(self) :
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')

# Set up the grid in polar
        theta = np.linspace(0,2*np.pi,90)
        r = np.linspace(0,3,50)
        T, R = np.meshgrid(theta, r)

# Then calculate X, Y, and Z
        X = R * np.cos(T)
        Y = R * np.sin(T)
        Z = np.sqrt(X**2 + Y**2) - 1

# Set the Z values outside your range to NaNs so they aren't plotted
        Z[Z < 0] = np.nan
        ax.plot_wireframe(X, Y, Z)
        ax.set_zlim(0,2)
        fig.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wireframe = Wireframe()
    wireframe.show()
    sys.exit(app.exec_())
