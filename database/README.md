# database

This creates an IOC database that is used by some of the Python examples.
In particular **mandelbrot** and **plot2dcurves**.
When the IOC is started it has the following PVRecords:
**TPYaddRecord**,**TPYremoveRecord**,**TPYtraceRecord**,and **TPYmandelbrotRecord**.
The code for the first three are implemented by **pvDatabaseCPP**

The code for **TPYmandelbrotRecord** is implemented here.

In addition to being used by testPython, this is a simple example of how to build an
IOC database that contains a combination of PVRecords and DBRecords.

It contains the following subdirectories:

* src - Here is the code for **TPYmandelbrotRecord**
* dbSrc - Here is where DBRecords can be configured.
* iocSrc - Here is where the IOC database is created.
* iocBoot/mandelbrotDatabase - Here is where the database is started.

To build just type

    make

Then to start the IOC

    cd iocBoot/mandelbrotDatabase
    ../../bin/linux-x86_64/mandelbrotDatabase st.cmd
    ...
    epics> dbl
    TPYcounter01
    epics> pvdbl
    TPYaddRecord
    TPYmandelbrotRecord
    TPYremoveRecord
    TPYtraceRecord
    epics> 

