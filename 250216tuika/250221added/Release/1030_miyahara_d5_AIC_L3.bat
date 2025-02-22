set dirname=C:\_suzuki\work_suzuki\from_koba\20161122\
set path_prm=%dirname%param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3

batchVModeler.exe 1030 %dirname%centerline.txt %path_prm% %helix% %dirname%output\ %sigma2%
