set dirname=P:\U\miyahara\dicom\

batchVModeler.exe 122 ^
%dirname%seg1\header.txt ^
%dirname%work\SPSURFACE\centerline_d5_cp121_lmd1d0.000_lmd2d0.000_lmd3d1.000_lmd4d0.000_spline3d.txt ^
%dirname%work\SPSURFACE\ 10 5 119


::%dirname%work\SPSURFACE\tube_sampling.txt ^
::%dirname%work\SPSURFACE\tube7.stl ^
::%dirname%work\SPSURFACE\tube_sampling3.txt
