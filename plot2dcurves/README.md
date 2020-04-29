# testPython/dynamicplot 2020.04.29

- For more information see
   [python/PYQTwithPVDatabase](https://mrkraimer.github.io/website/developerGuide/python/PYQTwithPVDatabase.html).

The rest of this document will remain until above has incorporated this material.



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
The default is 'TPYaddRecord'.
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

