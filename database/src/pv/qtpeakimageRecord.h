/*
 * Copyright information and license terms for this software can be
 * found in the file LICENSE that is included with the distribution
 */

/**
 * @author mrk
 * @date 2013.04.02
 */
#ifndef QTPEAKIMAGERECORD_H
#define QTPEAKIMAGERECORD_H


#include <pv/pvDatabase.h>
#include <pv/timeStamp.h>
#include <pv/pvTimeStamp.h>

#include <shareLib.h>


namespace epics { namespace testPython {


class QtpeakimageRecord;
typedef std::tr1::shared_ptr<QtpeakimageRecord> QtpeakimageRecordPtr;

/**
 * @brief A PVRecord that implements a hello service accessed via a channelPutGet request.
 *
 */
class epicsShareClass QtpeakimageRecord :
    public epics::pvDatabase::PVRecord
{
public:
    POINTER_DEFINITIONS(QtpeakimageRecord);
    /**
     * @brief Create an instance of QtpeakimageRecord.
     *
     * @param recordName The name of the record.
     * @return The new instance.
     */
    static QtpeakimageRecordPtr create(
        std::string const & recordName);
    /**
     *  @brief Implement hello semantics.
     */
    virtual void process();
    virtual ~QtpeakimageRecord() {}
    virtual bool init() {return false;}
    void createImage();
    
private:
    void createGrayscale8(int height,int width);
    void createBGR888(int height,int width);
    void createGrayscale16(int height,int width);
    QtpeakimageRecord(std::string const & recordName,
        epics::pvData::PVStructurePtr const & pvStructure);

};


}}

#endif  /* QTPEAKIMAGERECORD_H */
