from pvapy import Channel, PvTimeStamp
channel = Channel('PVRdouble')
timestamp = PvTimeStamp(10, 100,1)
print('start value=',channel.get('timeStamp'))
channel.put(10,'record[process=false]field(timeStamp.secondsPastEpoch)')
channel.put(10000,'record[process=false]field(timeStamp.nanoseconds)')
val = channel.get('value,alarm,timeStamp')
print('after put timeStamp value=',channel.get('timeStamp'))

