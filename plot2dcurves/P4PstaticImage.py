#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from p4p.client.thread import Context
import sys

if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs<2 :
        print('must specify channelName')
    else :
        channelName = sys.argv[1]
        ctxt = Context('pva')
        val = ctxt.get(channelName,"x,y")
        x = val["x"]
        y = val["y"]
        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
