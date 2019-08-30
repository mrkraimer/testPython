# testPvaPy/array

**testPvaPy/array** has python code that demonstrates **pvaPy** performance when the client uses numpy support.

## exampleCPP/arrayPerformance

**exampleCPP/arrayPerformance** is C++ code that demonstrates perforamnce for large arrays.
This is the code that is used to compare the python performance.

To run the test, in one window, run:

>mrk> pwd
/home/epicsv4/masterCPP/exampleCPP/arrayPerformance
mrk> bin/linux-x86_64/arrayPerformanceMain
arrayPerformance 10000000 0.0001 1 2
pvAccess Server v7.0.1-SNAPSHOT
Active configuration (w/ defaults)
EPICS_PVAS_INTF_ADDR_LIST = 0.0.0.0:5075
EPICS_PVAS_BEACON_ADDR_LIST = 
EPICS_PVAS_AUTO_BEACON_ADDR_LIST = YES
EPICS_PVAS_BEACON_PERIOD = 15
EPICS_PVAS_BROADCAST_PORT = 5076
EPICS_PVAS_SERVER_PORT = 5075
EPICS_PVAS_PROVIDER_NAMES = local
arrayPerformance
Type exit to stop: 
arrayPerformance value 19 time 1.01748 Iterations/sec 18.6735 megaElements/sec 186.735
 monitors/sec 15 first 18 last 18 changed {1, 4} overrun {} megaElements/sec 157.766
arrayPerformance value 36 time 1.02704 Iterations/sec 16.5524 megaElements/sec 165.524
 monitors/sec 17 first 35 last 35 changed {1, 4} overrun {} megaElements/sec 165.519
arrayPerformance value 51 time 1.01022 Iterations/sec 14.8482 megaElements/sec 148.482
 monitors/sec 14 first 50 last 50 changed {1, 4} overrun {} megaElements/sec 138.453
arrayPerformance value 68 time 1.02382 Iterations/sec 16.6045 megaElements/sec 166.045
 monitors/sec 17 first 67 last 67 changed {1, 4} overrun {} megaElements/sec 165.794
arrayPerformance value 87 time 1.0095 Iterations/sec 18.8211 megaElements/sec 188.211
 monitors/sec 19 first 86 last 86 changed {1, 4} overrun {} megaElements/sec 186.169
exarrayPerformance value 103 time 1.02836 Iterations/sec 15.5588 megaElements/sec 155.588
 monitors/sec 16 first 102 last 102 changed {1, 4} overrun {} megaElements/sec 156.465
itarrayPerformance value 120 time 1.04606 Iterations/sec 16.2514 megaElements/sec 162.514
 monitors/sec 17 first 119 last 119 changed {1, 4} overrun {} megaElements/sec 160.746


In another window run:

>mrk> pwd
/home/epicsv4/masterCPP/exampleCPP/arrayPerformance
mrk> bin/linux-x86_64/longArrayMonitorMain
Type exit to stop: 
 monitors/sec 8 first 138 last 138 changed {1, 4} overrun {} megaElements/sec 87.309
 monitors/sec 9 first 148 last 148 changed {1, 4} overrun {} megaElements/sec 89.2977
 monitors/sec 10 first 160 last 160 changed {1, 4} overrun {} megaElements/sec 95.3641
 monitors/sec 12 first 172 last 172 changed {1, 3, 4} overrun {} megaElements/sec 109.662
 monitors/sec 10 first 183 last 183 changed {1, 3, 4} overrun {} megaElements/sec 98.9655
 monitors/sec 9 first 194 last 194 changed {1, 4} overrun {} megaElements/sec 83.1417
 monitors/sec 11 first 205 last 205 changed {1, 4} overrun {} megaElements/sec 107.873

This is what can be used to compare the python performance.


## testPvaPy/array/monitorRate.py

mrk> python monitorRate.py arrayPerformance
enter somethingmonitors/sec  0.4360687333412556  megaElements/sec  4.360687333412556
monitors/sec  8.403444748561627  megaElements/sec  84.03444748561627
monitors/sec  7.858445811755713  megaElements/sec  78.58445811755712
monitors/sec  7.646654979046831  megaElements/sec  76.4665497904683
monitors/sec  9.98271510430201  megaElements/sec  99.8271510430201
monitors/sec  6.956601515944906  megaElements/sec  69.56601515944907
monitors/sec  9.203942969533294  megaElements/sec  92.03942969533294
monitors/sec  9.62315262741895  megaElements/sec  96.2315262741895
monitors/sec  6.860796769644378  megaElements/sec  68.60796769644378
monitors/sec  10.909463091219676  megaElements/sec  109.09463091219675
monitors/sec  7.976959023815745  megaElements/sec  79.76959023815745
monitors/sec  9.822608676102464  megaElements/sec  98.22608676102463
monitors/sec  9.970103741940882  megaElements/sec  99.70103741940882
monitors/sec  8.412321399322312  megaElements/sec  84.12321399322313
monitors/sec  8.61018047086377  megaElements/sec  86.10180470863772
monitors/sec  9.17014056583581  megaElements/sec  91.7014056583581
monitors/sec  9.736079448449525  megaElements/sec  97.36079448449526
monitors/sec  9.009509133334722  megaElements/sec  90.09509133334721
monitors/sec  10.733154328566956  megaElements/sec  107.33154328566955
monitors/sec  6.814508991932873  megaElements/sec  68.14508991932874

But without using ndarray

mrk> python monitorRate.py arrayPerformance False
monitors/sec  0.878050108031692  megaElements/sec  8.78050108031692
monitors/sec  0.8107910516342132  megaElements/sec  8.107910516342132
monitors/sec  0.8494896140510062  megaElements/sec  8.494896140510061
monitors/sec  0.8379827616623302  megaElements/sec  8.379827616623302
monitors/sec  0.8417130287692877  megaElements/sec  8.417130287692876
monitors/sec  0.8687278367738523  megaElements/sec  8.687278367738523


## testPvaPy/array/monitorRateP4P.py

mrk> python monitorRateP4P.py arrayPerformance
enter somethingmonitors/sec  0.41240029465704037  megaElements/sec  4.124002946570404
monitors/sec  4.48996457531268  megaElements/sec  44.8996457531268
monitors/sec  4.186471948279159  megaElements/sec  41.86471948279159
monitors/sec  4.100980448521271  megaElements/sec  41.009804485212705
monitors/sec  4.481921448746093  megaElements/sec  44.81921448746093
monitors/sec  4.2656695039347285  megaElements/sec  42.656695039347284
monitors/sec  4.578652580779961  megaElements/sec  45.786525807799606
monitors/sec  4.402579468462224  megaElements/sec  44.025794684622234
monitors/sec  3.7047688154211085  megaElements/sec  37.04768815421108
eximonitors/sec  3.627987802056316  megaElements/sec  36.27987802056316
tmonitors/sec  4.537375899214812  megaElements/sec  45.37375899214812


