

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

set dname=D:\koba\program\V-Modeler\data\
batchVModeler.exe 104 %dname%009.stl %dname%009_00.txt %dname%009_00.obj %dname%009_00.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_01.txt %dname%009_01.obj %dname%009_01.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_02.txt %dname%009_02.obj %dname%009_02.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_03.txt %dname%009_03.obj %dname%009_03.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_04.txt %dname%009_04.obj %dname%009_04.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_05.txt %dname%009_05.obj %dname%009_05.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_06.txt %dname%009_06.obj %dname%009_06.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_07.txt %dname%009_07.obj %dname%009_07.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_08.txt %dname%009_08.obj %dname%009_08.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_09.txt %dname%009_09.obj %dname%009_09.stl 36 0.1
batchVModeler.exe 104 %dname%009.stl %dname%009_10.txt %dname%009_10.obj %dname%009_10.stl 36 0.1

