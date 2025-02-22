

:: make tube model by spline surface
:: process id
:: control point file
:: surface stl file
:: the number of circumferential control points
:: the number of longitudinal control points
:: radius x
:: radius y
:: z step 
:: interpolating step of knot vector
::batchVModeler.exe 102 C:\koba\U\tube1_cp.obj C:\koba\U\tube1.stl 10 20 1.0 1.0 1.0 0.1


:: cross section
::batchVModeler.exe 103 C:\koba\U\009.stl C:\koba\U\009_cp_00.txt C:\koba\U\009_cs5_r2.obj 5.0 36

::set dname=C:\koba\U\V-Modeler\data\centerline2\
::set dname=D:\koba\program\V-Modeler\data\centerline2\
::batchVModeler.exe 107 D:\koba\program\V-Modeler\data\009.stl %dname% %dname%009_xx.obj %dname%009_xx.stl 36 0.2


set dname0=F:\U20140718\hayakawa\
set dname=F:\U20140718\hayakawa\seg225_left\
::set dname=F:\U20140718\hayakawa\seg225_right\
batchVModeler.exe 107 %dname%20090421_060Y_M_009_seg.stl %dname% %dname%009_xx.obj %dname%009_xx.stl 36 0.2 009


batchVModeler.exe 107 %dname%20090421_060Y_M_010_seg.stl %dname% %dname%010_xx.obj %dname%010_xx.stl 36 0.2 010

batchVModeler.exe 107 %dname%20090421_060Y_M_011_seg.stl %dname% %dname%011_xx.obj %dname%011_xx.stl 36 0.2 011
batchVModeler.exe 107 %dname%20090421_060Y_M_012_seg.stl %dname% %dname%012_xx.obj %dname%012_xx.stl 36 0.2 012
batchVModeler.exe 107 %dname%20090421_060Y_M_013_seg.stl %dname% %dname%013_xx.obj %dname%013_xx.stl 36 0.2 013
batchVModeler.exe 107 %dname%20090421_060Y_M_014_seg.stl %dname% %dname%014_xx.obj %dname%014_xx.stl 36 0.2 014
batchVModeler.exe 107 %dname%20090421_060Y_M_015_seg.stl %dname% %dname%015_xx.obj %dname%015_xx.stl 36 0.2 015
batchVModeler.exe 107 %dname%20090421_060Y_M_016_seg.stl %dname% %dname%016_xx.obj %dname%016_xx.stl 36 0.2 016
batchVModeler.exe 107 %dname%20090421_060Y_M_017_seg.stl %dname% %dname%017_xx.obj %dname%017_xx.stl 36 0.2 017
batchVModeler.exe 107 %dname%20090421_060Y_M_018_seg.stl %dname% %dname%018_xx.obj %dname%018_xx.stl 36 0.2 018
batchVModeler.exe 107 %dname%20090421_060Y_M_019_seg.stl %dname% %dname%019_xx.obj %dname%019_xx.stl 36 0.2 019
batchVModeler.exe 107 %dname%20090421_060Y_M_020_seg.stl %dname% %dname%020_xx.obj %dname%020_xx.stl 36 0.2 020
batchVModeler.exe 107 %dname%20090421_060Y_M_021_seg.stl %dname% %dname%021_xx.obj %dname%021_xx.stl 36 0.2 021
batchVModeler.exe 107 %dname%20090421_060Y_M_022_seg.stl %dname% %dname%022_xx.obj %dname%022_xx.stl 36 0.2 022
batchVModeler.exe 107 %dname%20090421_060Y_M_023_seg.stl %dname% %dname%023_xx.obj %dname%023_xx.stl 36 0.2 023
batchVModeler.exe 107 %dname%20090421_060Y_M_024_seg.stl %dname% %dname%024_xx.obj %dname%024_xx.stl 36 0.2 024
batchVModeler.exe 107 %dname%20090421_060Y_M_025_seg.stl %dname% %dname%025_xx.obj %dname%025_xx.stl 36 0.2 025
batchVModeler.exe 107 %dname%20090421_060Y_M_026_seg.stl %dname% %dname%026_xx.obj %dname%026_xx.stl 36 0.2 026
batchVModeler.exe 107 %dname%20090421_060Y_M_027_seg.stl %dname% %dname%027_xx.obj %dname%027_xx.stl 36 0.2 027
batchVModeler.exe 107 %dname%20090421_060Y_M_028_seg.stl %dname% %dname%028_xx.obj %dname%028_xx.stl 36 0.2 028
