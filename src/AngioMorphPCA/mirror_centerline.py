"""
本程序用于批量处理vtk格式的3D曲线数据，对曲线进行YZ平面镜像反转，并保存处理后的曲线数据。
This program is used to batch process 3D curve data in vtk format, perform mirror reflection with respect to the YZ-plane,
and save the processed curve data.

功能概述 / Functionality:
1. 读取指定目录下所有符合“*_R.vtk”模式的曲线文件。
   Read all curve files in the specified directory matching the pattern "*_R.vtk".
2. 将曲线关于YZ平面进行镜面反转，即x坐标取反，其余坐标保持不变。
   Perform mirror reflection of the curve with respect to the YZ-plane (negate the x-coordinates, keep y and z unchanged).
3. 将镜像反转后的曲线保存为新文件，文件名后缀由“_R.vtk”替换为“_R2.vtk”。
   Save the mirrored curve to a new file, replacing the suffix "_R.vtk" with "_R2.vtk".

使用方法 / Usage:
- 修改代码中“files = glob.glob(...)”部分的路径为你的数据路径。
  Modify the path in the line "files = glob.glob(...)" to your data directory.
- 确保目录下的vtk文件符合“*_R.vtk”命名模式。
  Ensure that the vtk files in the directory follow the "*_R.vtk" naming pattern.
- 运行本脚本，即可在相同目录下生成“*_R2.vtk”镜像曲线文件。
  Run this script to generate mirrored curve files with the suffix "_R2.vtk" in the same directory.

注意 / Notes:
- 本程序依赖于`cut_centerline.py`文件中的`read_vtk_curve`、`cut_curve`、`interpolate_curve`、`write_vtk_curve`函数，请确保同目录下存在该文件。
  This program depends on the functions `read_vtk_curve`, `cut_curve`, `interpolate_curve`, and `write_vtk_curve` in `cut_centerline.py`.
  Make sure that this file is in the same directory as this script.
- 假设vtk文件为ASCII格式，数据类型为POLYDATA曲线。
  This program assumes that the vtk files are in ASCII format with the POLYDATA curve type.
"""


from cut_centerline import read_vtk_curve, cut_curve, interpolate_curve, write_vtk_curve
import numpy as np
import sys
import vtk
import glob 

def mirror_curve_yz(coords):
    mirrored_coords = coords.copy()
    mirrored_coords[:, 0] = -mirrored_coords[:, 0]
    return mirrored_coords

files = glob.glob('D:/!BraVa_src/ica_results/250216tuika/*.vtk')
print (files)


for input_file in files:
    output_file = input_file.replace(".vtk", "_MirroredV2.vtk")
    coords = read_vtk_curve(input_file)
    mirrored_coords = mirror_curve_yz(coords)
    write_vtk_curve(mirrored_coords, output_file)