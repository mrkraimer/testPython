#!/usr/bin/env python

import sys, time
from p4p.client.thread import Context
import numpy as np

nSinceLastReport = 0
lasttime = time.time() - 2

def mycallback(arg):
    global nSinceLastReport
    global lasttime
    arr = np.array(arg)
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

with Context('pva') as ctxt:
    S = ctxt.monitor(sys.argv[1], mycallback)
    input("enter something")
    S.close()
print('Exiting')
