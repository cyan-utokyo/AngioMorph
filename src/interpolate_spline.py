import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from AngioMorphPCA.preprocessing import parameterize_curve, calculate_3d_curve_abscissas,remove_high_freq_components, min_max_normalize, autocovariance_function
from AngioMorphPCA.io import Get_simple_vtk, makeVtkFile
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism
from AngioMorphPCA.srvf_rep import compute_srvf_func, reconstruct_curve_from_srvf
from AngioMorphPCA.L2distance import calculate_l2_distance
from AngioMorphPCA.compute_geometry import compute_curvature_and_torsion,build_curve_from_curvatures
from tqdm import tqdm

files = glob.glob('D:/!BraVa_src/ica_results/250216tuika/250221added/*.vtk')
print (files)

curves = []
for f in files:
    filename = f.split('\\')[-1][:8]
    print (filename)
    curve = Get_simple_vtk(f)
    t = np.linspace(0,1,120)
    function_c = parameterize_curve(curve)
    parameterized_c = function_c(t)
    if 'L' in filename:
        parameterized_c[:,0] = -parameterized_c[:,0]
    parameterized_c = parameterized_c - parameterized_c[0]
    curves.append(parameterized_c)

curves = np.array(curves)
for i in range(len(curves)):
    filename = files[i].split('\\')[-1][:8]
    makeVtkFile('D:/!BraVa_src/ica_results/250216tuika/250221added/'+filename+'.vtk',curves[i],[])
# #     plt.plot(curves[i,:,0], curves[i,:,1])

# plt.show()



