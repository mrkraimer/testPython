< envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase("dbd/testPython.dbd")
testPython_registerRecordDeviceDriver(pdbbase)
dbLoadRecords("db/dbCounter.db","name=TPYcounter01")

iocInit()

addRecordCreate TPYaddRecord
removeRecordCreate TPYremoveRecord
traceRecordCreate TPYtraceRecord
mandelbrotRecordCreate TPYmandelbrotRecord
qtimageRecordCreate TPYqtimageRecord

