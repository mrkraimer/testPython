# testPython 2020.04.18

This contains example python code as well as code for testing pvaPy and p4p

## database 

This is a database used by some of the python examples, e. g. **plot2dcurves** and **mandelbrot** both use it.

##plot2dcurves##

This has it's own **README.md**.

## mandelbrot

This has it's own **README.md**.

## setpathPVAPY

This is an example of setting the path to **pvaPy**.
Edit this file to specify where you have built pvaPy.
Then use it to create your **PYTHONPATH**.

## database for some test examples

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
      /home/epicsv4/masterCPP/testPython/examples
      mrk> source ../setpath 
      mrk> python monitorN.py 50000 pva

and

      mrk> pwd
      /home/epicsv4/masterCPP/testPython/examples
      mrk> source ../setpath 
      mrk> python monitorN.py 50000 ca


## monitorPutGetN.py

This is like **monitorN.py** but after the monitors have all connected a put and then a get is issued
for each channel.

Note that if the monitors are not issued before the put and get, then each put causes a wait for the channel to connect. It taks a **LONG** time for 50000 channels to connect.

Examples are:

      mrk> pwd
      /home/epicsv4/masterCPP/testPython/examples
      mrk> source ../setpath 
      mrk> python monitorPutGetN.py 50000 pva

and

      mrk> pwd
      /home/epicsv4/masterCPP/testPython/examples
      mrk> source ../setpath 
      mrk> python monitorPutGetN.py 50000 ca






