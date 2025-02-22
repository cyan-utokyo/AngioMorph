set dirname=P:\U\AAA\_work\20160214_stent\
set path_prm=%dirname%param_5d_L2.txt
set helix=1 1 1
set sigma2=16
set key=_4mm_L2

start "0m" batchVModeler.exe 1030 %dirname%input\0month_right.txt %path_prm% %helix% %dirname%0m_right%key%\ %sigma2%
start "7m" batchVModeler.exe 1030 %dirname%input\7months_right.txt %path_prm% %helix% %dirname%7m_right%key%\ %sigma2%
start "10m" batchVModeler.exe 1030 %dirname%input\10months_right.txt %path_prm% %helix% %dirname%10m_right%key%\ %sigma2%
start "0m" batchVModeler.exe 1030 %dirname%input\0month_left.txt %path_prm% %helix% %dirname%0m_left%key%\ %sigma2%
start "7m" batchVModeler.exe 1030 %dirname%input\7months_left.txt %path_prm% %helix% %dirname%7m_left%key%\ %sigma2%
start "10m" batchVModeler.exe 1030 %dirname%input\10months_left.txt %path_prm% %helix% %dirname%10m_left%key%\ %sigma2%

