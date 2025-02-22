



set dname=D:\data\hayakawa\
set param=190 400 5 10

set fname=seg225_left
::batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg250_left
::batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg275_left
::batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg300_left
::batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%




set fname=seg225_right
batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg250_right
batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg275_right
batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%

set fname=seg300_right
batchVModeler.exe 113 %dname%%fname%\ *.vxu1 %dname%%fname%.txt %param%


