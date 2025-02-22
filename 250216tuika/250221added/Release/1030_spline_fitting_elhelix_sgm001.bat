::set dirname=P:\U\AAA\_work\20150824\
set dirname=P:\U\AAA\_work\20151009\


::start "elliptical_helix_a1_b1_c10" batchVModeler.exe 1019 %dirname%elliptical_helix_201_a1_b1_c10_sgm001.txt %dirname%param_elliptical_helix.txt 1 10
start "elliptical_helix_a1_b2_c10" batchVModeler.exe 1030 %dirname%elliptical_helix_201_a1_b2_c10_sgm001.txt %dirname%param_elliptical_helix_0.txt 1 10 2
::start "elliptical_helix_a1_b5_c10" batchVModeler.exe 1019 %dirname%elliptical_helix_201_a1_b5_c10_sgm001.txt %dirname%param_elliptical_helix.txt 1 10 5
::start "elliptical_helix_a1_b10_c10" batchVModeler.exe 1019 %dirname%elliptical_helix_201_a1_b10_c10_sgm001.txt %dirname%param_elliptical_helix.txt 1 10 10
