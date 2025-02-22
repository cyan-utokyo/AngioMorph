set dirname=P:\U\AAA\_work\20151013\


start "0m" batchVModeler.exe 1030 %dirname%0month_right.txt %dirname%param_0m.txt 0.5 0.5 0
start "7m" batchVModeler.exe 1030 %dirname%7months_right.txt %dirname%param_7m.txt 0.5 0.5 1
start "10m" batchVModeler.exe 1030 %dirname%10months_right.txt %dirname%param_10m.txt 0.5 0.5 2
