# testPvaPy

This contains code for testing pvaPy

## testpath

This is an example of setting the path to **pvaPy**.
Edit this file to specify where you have built pvaPy.
Then use it to create your **PYTHONPATH**.

## database for examples

The examples assume the a database containing 50000 calc records is running.

An example database is in **https://github.com/mrkraimer/testDatabaseCPP**

To run the example database:

    mrk> pwd
    /home/epicsv4/masterCPP/testDatabaseCPP/iocBoot/manyDBRecords
    mrk> ../../bin/linux-x86_64/manyDBRecords st.cmd


## monitorN.py

This issues monitors on up to 50000 channels and allows the user to specify the channel provider.
Examples are:

      mrk> pwd
      /home/epicsv4/masterCPP/testPvaPy/examples
      mrk> source ../setpath 
      mrk> python monitorN.py 50000 pva

and

      mrk> pwd
      /home/epicsv4/masterCPP/testPvaPy/examples
      mrk> source ../setpath 
      mrk> python monitorN.py 50000 ca


## monitorPutGetN.py

This is like **monitorN.py** but after the monitors have all connected a put and then a get is issued
for each channel.

Note that if the monitors are not issued before the put and get, then each put causes a wait for the channel to connect. It taks a **LONG** time for 50000 channels to connect.

Examples are:

      mrk> pwd
      /home/epicsv4/masterCPP/testPvaPy/examples
      mrk> source ../setpath 
      mrk> python monitorPutGetN.py 50000 pva

and

      mrk> pwd
      /home/epicsv4/masterCPP/testPvaPy/examples
      mrk> source ../setpath 
      mrk> python monitorPutGetN.py 50000 ca






