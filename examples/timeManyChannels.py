#!/usr/bin/env python

#
# This example can be used to monitor large number of channels with slow 
# updates.
#

import sys
import time
from pvaccess import Channel,CA

if __name__ == '__main__':
    nChannels = 2
    provider = "pva"
    if len(sys.argv) > 1:
        nChannels = int(sys.argv[1])
    if len(sys.argv) > 2:
        provider = sys.argv[2]
    nameList = list()
    channelList = list()
    startChannel = time.time()
    for channelCnt in range(1,nChannels+1):
        channelName = 'X%s' % channelCnt
        nameList.append(channelName)
        if provider == "ca" :
            c = Channel(channelName,CA)
        else :
            c = Channel(channelName)
        channelList.append(c);
    endChannel = time.time()
    print("get")
    startGet1 = time.time()
    for i in range(nChannels):
        name = nameList[i]
        chan = channelList[i]
        print(name),;print(chan.get().getDouble())
    endGet1 = time.time()
    print("put")
    startPut = time.time()
    for i in range(nChannels):
        chan = channelList[i]
        chan.put(1.0)
    endPut = time.time()
    print("get")
    startGet2 = time.time()
    for i in range(nChannels):
        name = nameList[i]
        chan = channelList[i]
        print(name),;print(chan.get().getDouble())
    endGet2 = time.time()
    print("provider"),;print(provider),;print("number of channels"),;print(nChannels)
    lenChannel = endChannel - startChannel
    print("seconds to create channels"),;print(lenChannel)
    lenGet1 = endGet1 - startGet1
    print("seconds for first get"),;print(lenGet1)
    lenPut = endPut - startPut
    print("seconds for put"),;print(lenPut)
    lenGet2 = endGet2 - startGet2
    print("seconds for second get"),;print(lenGet2)
    

