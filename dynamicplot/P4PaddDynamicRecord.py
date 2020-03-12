#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure,Dynamic_Channel_Provider
from p4p.client.thread import Context,Type,Value
import numpy as np
ctxt = Context('pva')
pvAddRecord = ctxt.get('PVRaddRecord')
print('pvAddRecord=',pvAddRecord)
channelStructure = ChannelStructure()
print('Dynamic_Channel_Provider().getChannelName()',Dynamic_Channel_Provider().getChannelName())
struct = channelStructure.get()
print('struct=',struct)
pvAddRecord['argument']['recordName'] = Dynamic_Channel_Provider().getChannelName()
pvAddRecord['argument']['union'] = struct
ctxt.put('PVRaddRecord',)


