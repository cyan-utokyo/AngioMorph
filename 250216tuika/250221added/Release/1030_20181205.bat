set dirname=C:\_suzuki\6xsimulation\66_U_vs_any\
set center=%dirname%\p1\B_spline\
set path_prm=C:\_suzuki\6xsimulation\61U\2curveture_1torsion_model\APDA\APDAA_remodeling\20181205_centerline\param_5d_L3.txt
set helix=1 1 1
set sigma2=1.5
set key=_AIC_L3


batchVModeler.exe 1030 %center%1205_center.txt %path_prm% %helix% %center%output_20181205\ %sigma2%
