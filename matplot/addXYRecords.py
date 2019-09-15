#!/usr/bin/env python

import numpy as np
from pvaccess import *

timeStamp = PvTimeStamp()
structValue = PvObject({'value':{'timeStamp':timeStamp,'value':[DOUBLE]}})
print(structValue)
addRecordValue = PvObject({'argument':{'recordName':STRING,'union':()}})
addRecordValue['argument.union'] = structValue;
print(addRecordValue)
chan = Channel("PVRaddRecord")
addRecordValue['argument.recordName'] = 'x';
print(addRecordValue)
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)
addRecordValue['argument.recordName'] = 'y';
print(addRecordValue)
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)

