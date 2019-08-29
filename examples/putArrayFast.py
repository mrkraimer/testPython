#!/usr/bin/env python

import sys,time
import numpy as np
from pvaccess import *
if len(sys.argv)<3 :
    print("must supply three args: channelName numElements sleepTime")
    exit()
channelName = sys.argv[1]
numElements = sys.argv[2]
sleepTime = float(sys.argv[3])
chan = Channel(channelName)
pv = chan.get("value")
arr = pv['value']
print(arr.dtype)
typ=str(arr.dtype)
print(typ)
ndarr = np.ndarray(shape=(int(numElements)),dtype=arr.dtype)
i = 0;
while True :
    ndarr.fill(i)
    i += 1
    pv["value"] = ndarr
    chan.put(pv)
    time.sleep(sleepTime)





