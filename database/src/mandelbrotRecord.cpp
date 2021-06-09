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
using std::cout;

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
            add("xmax",pvDouble)->
            add("ymin",pvDouble)->
            add("ymax",pvDouble)->
            add("nx",pvInt)->
            add("ny",pvInt)->
            add("nz",pvInt)->
            add("expz",pvInt)->
            endNested()->
        addNestedStructure("result") ->
            addArray("value",pvUByte) ->
            endNested()->
        createStructure();
    PVStructurePtr pvStructure = pvDataCreate->createPVStructure(topStructure);
    pvStructure->getSubField<PVInt>("argument.nz")->put(3);

    MandelbrotRecordPtr pvRecord(
        new MandelbrotRecord(recordName,pvStructure));
    pvRecord->initPVRecord();
    return pvRecord;
}

MandelbrotRecord::MandelbrotRecord(
    string const & recordName,
    PVStructurePtr const & pvStructure)
: PVRecord(recordName,pvStructure) {}

void MandelbrotRecord::expzCalc(double z[], int expz)
{
    double realorig = z[0];
    double imgorig = z[1];
    for(int ind=0; ind<(expz-1); ++ind) {
        double real = z[0]*realorig - z[1]*imgorig;
        double img = z[0]*imgorig + z[1]*realorig;
        z[0] = real;
        z[1] = img;
    }
}

void MandelbrotRecord::createImage()
{
    PVStructurePtr pvArgument = getPVStructure()->getSubField<PVStructure>("argument");
    double xmin = pvArgument->getSubField<PVDouble>("xmin")->get();
    double xmax = pvArgument->getSubField<PVDouble>("xmax")->get();
    double ymin = pvArgument->getSubField<PVDouble>("ymin")->get();
    double ymax = pvArgument->getSubField<PVDouble>("ymax")->get();
    int nx = pvArgument->getSubField<PVInt>("nx")->get();
    int ny = pvArgument->getSubField<PVInt>("ny")->get();
    int expz = pvArgument->getSubField<PVInt>("expz")->get();  
    double xinc = (xmax-xmin)/nx;
    double yinc = (ymax-ymin)/ny;
    double scaley = 1.0;
    double scalex = 1.0;
    double ratio = yinc/xinc;
    if(ratio>1.0) {
        scalex = ratio;
    } else {
        scaley = 1.0/ratio;
    }
    int nz = pvArgument->getSubField<PVInt>("nz")->get();
    size_t num = ny*nx*nz;
    epics::pvData::shared_vector<uint8_t> value(num,255);
    for(int indy=0; indy<ny; ++indy)
    {
        double y = ymin + indy*yinc*scaley;
        for(int indx=0; indx<nx; ++indx)
        {
             int indpix = indy*nx*nz + indx*nz;
             double x = xmin + indx*xinc*scalex;
             double c[2] = {x,y};
             double z[2] = {0.0,0.0};
             int intensity =0;
             for(int j=0; j<255; ++j)
             {
                 expzCalc(z,expz);
                 z[0] = z[0] + c[0];
                 z[1] = z[1] + c[1];
                 double absz = std::sqrt(z[0]*z[0] + z[1]*z[1]);
                 if(absz>=2.0) break;
                 intensity += 1;
             }
             intensity = 255 - intensity;
             if(nz==1) {
                // Color scheme is grayscale
                value[indpix] = intensity;
             } else {
                 // Color scheme is that of Julia sets
                 value[indpix] = intensity % 8 * 32;
                 value[indpix+1] = intensity % 16 * 16;
                 value[indpix+2] = intensity % 32 * 8;
             }
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
