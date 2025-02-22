set dirname=P:\U\shojima\20091019-CT_SN9\work\SFM\
set path_prm=%dirname%param_5d_L3.txt
set helix=1 1 1
set sigma2=1
set key=_AIC_L3

batchVModeler.exe 1030 %dirname%centerline.txt %path_prm% %helix% %dirname%output\ %sigma2%
