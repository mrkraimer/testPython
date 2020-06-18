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
#include "pv/qtpeakimageRecord.h"

using namespace epics::pvData;
using namespace epics::pvDatabase;
using std::tr1::static_pointer_cast;
using std::string;
using std::cout;

namespace epics { namespace testPython {


QtpeakimageRecordPtr QtpeakimageRecord::create(
    string const & recordName)
{
    StandardFieldPtr standardField = getStandardField();
    FieldCreatePtr fieldCreate = getFieldCreate();
    PVDataCreatePtr pvDataCreate = getPVDataCreate();
    UnionConstPtr union_t = getFieldCreate()->createFieldBuilder()->
        addArray("uint8",pvUByte)->
        addArray("uint16",pvUShort)->
        addArray("uint32",pvUInt)->
        createUnion();
    StructureConstPtr  topStructure = fieldCreate->createFieldBuilder()->
        add("timeStamp",standardField->timeStamp()) ->
        addNestedStructure("peak")->
            add("x",pvDouble)->
            add("xwidth",pvDouble)->
            add("y",pvDouble)->
            add("ywidth",pvDouble)->
            add("intensity",pvDouble)->
            endNested()->
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
    QtpeakimageRecordPtr pvRecord(
        new QtpeakimageRecord(recordName,pvStructure));
    pvStructure->getSubField<PVInt>("argument.height")->put(800);
    pvStructure->getSubField<PVInt>("argument.width")->put(800);
    shared_vector<string> choices(4);
    choices[0] = "Grayscale8";
    choices[1] = "Indexed8";
    choices[2] = "RGB888";
    choices[3] = "Grayscale16";
    PVStringArrayPtr pvChoices = pvStructure->getSubField<PVStringArray>("argument.format.choices");
    pvChoices->replace(freeze(choices));
    pvStructure->getSubField<PVInt>("argument.format.index")->put(0);
    pvStructure->getSubField<PVDouble>("peak.x")->put(100);
    pvStructure->getSubField<PVDouble>("peak.xwidth")->put(50.0);
    pvStructure->getSubField<PVDouble>("peak.y")->put(200);
    pvStructure->getSubField<PVDouble>("peak.ywidth")->put(50.0);
    pvStructure->getSubField<PVDouble>("peak.intensity")->put(1.0);
    pvRecord->initPVRecord();
    return pvRecord;
}

QtpeakimageRecord::QtpeakimageRecord(
    string const & recordName,
    PVStructurePtr const & pvStructure)
: PVRecord(recordName,pvStructure)
{

}

void QtpeakimageRecord::createGrayscale8(int height,int width)
{
    size_t num = width*height;
    int maxvalue = 255;
    epics::pvData::shared_vector<uint8_t> value(num,0);
    double x = getPVStructure()->getSubField<PVDouble>("peak.x")->get();
    double xwidth = getPVStructure()->getSubField<PVDouble>("peak.xwidth")->get();
    double y = getPVStructure()->getSubField<PVDouble>("peak.y")->get();
    double ywidth = getPVStructure()->getSubField<PVDouble>("peak.ywidth")->get();
    double intensity = getPVStructure()->getSubField<PVDouble>("peak.intensity")->get();
    int pixvalue = maxvalue*intensity;
    if(intensity<0.0||intensity>1.0) {
        throw std::logic_error("intensity must be between 0 and 1");
    } 
    int ny = ywidth;
    int starty = y - ywidth/2;
    int endy = starty + ny;
    int nx = xwidth;
    int startx = x - xwidth/2;
    int endx = startx + nx;
    for(int indy = starty; indy<endy; indy++) {
        for(int indx = startx; indx<endx; indx++) {
            int indpix = int(indy*width + indx);
            value[indpix] = pixvalue;
        }
    }    
    PVScalarArrayPtr arr = getPVDataCreate()->createPVScalarArray(pvUByte);
    PVUByteArrayPtr pvValue = std::tr1::static_pointer_cast<PVUByteArray>(arr);
    pvValue->putFrom(freeze(value));
    PVStructurePtr pvResult = getPVStructure()->getSubField<PVStructure>("result");
    PVUnionPtr pvUnion = std::tr1::static_pointer_cast<PVUnion>(pvResult->getSubField("value"));
    pvUnion->set("uint8",pvValue);
}

void QtpeakimageRecord::createBGR888(int height,int width)
{
    int nz = 3;
    size_t num = width*height*nz;
    int maxvalue = 255;
    epics::pvData::shared_vector<uint8_t> value(num,0);
    double x = getPVStructure()->getSubField<PVDouble>("peak.x")->get();
    double xwidth = getPVStructure()->getSubField<PVDouble>("peak.xwidth")->get();
    double y = getPVStructure()->getSubField<PVDouble>("peak.y")->get();
    double ywidth = getPVStructure()->getSubField<PVDouble>("peak.ywidth")->get();
    double intensity = getPVStructure()->getSubField<PVDouble>("peak.intensity")->get();
    int pixvalue = maxvalue*intensity;
    if(intensity<0.0||intensity>1.0) {
        throw std::logic_error("intensity must be between 0 and 1");
    } 
    int ny = ywidth;
    int starty = y - ywidth/2;
    int endy = starty + ny;
    int nx = xwidth;
    int startx = x - xwidth/2;
    int endx = startx + nx;
    for(int indy = starty; indy<endy; indy++) {
        for(int indx = startx; indx<endx; indx++) {
            int indpix = int(indy*width*nz + indx*nz);
            value[indpix+1] = pixvalue; // set green
        }
    }    
    PVScalarArrayPtr arr = getPVDataCreate()->createPVScalarArray(pvUByte);
    PVUByteArrayPtr pvValue = std::tr1::static_pointer_cast<PVUByteArray>(arr);
    pvValue->putFrom(freeze(value));
    PVStructurePtr pvResult = getPVStructure()->getSubField<PVStructure>("result");
    PVUnionPtr pvUnion = std::tr1::static_pointer_cast<PVUnion>(pvResult->getSubField("value"));
    pvUnion->set("uint8",pvValue);
}


void QtpeakimageRecord::createGrayscale16(int height,int width)
{
    size_t num = width*height;
    int maxvalue = 65535;
    epics::pvData::shared_vector<uint16_t> value(num,0);
    double x = getPVStructure()->getSubField<PVDouble>("peak.x")->get();
    double xwidth = getPVStructure()->getSubField<PVDouble>("peak.xwidth")->get();
    double y = getPVStructure()->getSubField<PVDouble>("peak.y")->get();
    double ywidth = getPVStructure()->getSubField<PVDouble>("peak.ywidth")->get();
    double intensity = getPVStructure()->getSubField<PVDouble>("peak.intensity")->get();
    int pixvalue = maxvalue*intensity;
    if(intensity<0.0||intensity>1.0) {
        throw std::logic_error("intensity must be between 0 and 1");
    } 
    int ny = ywidth;
    int starty = y - ywidth/2;
    int endy = starty + ny;
    int nx = xwidth;
    int startx = x - xwidth/2;
    int endx = startx + nx;
    for(int indy = starty; indy<endy; indy++) {
        for(int indx = startx; indx<endx; indx++) {
            int indpix = int(indy*width + indx);
            value[indpix] = pixvalue;
        }
    }  
    PVScalarArrayPtr arr = getPVDataCreate()->createPVScalarArray(pvUShort);
    PVUShortArrayPtr pvValue = std::tr1::static_pointer_cast<PVUShortArray>(arr);
    pvValue->putFrom(freeze(value));
    PVStructurePtr pvResult = getPVStructure()->getSubField<PVStructure>("result");
    PVUnionPtr pvUnion = std::tr1::static_pointer_cast<PVUnion>(pvResult->getSubField("value"));
    pvUnion->set("uint16",pvValue);
}

void QtpeakimageRecord::createImage()
{
    PVStructurePtr pvArgument = getPVStructure()->getSubField<PVStructure>("argument");
    int height = pvArgument->getSubField<PVInt>("height")->get();
    int width = pvArgument->getSubField<PVInt>("width")->get();
    int choice = pvArgument->getSubField<PVInt>("format.index")->get();
    switch (choice) {
        case 0:
        case 1:
            createGrayscale8(height,width);
            break;
        case 2:
            createBGR888(height,width);
            break;
        case 3:
            createGrayscale16(height,width);
            break;
        default:
            cout << "unsupported format\n";
    }
}

void QtpeakimageRecord::process()
{
    createImage();
}

}}
