import numpy as np 
import glob 
import vtk

brava_files = glob.glob('brava_ica_mirrored/*.vtk')
aneurisk_files = glob.glob('aneurisk_ica_mirrored/*.vtk')
total_files = brava_files + aneurisk_files

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
        

for i in range(len(total_files)):
    print (total_files[i])
    temp = Get_simple_vtk(total_files[i])
    print(temp.shape, temp[0])
    
