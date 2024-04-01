import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from AngioMorphPCA.preprocessing import parameterize_curve
from AngioMorphPCA.io import Get_simple_vtk
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism
from AngioMorphPCA.srvf_rep import compute_srvf_func, reconstruct_curve_from_srvf
from AngioMorphPCA.L2distance import calculate_l2_distance
from procrustes import rotational, orthogonal
from procrustes.generalized import generalized
from tqdm import tqdm
min_reparam = np.load("../004（400）/min_reparam.npy")

print (min_reparam.shape)

reconstructed_curve = []
for i in range(len(min_reparam)):
    reconstructed_curve.append(reconstruct_curve_from_srvf(min_reparam[i],np.array([0,0,0])))
    plt.plot(reconstructed_curve[i][:,0], reconstructed_curve[i][:,1])
plt.show()