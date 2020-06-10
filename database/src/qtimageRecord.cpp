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
#include "pv/qtimageRecord.h"

using namespace epics::pvData;
using namespace epics::pvDatabase;
using std::tr1::static_pointer_cast;
using std::string;
using std::cout;

namespace epics { namespace testPython {


QtimageRecordPtr QtimageRecord::create(
    string const & recordName)
{
    StandardFieldPtr standardField = getStandardField();
    FieldCreatePtr fieldCreate = getFieldCreate();
    PVDataCreatePtr pvDataCreate = getPVDataCreate();
    UnionConstPtr union_t = getFieldCreate()->createFieldBuilder()->
        addArray("uint8",pvUByte)->
        addArray("uint18",pvUShort)->
        createUnion();
    StructureConstPtr  topStructure = fieldCreate->createFieldBuilder()->
        add("timeStamp",standardField->timeStamp()) ->
        add("name",pvString) ->
        addArray("x",pvDouble)->
        addArray("y",pvDouble)->
        add("xmin",pvDouble)->
        add("xmax",pvDouble)->
        add("ymin",pvDouble)->
        add("ymax",pvDouble)->
        addNestedStructure("argument")->
            addNestedStructure("format")->
                add("index",pvInt)->
                addArray("choices",pvString)->
                endNested()->
            add("height",pvInt)->
            add("width",pvInt)->
            endNested()->
        addNestedStructure("result") ->
            add("value",union_t) ->
            endNested()->
        createStructure();
    PVStructurePtr pvStructure = pvDataCreate->createPVStructure(topStructure);
    QtimageRecordPtr pvRecord(
        new QtimageRecord(recordName,pvStructure));
    pvStructure->getSubField<PVInt>("argument.height")->put(800);
    pvStructure->getSubField<PVInt>("argument.width")->put(800);
    shared_vector<string> choices(2);
    choices[0] = "Grayscale8";
    choices[1] = "RGB888";
    PVStringArrayPtr pvChoices = pvStructure->getSubField<PVStringArray>("argument.format.choices");
    pvChoices->replace(freeze(choices));
    pvStructure->getSubField<PVInt>("argument.format.index")->put(1);
    pvRecord->initPVRecord();
    return pvRecord;
}

QtimageRecord::QtimageRecord(
    string const & recordName,
    PVStructurePtr const & pvStructure)
: PVRecord(recordName,pvStructure)
{

}

void QtimageRecord::createGrayscale8(int height,int width)
{
    size_t num = width*height;
    epics::pvData::shared_vector<uint8_t> value(num,255);
    double xmin = getPVStructure()->getSubField<PVDouble>("xmin")->get();
    double xmax = getPVStructure()->getSubField<PVDouble>("xmax")->get();
    double ymin = getPVStructure()->getSubField<PVDouble>("ymin")->get();
    double ymax = getPVStructure()->getSubField<PVDouble>("ymax")->get();
    if(xmax>xmin && ymax>ymin) {
        double xinc = width/(xmax-xmin);
        double yinc = height/(ymax-ymin);
        PVScalarArrayPtr pvScalarArray = getPVStructure()->getSubField<PVDoubleArray>("x");
        shared_vector<const double> xarr;
        pvScalarArray->getAs<const double>(xarr);
        pvScalarArray = getPVStructure()->getSubField<PVDoubleArray>("y");
        shared_vector<const double> yarr;
        pvScalarArray->getAs<const double>(yarr);
        if(xarr.size()!=yarr.size()) {
                throw std::logic_error("x.size() ne y.size()");
        }
        int npts = xarr.size();
        int numpix = height*width;
        for(int ind=0; ind<npts; ind++)
        {
            double xnow =  (xarr[ind]-xmin)*xinc;
            double ynow =  (yarr[ind]-ymin)*yinc;
            int indx = int(xnow);
            int indy = int(ynow);
            int indpix = indy*width + indx;
            if(indpix>=numpix) continue;
            value[indpix] = 0;
        }
    }
    PVScalarArrayPtr arr = getPVDataCreate()->createPVScalarArray(pvUByte);
    PVUByteArrayPtr pvValue = std::tr1::static_pointer_cast<PVUByteArray>(arr);
    pvValue->putFrom(freeze(value));
    PVStructurePtr pvResult = getPVStructure()->getSubField<PVStructure>("result");
    PVUnionPtr pvUnion = std::tr1::static_pointer_cast<PVUnion>(pvResult->getSubField("value"));
    pvUnion->set("uint8",pvValue);
}

void QtimageRecord::createBGR888(int height,int width)
{
    int nz = 3;
    size_t num = width*height*nz;
    epics::pvData::shared_vector<uint8_t> value(num,255);
    double xmin = getPVStructure()->getSubField<PVDouble>("xmin")->get();
    double xmax = getPVStructure()->getSubField<PVDouble>("xmax")->get();
    double ymin = getPVStructure()->getSubField<PVDouble>("ymin")->get();
    double ymax = getPVStructure()->getSubField<PVDouble>("ymax")->get();
    if(xmax>xmin && ymax>ymin) {
        double xinc = width/(xmax-xmin);
        double yinc = height/(ymax-ymin);
        PVScalarArrayPtr pvScalarArray = getPVStructure()->getSubField<PVDoubleArray>("x");
        shared_vector<const double> xarr;
        pvScalarArray->getAs<const double>(xarr);
        pvScalarArray = getPVStructure()->getSubField<PVDoubleArray>("y");
        shared_vector<const double> yarr;
        pvScalarArray->getAs<const double>(yarr);
        if(xarr.size()!=yarr.size()) {
                throw std::logic_error("x.size() ne y.size()");
        }
        int npts = xarr.size();
        int numpix = height*width*nz;
        for(int ind=0; ind<npts; ind++)
        {
            double xnow =  (xarr[ind]-xmin)*xinc;
            double ynow =  (yarr[ind]-ymin)*yinc;
            int indx = int(xnow);
            int indy = int(ynow);
            int indpix = indy*width*nz + indx*nz;
            if(indpix>=numpix) continue;
            value[indpix] = 0;
            value[indpix+1] = 0;
            value[indpix+2] = 0;
        }
    }
    
    PVScalarArrayPtr arr = getPVDataCreate()->createPVScalarArray(pvUByte);
    PVUByteArrayPtr pvValue = std::tr1::static_pointer_cast<PVUByteArray>(arr);
    pvValue->putFrom(freeze(value));
    PVStructurePtr pvResult = getPVStructure()->getSubField<PVStructure>("result");
    PVUnionPtr pvUnion = std::tr1::static_pointer_cast<PVUnion>(pvResult->getSubField("value"));
    pvUnion->set("uint8",pvValue);
}

void QtimageRecord::createImage()
{
    PVStructurePtr pvArgument = getPVStructure()->getSubField<PVStructure>("argument");
    int height = pvArgument->getSubField<PVInt>("height")->get();
    int width = pvArgument->getSubField<PVInt>("width")->get();
    int choice = pvArgument->getSubField<PVInt>("format.index")->get();
    switch (choice) {
        case 0:
            createGrayscale8(height,width);
            break;
        case 1:
            createBGR888(height,width);
            break;
        default:
            cout << "unsupported format\n";
    }
}

void QtimageRecord::process()
{
    createImage();
}

}}
