< envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase("dbd/mandelbrotDatabase.dbd")
mandelbrotDatabase_registerRecordDeviceDriver(pdbbase

cd ${TOP}/iocBoot/${IOC}
iocInit()

addRecordCreate TPYaddRecord
removeRecordCreate TPYremoveRecord
traceRecordCreate TPYtraceRecord
mandelbrotRecordCreate TPYmandelbrotRecord

