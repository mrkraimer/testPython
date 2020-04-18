#!/usr/bin/env python
from Dynamic_Common import getAddRecordName,getDynamicRecordName
from pvaccess import *
import numpy as np

chan = Channel(getAddRecordName())
pvAddRecord = chan.get('field(argument)')
print('pvAddRecord=',pvAddRecord)
struct = PvObject(\
      {   'name':STRING\
          ,'x':[DOUBLE]\
          ,'y':[DOUBLE]\
          ,'xmin':DOUBLE\
          ,'xmax':DOUBLE\
          ,'ymin':DOUBLE\
          ,'ymax':DOUBLE\
      })
structValue = PvObject({'value':struct})
addRecordValue = PvObject({'argument':{'recordName':STRING,'union':()}})
addRecordValue['argument.union'] = structValue;
chan = Channel("TPYaddRecord")
addRecordValue['argument.recordName'] = getDynamicRecordName()
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)
