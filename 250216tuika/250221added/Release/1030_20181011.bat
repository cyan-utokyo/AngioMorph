set dirname=C:\_suzuki\vmtk_centerline\geometry\V-modelar\
set center=%dirname%
set path_prm=C:\_suzuki\3xsoftware\31V-modelar\param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3


batchVModeler.exe 1030 %center%centerline.txt %path_prm% %helix% %center%output_1030\ %sigma2%
