import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os
def mkdir(super_path,testname):
    #dir_path = test_dir_path+"{}\\".format(testname)
    dir_path = super_path+"{}/".format(testname)
    if os.path.exists(dir_path)==False:
        #print("making new directory {}...".format(dir_path))
        os.mkdir(dir_path)
    # else:
    #     print("generating in directory {}...".format(dir_path))
    return dir_path

def Get_simple_vtk(filepath, frenet=0):
    reader = vtk.vtkPolyDataReader()
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.SetFileName(filepath)
    reader.Update()
    polydata = reader.GetOutput()

    pts = polydata.GetPoints()    
    np_pts = np.array([pts.GetPoint(i) for i in range(pts.GetNumberOfPoints())])
    np_pts = np_pts - np_pts[0] # distalの始点を(0, 0, 0)まで移動
    # Curv = np.array(polydata.GetPointData().GetArray("Curvature"))
    # Tors = np.array(polydata.GetPointData().GetArray("Torsion"))
    return np_pts

def makeVtkFile(savePath, coords, scalarAttributes):
    v = open(savePath, "w+")
    v.write("# vtk DataFile Version 2.0\nVessel Segment\nASCII\nDATASET POLYDATA\nPOINTS {} float\n".format(len(coords)))
    for i in range(len(coords)):
        v.write("{} {} {}\n".format(coords[i,0], coords[i,1], coords[i,2]))

    v.write("LINES {} {}\n".format(1, len(coords)+1))
    v.write("{}".format(len(coords)))
    for i in range(len(coords)):
        v.write(" {}".format(i))
    v.write("\n")

    ####################################
    #        scalar Attributes         #
    ####################################

    if len(scalarAttributes) > 0:
        v.write("POINT_DATA {}\n".format(len(coords)))
        for i in range(len(scalarAttributes)):
            v.write("SCALARS {} {}\n".format(scalarAttributes[i][0], scalarAttributes[i][1]))
            v.write("LOOKUP_TABLE default\n")
            for j in range(len(coords)):
                    v.write("{}\n".format(scalarAttributes[i][2][j]))

    v.close()