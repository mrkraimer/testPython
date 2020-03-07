#!/usr/bin/env python
from Dynamic_Viewer import ChannelStructure
from pvaccess import *
import numpy as np
from pvaccess import *

struct = ChannelStructure()
structValue = PvObject({'value':struct.get()})
addRecordValue = PvObject({'argument':{'recordName':STRING,'union':()}})
addRecordValue['argument.union'] = structValue;
chan = Channel("PVRaddRecord")
addRecordValue['argument.recordName'] = 'dynamicRecord';
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)

