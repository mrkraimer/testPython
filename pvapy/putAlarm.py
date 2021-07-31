
from pvaccess import Channel, PvAlarm
channel = Channel('PVRdouble')
alarm = PvAlarm(1,2,"message")
print('alarm=',alarm)
channel.put(alarm,'alarm')
print('after put alarm value\n',channel.get('alarm'))
alarm = PvAlarm(0,0,"")
print('alarm=',alarm)
channel.put(alarm,'alarm')
print('after put alarm value/n',channel.get('alarm'))
