import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

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