set dirname=C:\_suzuki\3xsoftware\31V-modelar\
set center=C:\_suzuki\bif_curve\non_aneurysm\
set path_prm=%dirname%param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3

batchVModeler.exe 1030 %center%centerline.txt %path_prm% %helix% %center%output\ %sigma2%
