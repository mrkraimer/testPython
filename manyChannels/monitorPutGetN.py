#!/usr/bin/env python

#
# This example can be used to monitor large number of channels with slow 
# updates.
#

import sys
import time
from pvaccess import Channel,CA

class ScaleMonitor:

    def __init__(self, name):
        self.name = name
        self.value = 0
        self.nReceived = 0
        self.nMissed = 0

    def toString(self):
        return '%6s: Received: %7d ; Missed: %7d ' % (self.name, self.nReceived, self.nMissed)
       
    def monitor(self, pv):
        oldValue = self.value
        self.value = pv['value']
        self.nReceived += 1
        diff = self.value - oldValue
        if oldValue > 0:
            self.nMissed += diff-1

if __name__ == '__main__':
    nChannels = 2
    provider = "pva"
    if len(sys.argv) > 1:
        nChannels = int(sys.argv[1])
    if len(sys.argv) > 2:
        provider = sys.argv[2]
    nameList = list()
    channelList = list()
    monitorList = list()
    startTime = time.time()
    for channelCnt in range(1,nChannels+1):
        channelName = 'X%s' % channelCnt
        nameList.append(channelName)
        if provider == "ca" :
            c = Channel(channelName,CA)
        else :
            c = Channel(channelName)
        channelList.append(c);
        m = ScaleMonitor(channelName)
        monitorList.append(m);
    for i in range(nChannels):
        name = nameList[i]
        chan = channelList[i]
        m = monitorList[i]
        chan.subscribe(name, m.monitor)
    for i in range(nChannels):
        chan = channelList[i]
        chan.startMonitor()
        if i % 500 == 0:
            time.sleep(.5)
    while True :
        allConnected = True
        for i in range(nChannels):
            if(monitorList[i].nReceived==0) :
                allConnected = False
        if allConnected:
            break
        print("sleeping")
        time.sleep(1)

    time.sleep(1)
    for i in range(nChannels):
        chan = channelList[i]
        chan.stopMonitor()

    endTime = time.time()
    timediff = endTime - startTime
    print("put")
    startPut = time.time()
    for i in range(nChannels):
        chan = channelList[i]
        chan.put(1.0)
    endPut = time.time()
    lenPut = endPut - startPut
    print("seconds for put"),;print(lenPut)
    print("get")
    startGet = time.time()
    for i in range(nChannels):
        name = nameList[i]
        chan = channelList[i]
        value = chan.get().getDouble()
        if i==(nChannels-1) :
            print(name),;print(value)
    endGet = time.time()
    print("provider"),;print(provider),;print("number of channels"),;print(nChannels)
    lenGet = endGet - startGet
    print("seconds for get"),;print(lenGet)
    print("seconds to create channels and monitor"),;print(timediff)
    totalReceived = 0
    totalMissed = 0
    for i in range(nChannels):
        name = nameList[i]
        monitor = monitorList[i]
        totalReceived += monitor.nReceived
        totalMissed += monitor.nMissed
    print('TOTAL RECEIVED '),;print(totalReceived)
    print('TOTAL MISSED' ),;print(totalMissed)
    ans = input('enter "exit" : ')
    while ans != "exit" :
        print(ans)
        ans = input('enter "exit" :')
    del nameList[:]
    del channelList[:]
    del monitorList[:]
    time.sleep(1)
    
    

