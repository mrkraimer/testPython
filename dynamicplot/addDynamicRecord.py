#!/usr/bin/env python
from Dynamic_Viewer import Dynamic_Channel_Provider
from pvaccess import *
import numpy as np
from pvaccess import *

name = Dynamic_Channel_Provider().getChannelName()

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
chan = Channel("PVRaddRecord")
addRecordValue['argument.recordName'] = str(name);
result = chan.putGet(addRecordValue,'putField(argument)getField(result)')
print(result)

