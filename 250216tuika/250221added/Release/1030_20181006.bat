set dirname=C:\_suzuki\3xsoftware\31V-modelar\work1\p5\
set center=%dirname%
set path_prm=C:\_suzuki\3xsoftware\31V-modelar\param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3


::batchVModeler.exe 1030 %center%IPDA_centerline.txt %path_prm% %helix% %center%IPDA_output\ %sigma2%
::batchVModeler.exe 1030 %center%IAPDA_centerline.txt %path_prm% %helix% %center%IAPDA_output\ %sigma2%
batchVModeler.exe 1030 %center%IPPDA_centerline.txt %path_prm% %helix% %center%IPPDA_output\ %sigma2%
