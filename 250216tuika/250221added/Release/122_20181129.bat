set dirname=C:\_suzuki\6xsimulation\65_2018\p1\

:: argv[1]=process ID (122)
:: argv[2]=segmentation volume header
:: argv[3]=centerline file (spline format)
:: argv[4]=output directory
:: argv[5]=threshold degree   adj(é©å»åç∑Çñ≥Ç≠ÇπÇÈ)Ç…çÏóp def 
:: argv[6], argv[7]=knot range
:: -- option --
:: argv[8]=knot step(0.25)
:: argv[9]=gaussian width (31)
:: argv[10]=gaussian sigma (15)
:: argv[11]=cap stl (0 or 1)


batchVModeler.exe 122 ^
C:\_suzuki\6xsimulation\60Patietn_deta\dicom\patient1\seg_20181129_2\header.txt  ^
%dirname%output_1030\centerline_sigma0\centerline_d5_cp120_lmd1d0.000_lmd2d0.000_lmd3d2.000_lmd4d0.000_spline3d.txt ^
%dirname%spline\ 8 5 120 0.25 31 15 1


::%dirname%work\SPSURFACE\tube_sampling.txt ^
::%dirname%work\SPSURFACE\tube7.stl ^
::%dirname%work\SPSURFACE\tube_sampling3.txt
