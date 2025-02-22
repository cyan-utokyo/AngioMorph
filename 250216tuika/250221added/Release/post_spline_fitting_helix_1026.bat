set dirname=P:\U\AAA\_work\20150824\

::batchVModeler.exe 1026 %dirname%helix_sgm001_z0.txt %dirname%output_helix_z0\ %dirname%param_helix_z10.txt %dirname%helix_z0_AIC2.txt
start "" batchVModeler.exe 1026 %dirname%helix_sgm001_z1.txt %dirname%output_helix_z1\ %dirname%param_helix_z10.txt %dirname%helix_z1_AIC2.txt
start "" batchVModeler.exe 1026 %dirname%helix_sgm001_z2.txt %dirname%output_helix_z2\ %dirname%param_helix_z10.txt %dirname%helix_z2_AIC2.txt
start "" batchVModeler.exe 1026 %dirname%helix_sgm001_z5.txt %dirname%output_helix_z5\ %dirname%param_helix_z10.txt %dirname%helix_z5_AIC2.txt
start "" batchVModeler.exe 1026 %dirname%helix_sgm001_z10.txt %dirname%output_helix_z10\ %dirname%param_helix_z10.txt %dirname%helix_z10_AIC2.txt
