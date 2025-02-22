


set dname=F:\U20140718\hayakawa\
::set dname=D:\data\hayakawa\

::225
::Left
::batchVModeler.exe 115 %dname%seg350_left\ *_seg.vxu1 %dname%seg350_left\ %dname%ROI_CA_Left.txt
batchVModeler.exe 115 %dname%seg400_left\ *_seg.vxu1 %dname%seg400_left\ %dname%ROI_CA_Left.txt 2
::Right
::batchVModeler.exe 115 %dname%seg350_right\ *_seg.vxu1 %dname%seg350_right\

