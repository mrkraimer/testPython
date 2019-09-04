# testPvaPy/array

**Author** Marty Kraimer
**Date** 2019.09.04

**testPvaPy/array** has python code that demonstrates **pvaPy** performance when the client uses numpy support.

From the early days of EPICS V4 (2013) **exampleCPP** implemented **arrayPerformance**,
which was used to measure the monitor performance of large arrays.
Most of the examples shown below were for an int64 array with 10 megaElements, i.e. 80 megaBytes.

A summary of the results below is:

```
arrayPerformanceMain longArrayMonitorMain monitorRate.py monitorRateP4P.py monitorRate.py(getScalarArray)
                 76                   83            83                43             8
```

Notes:

* All results are megaElements/second. Thus multiply by 8 to get megaBytes/second.
* The last coluumn shows that not using numpy causes a significent performance loss.
* arrayPerformanceMain was measured while longArrayMonitorMain was running and is the monitor/sec value.

There is also an example **putArrayFast.py**.
This is a python client that sends arrays to a server.
It shows that the performance is less than 1/2 the rate of a server generating the arrays.
But since this involves an extra transfer of each array over the network it is what is expected.
It does show that using python with numpy support provides good performance.

## exampleCPP/arrayPerformance

**exampleCPP/arrayPerformance** is C++ code that demonstrates perforamnce for large arrays.
This is the code that is used to compare the python performance.

To run the test, in one window, run:

```
mrk> pwd
/home/epicsv4/masterCPP/exampleCPP/arrayPerformance
mrk> bin/linux-x86_64/arrayPerformanceMain
arrayPerformance 10000000 0.0001 1 2
...
arrayPerformance value 630 time 1.03036 Iterations/sec 11.6464 megaElements/sec 116.464
 monitors/sec 7 first 636 last 636 changed {1, 4} overrun {1, 4} megaElements/sec 66.1776
arrayPerformance value 642 time 1.0302 Iterations/sec 11.6483 megaElements/sec 116.483
 monitors/sec 9 first 649 last 649 changed {1, 4} overrun {} megaElements/sec 83.9152
arrayPerformance value 654 time 1.0109 Iterations/sec 11.8706 megaElements/sec 118.706
 monitors/sec 9 first 661 last 661 changed {1, 4} overrun {1, 4} megaElements/sec 86.1056
arrayPerformance value 667 time 1.08081 Iterations/sec 12.028 megaElements/sec 120.28
 monitors/sec 9 first 675 last 675 changed {1, 4} overrun {1, 4} megaElements/sec 79.0863
arrayPerformance value 680 time 1.03192 Iterations/sec 12.5979 megaElements/sec 125.979
 monitors/sec 8 first 688 last 688 changed {1, 4} overrun {1, 4} megaElements/sec 73.4352
arrayPerformance value 692 time 1.04915 Iterations/sec 11.4379 megaElements/sec 114.379
 monitors/sec 8 first 701 last 701 changed {1, 4} overrun {1, 4} megaElements/sec 69.3863
```

In another window run:

```
mrk> pwd
/home/epicsv4/masterCPP/exampleCPP/arrayPerformance
mrk> bin/linux-x86_64/longArrayMonitorMain
 monitors/sec 10 first 646 last 646 changed {1, 4} overrun {1, 4} megaElements/sec 92.3162
 monitors/sec 7 first 659 last 659 changed {1, 4} overrun {1, 4} megaElements/sec 67.2341
 monitors/sec 10 first 673 last 673 changed {1, 4} overrun {1, 4} megaElements/sec 85.7956
 monitors/sec 9 first 686 last 686 changed {1, 4} overrun {} megaElements/sec 83.7509
 monitors/sec 11 first 698 last 698 changed {1, 4} overrun {} megaElements/sec 105.761
 monitors/sec 10 first 711 last 711 changed {1, 4} overrun {1, 4} megaElements/sec 92.1672

```

This is what can be used to compare the python performance.


## testPvaPy/array/monitorRate.py

### using ndarray: arr = arg['value']

```
mrk> python monitorRate.py arrayPerformance
...
monitors/sec  8.403444748561627  megaElements/sec  84.03444748561627
monitors/sec  7.858445811755713  megaElements/sec  78.58445811755712
monitors/sec  7.646654979046831  megaElements/sec  76.4665497904683
monitors/sec  9.98271510430201  megaElements/sec  99.8271510430201
monitors/sec  6.956601515944906  megaElements/sec  69.56601515944907
monitors/sec  9.203942969533294  megaElements/sec  92.03942969533294
```


## testPvaPy/array/monitorRateP4P.py


```
mrk> python monitorRateP4P.py arrayPerformance
monitors/sec  4.48996457531268  megaElements/sec  44.8996457531268
monitors/sec  4.186471948279159  megaElements/sec  41.86471948279159
monitors/sec  4.100980448521271  megaElements/sec  41.009804485212705
monitors/sec  4.481921448746093  megaElements/sec  44.81921448746093
monitors/sec  4.2656695039347285  megaElements/sec  42.656695039347284
monitors/sec  4.578652580779961  megaElements/sec  45.786525807799606
```

### not using ndarray: arr = arg.getScalarArray('value')

```
mrk> python monitorRate.py arrayPerformance false
monitors/sec  0.878050108031692  megaElements/sec  8.78050108031692
monitors/sec  0.8107910516342132  megaElements/sec  8.107910516342132
monitors/sec  0.8494896140510062  megaElements/sec  8.494896140510061
monitors/sec  0.8379827616623302  megaElements/sec  8.379827616623302
monitors/sec  0.8417130287692877  megaElements/sec  8.417130287692876
monitors/sec  0.8687278367738523  megaElements/sec  8.687278367738523
```


## putArrayFast.py

### PVRlongArray

#### Start 

```
mrk> pwd
/home/epicsv4/masterCPP/testPvaPy/array
mrk> python putArrayFast.py
must supply three args: channelName numElements sleepTime
mrk> python putArrayFast.py PVRlongArray 10000000 .0001
```

#### monitorRate.py

```
mrk> python monitorRate.py PVRlongArray
...
monitors/sec  3.356648908287857  megaElements/sec  33.56648908287857
monitors/sec  3.298571862799108  megaElements/sec  32.98571862799108
monitors/sec  3.1572315705542877  megaElements/sec  31.572315705542877
monitors/sec  3.1993348550811693  megaElements/sec  31.993348550811692
monitors/sec  3.233522584256107  megaElements/sec  32.33522584256107
monitors/sec  3.320132265305569  megaElements/sec  33.20132265305569
```

#### monitorRateP4P.py


```
mrk> python monitorRateP4P.py PVRlongArray
monitors/sec  0.44614830345629247  megaElements/sec  4.461483034562925
monitors/sec  3.4186151047985516  megaElements/sec  34.18615104798552
monitors/sec  2.962368498805792  megaElements/sec  29.623684988057917
monitors/sec  2.963491777506933  megaElements/sec  29.63491777506933
monitors/sec  3.051719587378336  megaElements/sec  30.51719587378336
monitors/sec  2.8982533887666846  megaElements/sec  28.982533887666847
```


#### longArrayMonitorMain PV


```
mrk> bin/linux-x86_64/longArrayMonitorMain PVRlongArray
Type exit to stop: 
 monitors/sec 4 first 680 last 680 changed {1, 4} overrun {} megaElements/sec 42.4251
 monitors/sec 4 first 684 last 684 changed {1, 3, 4} overrun {} megaElements/sec 33.3599
 monitors/sec 4 first 688 last 688 changed {1, 4} overrun {} megaElements/sec 32.4083
 monitors/sec 4 first 692 last 692 changed {1, 4} overrun {} megaElements/sec 32.4121
 monitors/sec 4 first 696 last 696 changed {1, 4} overrun {} megaElements/sec 34.0309
 monitors/sec 4 first 700 last 700 changed {1, 4} overrun {} megaElements/sec 33.1869
 monitors/sec 4 first 704 last 704 changed {1, 3, 4} overrun {} megaElements/sec 32.0976
 monitors/sec 4 first 708 last 708 changed {1, 4} overrun {} megaElements/sec 32.0532
```

### PVRbyteArray

#### Start

```
mrk> python putArrayFast.py PVRbyteArray 100000000 .0001
```

#### monitorRate.py

```
mrk> python monitorRate.py PVRbyteArray
monitors/sec  0.45663953556353387  megaElements/sec  45.66395355635339
monitors/sec  2.757827194825427  megaElements/sec  275.7827194825427
monitors/sec  2.6452956064408344  megaElements/sec  264.52956064408346
monitors/sec  2.613025513466323  megaElements/sec  261.30255134663236
monitors/sec  2.732188106484644  megaElements/sec  273.2188106484644
monitors/sec  2.7565065225144387  megaElements/sec  275.6506522514439
monitors/sec  2.582194410658178  megaElements/sec  258.2194410658178
monitors/sec  2.6961058428748323  megaElements/sec  269.6105842874832
monitors/sec  2.6319761294431774  megaElements/sec  263.1976129443177
monitors/sec  2.696956466664395  megaElements/sec  269.6956466664395
```

#### monitorRateP4P.py


```
mrk> python monitorRateP4P.py PVRbyteArray
monitors/sec  0.44910414820519123  megaElements/sec  44.91041482051913
monitors/sec  2.7093038528236772  megaElements/sec  270.9303852823677
monitors/sec  2.4700966628629177  megaElements/sec  247.00966628629178
monitors/sec  2.4439178785020736  megaElements/sec  244.39178785020735
monitors/sec  2.45404738296825  megaElements/sec  245.40473829682503
monitors/sec  2.390684643443887  megaElements/sec  239.0684643443887
monitors/sec  2.4280109871980042  megaElements/sec  242.80109871980042
monitors/sec  2.492932448448063  megaElements/sec  249.29324484480628
```




