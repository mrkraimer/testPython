# testPython/dynamicplot 2020.03.17

This is code that produces dynamic image plots.
Dynamically means that the viewer shows the curve growing as the number of points increases.

Implementations are provided for both pvapy and p4p,
which are two different python wrappers for pvAccess/pvData.

Below there are instructions for

1) Starting the example
2) Installation of required Python modules.

## User Interface

When either version of the viewer is started the following appears:

![viewer window](viewer.png)

When **start** is pressed the following appears

![image window](image.png)

### Control window

1) **start**
Clicking this button starts communication with the server.
2) **stop**
Clicking this button stops communication with the server.
3) **npts**
This is the number of (x,y) points for the current image.
4) **imageName**
This is the name of the current curve being displayed.
5) **imageRate**
This is the number of images/second being displayed.
6) **status**
This shows current status.
Clicking **clear** erases the current status.

## Starting the example

### Starting example database.

Start an IOC running the example database
For example I start it as follows

    mrk> pwd
    /home/epics7/modules/exampleCPP/database/iocBoot/exampleDatabase
    mrk> ./../bin/linux-x86_64/exampleDatabase st.cmd

One of the records is one to add new records.

    mrk> pvinfo PVRaddRecord
    structure
        structure argument
            string recordName
            any union
        structure result
            string status

This is the default add record.
It is also possible to use a different add record by setting an environment variable **ADD_RECORDNAME**.


### Create dynamicRecord

Just issue the following:

    python P4PaddDynamicRecord.py

or

    python PVAPYaddDynamicRecord.py


Note that name for the record added is **dynamicRecord**.
This can be changed by setting an environment variable **DYNAMIC_RECORDNAME**.

The added record is :

    mrk> pvinfo dynamicRecord
    structure
        string name
        double[] x
        double[] y
        double xmin
        double xmax
        double ymin
        double ymax


### start P4P_Dynamic_Viewer or PVAPY_Dynamic_Viewer

For example:

    mrk> python P4P_Dynamic_Viewer.py

You will see errors if You have not installed all the python packages required.
If it shows no errors click connect and start.

Then run any of the curve generating python modules. For example

    mrk> python P4PgenerateCurve.py circle

or
    mrk> python PVAPYgenerateCurve.py circle

If either command is given without an argument then a list of curve types is provided.
For example:

    mrk> python PVAPYgenerateCurve.py
    argument must be one of:  ('line', 'circle', 'ellipse', 'clover', 'heart', 'lissajous')


On the viewer a circle appears.

Once a complete curve is generated then it is also posssible to generate a static plot.
For example:

    python PVAPYstaticImage.py dynamicRecord

produces:

![image window](staticimage.png)


## Required python modules

You must have python and pip installed.

The other python modules can be installed via **pip install ...**

For example issue the command

    sudo pip install numpy

The following shows all installed python modules

    pip list

The following is a list of modules required by PY_Dynamic_Viewer

1) numpy
2) PyQt5
3) PyQt5-sip
4) QtPy
5) p4p and/or pvapy
6) pyqtgraph



## Brief description of code

### Dynamic_Common.py

### GenerateCurve.py

### Dynamic_Viewer.py

### P4PaddDynamicRecord.py and PVAPYaddDynamicRecord.py

### P4P_Dynamic_Viewer.py and PVAPY_Dynamic_Viewer.py

### P4PgenerateCurve.py and PVAPYgenerateCurve.py


## PVAPY_Dynamic_Viewer Problem

**PVAPY_Dynamic_Viewer** does not use **PYQT5** threading, i.e. it calls Dynamic_Viewer.callback directly
from it's monitor callback.

1) Does not show complete dynamic image
2) Displays images at slower rate then **P4P_Dynamic_Viewer**.
Note that it thinks it is displaying them faster but the actual imapge rate is much slower.
This is probably because PyQt5 is displaying the images via a separate thread.
3) It sometimes gets in a mode where it is issuing messages:

    QBackingStore::endPaint() called with active painter; did you forget to destroy it or call QPainter::end() on it?
    QBackingStore::endPaint() called with active painter; did you forget to destroy it or call QPainter::end() on it?


To see this start it and also **P4P_Dynamic_Viewer** and then run:

    ./gencurves

I suspect the problem is interaction with the difference between **pvapy** and **PYQt5** threading.

**PVAPYpyqtSignal_Dynamic_Viewer.py** is a version that uses **PYQT5** threading.
It displays images at an even slower rate than **PVAPY_Dynamic_Viewer**.
But it never issues the error messages.


