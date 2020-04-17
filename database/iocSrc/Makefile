TOP=..

include $(TOP)/configure/CONFIG

#=============================
# build an ioc application

DBD += mandelbrotDatabase.dbd

PROD_IOC += mandelbrotDatabase


# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
mandelbrotDatabase_SRCS += mandelbrotDatabase_registerRecordDeviceDriver.cpp
mandelbrotDatabase_SRCS_DEFAULT += mandelbrotDatabaseMain.cpp
mandelbrotDatabase_SRCS_vxWorks += -nil-


# The following adds support from base/src/vxWorks
mandelbrotDatabase_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

mandelbrotDatabase_LIBS += mandelbrotRecord
mandelbrotDatabase_LIBS += pvDatabase qsrv pvaClient pvAccessIOC pvAccess pvAccessCA nt pvData

mandelbrotDatabase_LIBS += $(EPICS_BASE_IOC_LIBS)

PROD_SYS_LIBS_WIN32 += ws2_32

include $(TOP)/configure/RULES

