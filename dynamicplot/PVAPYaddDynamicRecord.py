#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from pvaccess import *
import numpy as np
from pvaccess import *

chan = Channel("PVRaddRecord")
pvAddRecord = chan.get('field(argument)')
print('pvAddRecord=',pvAddRecord)
channelStructure = ChannelStructure()
print('Dynamic_Channel_Provider().getChannelName()',Dynamic_Channel_Provider().getChannelName())
struct = channelStructure.get()
print('struct=',struct)
pvAddRecord['argument']['recordName'] = Dynamic_Channel_Provider().getChannelName()
pvAddRecord['argument']['union'] = struct
print('pvAddRecord=',pvAddRecord)
result = chan.putGet(pvAddRecord,'putField(argument)getField(result)')
print(result)

