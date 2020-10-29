#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
min = -1.0
max = 1.0
npts = 1000
inc = (max-min)/npts
t = np.arange(min, max, inc)
nplots = 3
fig, ax = plt.subplots(ncols=nplots,tight_layout=True,subplot_kw={"projection": "3d"})
for i in range(nplots):
    ax[i].set_xlabel("x")
    ax[i].set_ylabel("y")
    ax[i].set_zlabel("z")

a=1.0
b=1.0
c=2.0
x = a*np.cos(2*np.pi*t*c)
y = b*np.sin(2*np.pi*t*c)
ax[0].set_title("circle")
ax[0].plot3D(x, y, t, 'black')

a=1.0
b=3.0
c=2.0
x = a*np.cos(2*np.pi*t*c)
y = b*np.sin(2*np.pi*t*c)
ax[1].set_title("ellipse")
#ax[1].set_aspect("equal") not supported
ax[1].plot3D(x, y, t, 'blue')

x = t*a*np.cos(2*np.pi*t*c)
y = t*b*np.sin(2*np.pi*t*c)
ax[2].set_title("spiral")
ax[2].plot3D(x, y, t, 'green')
plt.show()
