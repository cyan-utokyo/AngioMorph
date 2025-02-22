
set path_curve=C:\_suzuki\work_suzuki\V-modeler\helix_validation_geometry\center_and_stl\curvature07.txt
set path_stl=C:\_suzuki\work_suzuki\V-modeler\helix_validation_geometry\center_and_stl\curvature07.stl



:: function: to make a helix
:: argv[1] process ID
:: argv[2] output curve points file path
:: argv[3] the number of helical points
:: argv[4] length of extension straight line points[mm]
:: argv[5] length of extension straight line points[mm]
:: argv[6] helical radius[mm]ÅFa
:: argv[7] helical height[mm] : ÇÀÇ∂ÇÍÇÃçÇÇ≥
:: argv[8] connect inversive helix (0=don't connect, 1=connect)
:: argv[9] degree of angle
batchVModeler.exe 1041 %path_curve% 100 3.342 3.342 1.428571 0 0 180

:: function: to convert a curve into tube
:: argv[1] process ID
:: argv[2] input curve points file path
:: argv[3] tube radius[mm]
:: argv[4] the number of circumferential points
:: argv[5] output stl file path
:: argv[6] cap mode (0=no cap, 1=with cap)
batchVModeler.exe 125 %path_curve% 0.725 36 %path_stl% 1
