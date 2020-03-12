# Dynamic_Common.py

import os

def getDynamicRecordName() :
    name = os.getenv('DYNAMIC_RECORDNAME')
    if name== None : return(str('dynamicRecord'))
    return str(name)

def getAddRecordName() :
    name = os.getenv('ADD_RECORDNAME')
    if name== None : return(str('PVRaddRecord'))
    return str(name)


