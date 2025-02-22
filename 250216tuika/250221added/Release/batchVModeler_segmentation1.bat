


set dname=F:\U20140718\hayakawa\
::set dname=D:\data\hayakawa\
::225
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg225_left\ 50 180 150 300 106 534 0 0 225 800 3 123 219 215
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg225_right\ 300 500 150 300 106 534 0 0 225 800 3 409 227 320

::250
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg250_left\ 50 180 150 300 106 534 0 0 250 800 3 123 219 215
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg250_right\ 300 500 150 300 106 534 0 0 250 800 3 409 227 300

::275
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg275_left\ 50 180 150 300 106 534 0 0 275 800 2 123 219 215
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg275_right\ 300 500 150 300 106 534 0 0 275 800 3 409 227 320

::300
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg300_left\ 50 180 150 300 106 534 0 0 300 800 2 123 219 215
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg300_right\ 300 500 150 300 106 534 0 0 300 800 3 409 227 320

::325
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg325_left\ 50 180 150 300 106 534 0 0 325 800 2 123 219 215
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg325_right\ 300 500 150 300 106 534 0 0 325 800 3 409 227 320


:: fill hole
:: iterative number of closing process

set thresSeg=350

set paramL1=50 180 150 300 106 534 0 0 
set paramSegL= 800 1 
set paramL2=-1 -1 1 1 

set paramR1=300 500 150 300 106 534 0 0 
set paramSegR=800 2 
set paramR2=409 227 320 1 1 


set thresSeg=350
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg350_left\ %paramL1% %thresSeg% %paramSegL% %paramL2%
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg350_right\ 300 500 150 300 106 534 0 0 350 800 3 409 227 320

set thresSeg=375
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg375_left\ %paramL1% %thresSeg% %paramSegL% %dname%seed_left.txt %paramL2%
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg375_right\ 300 500 150 300 106 534 0 0 375 800 3 409 227 320

set thresSeg=400
::Left
batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg400_left\ %paramL1% %thresSeg% %paramSegL% %dname%seed_left.txt %paramL2%
::Right
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg400_right\ 300 500 150 300 106 534 0 0 400 800 3 409 227 320

set thresSeg=450
::Left
::batchVModeler.exe 111 %dname% *_060Y_M_* *.dcm %dname%seg450_left\ %paramL1% %thresSeg% %paramSegL% %dname%seed_left.txt %paramL2%


