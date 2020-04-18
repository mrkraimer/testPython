#!/usr/bin/env python
from Dynamic_Common import getAddRecordName,getDynamicRecordName
from p4p.client.thread import Context,Type,Value
import numpy as np
ctxt = Context('pva')
pvAddRecord = ctxt.get(getAddRecordName())
print('pvAddRecord=',pvAddRecord)

struct = Value(Type([
   ('name', 's'),
   ('x', 'ad'),
   ('y', 'ad'),
   ('xmin', 'd'),
   ('xmax', 'd'),
   ('ymin', 'd'),
   ('ymax', 'd'),
]))

pvAddRecord['argument']['recordName'] = getDynamicRecordName()
pvAddRecord['argument']['union'] = struct
ctxt.put(getAddRecordName(),pvAddRecord)


