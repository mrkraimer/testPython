TOP=..

include $(TOP)/configure/CONFIG

#=============================
# build an ioc application

DBD += testPython.dbd

PROD_IOC += testPython


# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
testPython_SRCS += testPython_registerRecordDeviceDriver.cpp
testPython_SRCS_DEFAULT += testPythonMain.cpp
testPython_SRCS_vxWorks += -nil-


# The following adds support from base/src/vxWorks
testPython_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

testPython_LIBS += testPython
testPython_LIBS += pvDatabase qsrv pvaClient pvAccessIOC pvAccess pvAccessCA nt pvData

testPython_LIBS += $(EPICS_BASE_IOC_LIBS)

PROD_SYS_LIBS_WIN32 += ws2_32

include $(TOP)/configure/RULES

