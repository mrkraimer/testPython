# testPython/mandelbrot 2020.04.18

This is code that produces a mandelbrot image.

Two versions are provided: **DisplayImagePython** and **DisplayImagePVAPY**.
**DisplayImagePython** does all computations in Python.
**DisplayImagePVAPY** does all computation in and IOC PVRecord named **TPYmandelbrotRecord**

There is a big difference in performance.


**DisplayImagePVAPY** requires that the database provided by testPython has been started.
For example I start it as follows

    mrk> pwd
    /home/epics7/modules/testPython/database/iocBoot/mandelbrotDatabase
    mrk> ../../bin/linux-x86_64/mandelbrotDatabase st.cmd 



## User Interface

When the following is entered

    python DisplayImagePVAPY.py

The following appears:

![viewer window](viewer.png)

When **start** is pressed the following appears.

![image window](image.png)

After the image appears you can use the mouse to select a sub-image.
Just depress the mouse in the image, drag it in lower right direction, and release.
The subimage will appear.

You can also run:

     python DisplayImagePython.py

You will find it much slower than the pvapy version.
Be patient waiting for the images to appear.
