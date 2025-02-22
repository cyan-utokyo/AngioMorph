set dname=P:\U\AAA\_work\20160121_a1b1c10\
set base_input=%dname%input0\elliptical_helix_201_a1_b1_c10_sgm000
set path_prm=%dname%param_elhelix_d5_n10.txt
set dirname_out=%dname%result_d5\
set helix=1 1 10


batchVModeler.exe 1030 %base_input%_0000.txt %path_prm% %helix% %dirname_out% 0.01 1

set path_prm=%dname%param_elhelix_d3_n10.txt
set dirname_out=%dname%result_d3\

batchVModeler.exe 1030 %base_input%_0000.txt %path_prm% %helix% %dirname_out% 0.01 1
