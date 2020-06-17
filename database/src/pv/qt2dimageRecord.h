/*
 * Copyright information and license terms for this software can be
 * found in the file LICENSE that is included with the distribution
 */

/**
 * @author mrk
 * @date 2013.04.02
 */
#ifndef QT2DIMAGERECORD_H
#define QT2DIMAGERECORD_H


#include <pv/pvDatabase.h>
#include <pv/timeStamp.h>
#include <pv/pvTimeStamp.h>

#include <shareLib.h>


namespace epics { namespace testPython {


class Qt2dimageRecord;
typedef std::tr1::shared_ptr<Qt2dimageRecord> Qt2dimageRecordPtr;

/**
 * @brief A PVRecord that implements a hello service accessed via a channelPutGet request.
 *
 */
class epicsShareClass Qt2dimageRecord :
    public epics::pvDatabase::PVRecord
{
public:
    POINTER_DEFINITIONS(Qt2dimageRecord);
    /**
     * @brief Create an instance of Qt2dimageRecord.
     *
     * @param recordName The name of the record.
     * @return The new instance.
     */
    static Qt2dimageRecordPtr create(
        std::string const & recordName);
    /**
     *  @brief Implement hello semantics.
     */
    virtual void process();
    virtual ~Qt2dimageRecord() {}
    virtual bool init() {return false;}
    void createImage();
    
private:
    void createGrayscale8(int height,int width);
    void createBGR888(int height,int width);
    void createGrayscale16(int height,int width);
    Qt2dimageRecord(std::string const & recordName,
        epics::pvData::PVStructurePtr const & pvStructure);

};


}}

#endif  /* QT2DIMAGERECORD_H */
