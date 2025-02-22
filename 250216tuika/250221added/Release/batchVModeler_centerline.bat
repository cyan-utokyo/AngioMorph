

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


set dname=D:\koba\program\V-Modeler\data\centerline4\
batchVModeler.exe 100 %dname%009_c_00.txt %dname%009_00_c.ply %dname%009_00_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_01.txt %dname%009_01_c.ply %dname%009_01_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_02.txt %dname%009_02_c.ply %dname%009_02_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_03.txt %dname%009_03_c.ply %dname%009_03_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_04.txt %dname%009_04_c.ply %dname%009_04_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_05.txt %dname%009_05_c.ply %dname%009_05_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_06.txt %dname%009_06_c.ply %dname%009_06_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_07.txt %dname%009_07_c.ply %dname%009_07_c.obj 0.1
batchVModeler.exe 100 %dname%009_c_08.txt %dname%009_08_c.ply %dname%009_08_c.obj 0.1
