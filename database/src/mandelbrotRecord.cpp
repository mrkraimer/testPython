/*
 * Copyright information and license terms for this software can be
 * found in the file LICENSE that is included with the distribution
 */

/**
 * @author mrk
 * @date 2013.04.02
 */

#include <cmath>
#include <pv/pvDatabase.h>
#include <pv/standardField.h>

#define epicsExportSharedSymbols
#include "pv/mandelbrotRecord.h"

using namespace epics::pvData;
using namespace epics::pvDatabase;
using std::tr1::static_pointer_cast;
using std::string;

namespace epics { namespace testPython {


MandelbrotRecordPtr MandelbrotRecord::create(
    string const & recordName)
{
    StandardFieldPtr standardField = getStandardField();
    FieldCreatePtr fieldCreate = getFieldCreate();
    PVDataCreatePtr pvDataCreate = getPVDataCreate();
    StructureConstPtr  topStructure = fieldCreate->createFieldBuilder()->
        add("timeStamp",standardField->timeStamp()) ->
        addNestedStructure("argument")->
            add("xmin",pvDouble)->
            add("xinc",pvDouble)->
            add("ymin",pvDouble)->
            add("yinc",pvDouble)->
            add("width",pvInt)->
            add("height",pvInt)->
            endNested()->
        addNestedStructure("result") ->
            addArray("value",pvUByte) ->
            endNested()->
        createStructure();
    PVStructurePtr pvStructure = pvDataCreate->createPVStructure(topStructure);

    MandelbrotRecordPtr pvRecord(
        new MandelbrotRecord(recordName,pvStructure));
    pvRecord->initPVRecord();
    return pvRecord;
}

MandelbrotRecord::MandelbrotRecord(
    string const & recordName,
    PVStructurePtr const & pvStructure)
: PVRecord(recordName,pvStructure)
{

}

int MandelbrotRecord::calcIntensity(double x,double y)
{
    double c[2] = {x,y};
    double z[2] = {0.0,0.0};
    int i =0;
    for(int j=0; j<255; ++j)
    {
        double absz = std::sqrt(z[0]*z[0] + z[1]*z[1]);
        if(absz>=2.0) break;
        i += 1;
        double xz = z[0]*z[0] - z[1]*z[1] + c[0];
        double yz = 2.0*z[0]*z[1] + c[1];
        z[0] = xz;
        z[1] = yz;
    }
    return i;
}

void MandelbrotRecord::createImage()
{
    PVStructurePtr pvArgument = getPVStructure()->getSubField<PVStructure>("argument");
    double xmin = pvArgument->getSubField<PVDouble>("xmin")->get();
    double xinc = pvArgument->getSubField<PVDouble>("xinc")->get();
    double ymin = pvArgument->getSubField<PVDouble>("ymin")->get();
    double yinc = pvArgument->getSubField<PVDouble>("yinc")->get();
    int height = pvArgument->getSubField<PVInt>("height")->get();
    int width = pvArgument->getSubField<PVInt>("width")->get();
    size_t num = width*height*3;
    epics::pvData::shared_vector<uint8_t> value(num,255);
    for(int indy=0; indy<height; ++indy)
    {
        double y = ymin + indy*yinc;
        for(int indx=0; indx<width; ++indx)
        {
             double x = xmin + indx*xinc;
             int  intensity = calcIntensity(x,y);
             int ind = indx*height*3 +indy*3;
             // Color scheme is that of Julia sets
             value[ind] = intensity % 8 * 32;
             value[ind+1] = intensity % 16 * 16;
             value[ind+2] = intensity % 32 * 8;
        }
    }
    PVUByteArrayPtr pvValue= getPVStructure()->getSubField<PVUByteArray>("result.value");
    pvValue->putFrom(freeze(value));
}

void MandelbrotRecord::process()
{
    createImage();
}

}}
