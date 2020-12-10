#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
min = 0.0
max = 2*np.pi
npts = 500
inc = (max-min)/npts
t = np.arange(min, max, inc)
a=1.0
b=2.0
limit = a
if b>a : limit = b
plt.xlim(-limit,limit)
plt.ylim(-limit,limit)
c=1.0
x = a*np.cos(t*c)
y = b*np.sin(t*c)

plt.xlim(-limit,limit)
plt.ylim(-limit,limit)
plt.plot(x, y,scalex=False,scaley=False)

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

plt.show()
