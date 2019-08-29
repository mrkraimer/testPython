#!/usr/bin/env python

import sys,time
import numpy as np
from pvaccess import *

nSinceLastReport = 0
lasttime = time.time() -2

def mycallback(arg):
    global nSinceLastReport
    global lasttime
    arr = arg['value']
    nSinceLastReport = nSinceLastReport +1
    timenow = time.time()
    timediff = timenow - lasttime
    if(timediff<1) : return
    events = nSinceLastReport/timediff
    sz = arr.size
    if sz<10 :
        print(arr)
    events = nSinceLastReport/timediff
    elements = events*sz/1e6
    print("monitors/sec ",events," megaElements/sec ",elements)
    lasttime = timenow
    nSinceLastReport = 0

channelName = sys.argv[1]
c = Channel(channelName)
c.subscribe('mycallback', mycallback)
c.startMonitor()
input("enter something")
c.stopMonitor()
c.unsubscribe('mycallback')
print('Exiting')
