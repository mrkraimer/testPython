/*
 * Copyright information and license terms for this software can be
 * found in the file LICENSE that is included with the distribution
 */

/**
 * @author mrk
 * @date 2013.07.24
 */


/* Author: Marty Kraimer */

#include <iocsh.h>
#include <pv/pvDatabase.h>
#include <pv/channelProviderLocal.h>

// The following must be the last include for code database uses
#include <epicsExport.h>
#define epicsExportSharedSymbols
#include "pv/qt2dimageRecord.h"

using namespace epics::pvData;
using namespace epics::pvAccess;
using namespace epics::pvDatabase;
using namespace epics::testPython;
using namespace std;

static const iocshArg testArg0 = { "recordName", iocshArgString };
static const iocshArg *testArgs[] = {
    &testArg0};

static const iocshFuncDef qt2dimageRecordFuncDef = {"qt2dimageRecordCreate", 1,testArgs};

static void qt2dimageRecordCallFunc(const iocshArgBuf *args)
{
    char *recordName = args[0].sval;
    if(!recordName) {
        throw std::runtime_error("qt2dimageRecordCreate invalid number of arguments");
    }
    Qt2dimageRecordPtr record = Qt2dimageRecord::create(recordName);
    bool result = PVDatabase::getMaster()->addRecord(record);
    if(!result) cout << "recordname" << " not added" << endl;
}

static void qt2dimageRecordRegister(void)
{
    static int firstTime = 1;
    if (firstTime) {
        firstTime = 0;
        iocshRegister(&qt2dimageRecordFuncDef, qt2dimageRecordCallFunc);
    }
}

extern "C" {
    epicsExportRegistrar(qt2dimageRecordRegister);
}
