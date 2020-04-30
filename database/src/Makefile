TOP=..

include $(TOP)/configure/CONFIG

EPICS_BASE_PVA_CORE_LIBS = pvDatabase pvaClient pvAccess pvAccessCA nt pvData ca Com

INC += pv/mandelbrotRecord.h

DBD += mandelbrotRecordRegister.dbd

LIBRARY = mandelbrotRecord
LIBSRCS = mandelbrotRecord.cpp
LIBSRCS += mandelbrotRecordRegister.cpp

mandelbrotRecord_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)

include $(TOP)/configure/RULES

