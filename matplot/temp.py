#!/usr/bin/env python

import numpy as np
from pvaccess import *

timeStamp = PvTimeStamp()
structValue = PvObject({'value':{'timeStamp':timeStamp,'value':[DOUBLE]}})
print(structValue)
addRecordValue = PvObject({'argument':{'recordName':STRING,'union':()}})
addRecordValue['argument.recordName'] = 'x'
addRecordValue['argument.union'] = structValue;
print(addRecordValue)

