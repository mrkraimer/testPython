#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from pvaccess import *

chan = Channel("x")
pv = chan.get("value")
x = pv['value']
chan = Channel("y")
pv = chan.get("value")
y = pv['value']
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.show()
