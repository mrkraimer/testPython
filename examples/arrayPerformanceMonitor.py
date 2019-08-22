#!/usr/bin/env python3

import time

from pvaccess import *
import numpy as np

nSinceLastReport = 0
lasttime = time.time()

def mycallback(arg):
    global nSinceLastReport
    global lasttime
# the following does not take a lot of time
    arr = np.array(arg)
    nSinceLastReport = nSinceLastReport +1
    timenow = time.time()
    timediff = timenow - lasttime
    if(timediff<10) : return
    events = nSinceLastReport/timediff
#   the following takes a long time for big arrays
    arr = np.array(arg.getScalarArray('value'))
    sz = arr.size
    print("size ",sz)
    if sz<10 :
        print("size is %d" % (sz))
        print(arr)
    events = nSinceLastReport/timediff
    elements = events*sz/1e6
    print("monitors/sec ",events," megaElements/sec ",elements," timediff ",timediff)
    lasttime = timenow
    nSinceLastReport = 0

channelName = input("enter channelName: ")
c = Channel(channelName)
c.subscribe('mycallback', mycallback)
c.startMonitor()
time.sleep(2)
input("enter something")
c.stopMonitor()
c.unsubscribe('mycallback')
print('Exiting')
