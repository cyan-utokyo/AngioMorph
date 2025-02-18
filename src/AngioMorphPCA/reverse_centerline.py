from cut_centerline import read_vtk_curve, cut_curve, interpolate_curve, write_vtk_curve
import numpy as np
import sys
import vtk
import glob 

def reverse_curve(coords):
    reversed_coords = coords[::-1]
    return reversed_coords

files = glob.glob('D:/!BraVa_src/ica_results/250216tuika/*.vtk')
print (files)


for input_file in files:
    output_file = input_file.replace(".vtk", "_reverse.vtk")
    coords = read_vtk_curve(input_file)
    reversed_coords = reverse_curve(coords)
    write_vtk_curve(reversed_coords, output_file)