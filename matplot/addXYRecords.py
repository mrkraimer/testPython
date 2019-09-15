#!/usr/bin/env python

import numpy as np
from pvaccess import *

timeStamp = PvTimeStamp()
structValue = PvObject({'value':{'timeStamp':timeStamp,'value':[DOUBLE]}})
addRecordValue = PvObject({'argument':{'recordName':STRING,'union':()}})
addRecordValue['argument.union'] = structValue;
chan = Channel("PVRaddRecord")
addRecordValue['argument.recordName'] = 'x';
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)
addRecordValue['argument.recordName'] = 'y';
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)

