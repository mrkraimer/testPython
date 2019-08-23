#!/usr/bin/env python3

import sys, time, logging

from p4p.client.thread import Context

import numpy as np

nSinceLastReport = 0
lasttime = time.time()

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
    print("size ",sz)
    if sz<10 :
        print("size is %d" % (sz))
        print(arr)
    events = nSinceLastReport/timediff
    elements = events*sz/1e6
    print("monitors/sec ",events," megaElements/sec ",elements," timediff ",timediff)
    lasttime = timenow
    nSinceLastReport = 0

print("Create Context")
with Context('pva') as ctxt:
    print("Subscribe to", sys.argv[1])
    S = ctxt.monitor(sys.argv[1], mycallback)
    print("Waiting")
    try:
        time.sleep(2)
        input("enter something")
    except KeyboardInterrupt:
        pass
    print("Close subscription")
    S.close()
print('Exiting')
