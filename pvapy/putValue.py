from pvaccess import Channel, CA, PvTimeStamp, PvAlarm
channel = Channel('PVRdouble')
print('start value=',channel.get('value,alarm,timeStamp'))
for i in range(5) :
    channel.put(i)
    print('after put  value=',channel.get())

