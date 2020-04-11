# testPython/dynamicplot 2020.04.08

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

This has the following:

    def getDynamicRecordName()
    def getAddRecordName() 
    class DynamicRecordData(object)
        def computeLimits(self)
    class Dynamic_Channel_Provider(object)

1) **getDynamicRecordName**
This gets the name of the record that holds the image data.
The default is 'dynamicRecord'.
An environment variable 'DYNAMIC_RECORDNAME' overrides the default.
2) **getAddRecordName**
This gets the name of a record that adds new records in the same PVDatabase.
The default is 'PVRaddRecord'.
An environment variable 'ADD_RECORDNAME' overrides the default.
3) **DynamicRecordData**
This describes the data in a dynamicRecord.
It has the following fields: name,x,y,xmin,xmax,ymin,ymax.
name is a string, x and y are double array,all other fields have type double.
**computeLimits** computes xmin,xmax,ymin,and ymax.
4) **Dynamic_Channel_Provider**
This describes methods that **P4P_Dynamic_Viewer** and **PVAPY_Dynamic_Viewer** must implement.
    

### GenerateCurve.py

This is the code that generates the x and y arrays for an image.
It is called by **P4PgenerateCurve** and **PVAPYgenerateCurve**.
It can also be called directly by python.
In order to generate a curve, it requires an argument that is the name of the curve.
Note that some of the code allows additional arguments.
Look at the code for details.

### Dynamic_Viewer.py

This is the code that provides the user interface and code that dynamically generates images.

### P4PaddDynamicRecord.py and PVAPYaddDynamicRecord.py

This is code that create a dynamicRecord.

### P4P_Dynamic_Viewer.py and PVAPY_Dynamic_Viewer.py

This is code that:
1) creates an instance of **Dynamic_Channel_Provider**,
2) creates an instance of **Dynamic_Viewer**
3) connects to a dynamicRecord
4) monitors the dynamicRecord and passes each monitor event to **Dynamic_Viewer**

### P4PgenerateCurve.py and PVAPYgenerateCurve.py

This is code that 
1) calls **GenerateCurve**
2) connects to dynamicRecord
3) Issues puts to dynamicRecord stating with a single x,y point, adding a new points, etc.
This continues until all points have been sent.

The code than terminates.

## Threading rules for Python client working with PyQt5

This assumes that a Python application has been started via **QApplication**.
Also that there are three python objects involved:

1) The application itself.
2) PyQt5 code.
3) Python server code, e. g. P4P and PVAPY

Each of these has data and threads that may or may not be **GIL** threads.

The rules for accessing data are:

1) Server data can only be manipulated via the server thread.
2) PyQt5 data can only be manipulated via the QApplication thread
3) The application data can be manipulated from either the server or QApplication thread.

Look at either **PVAPY_Dynamic_Viewer** or **P4PPY_Dynamic_Viewer** to see how **pyqtSignal()**
is used transfer control from the server thread to the QApplication thread.

