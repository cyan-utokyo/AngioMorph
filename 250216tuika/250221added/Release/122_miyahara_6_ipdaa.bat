set dirname=C:\_suzuki\work_suzuki\research\aaa\6_ipdaa\

batchVModeler.exe 122 ^
%dirname%seg_single\header.txt ^
%dirname%work\output_1\centerline_labeled_1_sigma0\centerline_labeled_1_d5_cp121_lmd1d0.000_lmd2d0.000_lmd3d5.000_lmd4d0.000_spline3d.txt ^
%dirname%work\stl\SPSURFACE_test\ 5 5 120


::%dirname%work\stl\SPSURFACE_stl\tube_sampling.txt ^
::%dirname%work\stl\SPSURFACE_stl\tube7.stl ^
::%dirname%work\stl\SPSURFACE_stl\tube_sampling3.txt
