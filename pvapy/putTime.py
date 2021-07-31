from pvapy import Channel, PvTimeStamp
channel = Channel('PVRdouble')
print('start value\n',channel.get('timeStamp'))
timestamp = PvTimeStamp(10, 100,1)
channel.put(timestamp,'record[process=false]field(timeStamp)')
val = channel.get('value,alarm,timeStamp')
print('after put timeStamp value\n',channel.get('timeStamp'))
timestamp = PvTimeStamp(0, 0,0)
channel.put(timestamp,'record[process=false]field(timeStamp)')
val = channel.get('value,alarm,timeStamp')
print('after put timeStamp value\n',channel.get('timeStamp'))

