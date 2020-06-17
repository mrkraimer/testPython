TOP=..

include $(TOP)/configure/CONFIG

EPICS_BASE_PVA_CORE_LIBS = pvDatabase pvaClient pvAccess pvAccessCA nt pvData ca Com

INC += pv/mandelbrotRecord.h
INC += pv/qt2dimageRecord.h

DBD += mandelbrotRecordRegister.dbd
DBD += qt2dimageRecordRegister.dbd

LIBRARY = testPython
LIBSRCS = mandelbrotRecord.cpp
LIBSRCS += mandelbrotRecordRegister.cpp
LIBSRCS += qt2dimageRecord.cpp
LIBSRCS += qt2dimageRecordRegister.cpp

testPython_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)

include $(TOP)/configure/RULES

