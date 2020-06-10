TOP=..

include $(TOP)/configure/CONFIG

EPICS_BASE_PVA_CORE_LIBS = pvDatabase pvaClient pvAccess pvAccessCA nt pvData ca Com

INC += pv/mandelbrotRecord.h
INC += pv/qtimageRecord.h

DBD += mandelbrotRecordRegister.dbd
DBD += qtimageRecordRegister.dbd

LIBRARY = testPython
LIBSRCS = mandelbrotRecord.cpp
LIBSRCS += mandelbrotRecordRegister.cpp
LIBSRCS += qtimageRecord.cpp
LIBSRCS += qtimageRecordRegister.cpp

testPython_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)

include $(TOP)/configure/RULES

