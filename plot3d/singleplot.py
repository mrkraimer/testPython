#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
ax = plt.axes(projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
min = -1.0
max = 1.0
npts = 1000
inc = (max-min)/npts
t = np.arange(min, max, inc)
a=1.0
b=1.0
c=1.0
x = a*np.cos(2*np.pi*t*c)
y = b*np.sin(2*np.pi*t*c)
ax.plot3D(x, y, t, 'black')

a=1.0
b=.25
x = a*np.cos(2*np.pi*t*c)
y = b*np.sin(2*np.pi*t*c)
ax.plot3D(x, y, t, 'blue')

plt.show()
