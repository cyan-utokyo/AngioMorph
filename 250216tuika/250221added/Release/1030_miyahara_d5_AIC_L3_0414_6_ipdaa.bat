set dirname=C:\_suzuki\work_suzuki\V-modeler\
set center=C:\_suzuki\work_suzuki\research\aaa\6_ipdaa\work\stl\seg_sp_7\
set path_prm=%dirname%param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3

batchVModeler.exe 1030 %center%centerline.txt %path_prm% %helix% %center%output\ %sigma2%
