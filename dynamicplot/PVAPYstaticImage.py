#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from pvaccess import *
import sys

if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs<2 :
        print('must specify channelName')
    else :
        channelName = sys.argv[1]
        chan = Channel(channelName)
        val = chan.get("x,y")
        x = val["x"]
        y = val["y"]
        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
