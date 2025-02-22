set dirname=C:\_suzuki\work_suzuki\V-modeler\
set center=C:\_suzuki\work_suzuki\research\aaa\patient1\stl_and_mesh\seg_single\geometry_info\
set path_prm=%dirname%param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3

batchVModeler.exe 1030 %center%centerline.txt %path_prm% %helix% %center%output\ %sigma2%
