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
from procrustes import rotational,generalized
from tqdm import tqdm
from AngioMorphPCA.compute_geometry import compute_curvature_and_torsion
import pandas as pd
import geomstats.backend as gs
from geomstats.geometry.euclidean import Euclidean
from geomstats.geometry.discrete_curves import DiscreteCurves


r3 = Euclidean(dim=3)
curves_r3 = DiscreteCurves(ambient_manifold=r3)



# 定义旋转矩阵函数
def rotate_y_matrix(theta=45):
    theta = np.radians(theta)  # 将角度转换为弧度
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

root_dir = "save_orbits/24-04-03-14-59-10/"

total_files = np.load("total_files.npy", allow_pickle=True)
min_reparam = np.load(root_dir+'min_reparam.npy',allow_pickle=True)
resampled_unit_curves = np.load(root_dir+'resampled_unit_curves.npy',allow_pickle=True)
curves = []


for i in range(len(total_files)):
    curve = reconstruct_curve_from_srvf(min_reparam[i][:,:3], np.zeros(3))
    curves.append(curve)
curves = np.array(curves)

k_sampling_points = 50

curve_a = curves[4]#.dot(rotate_y_matrix(theta=60))
curve_b = curves[19]#.dot(rotate_y_matrix(theta=60))

curvature_a,_ = compute_curvature_and_torsion(curve_a)
curvature_b,_ = compute_curvature_and_torsion(curve_b)

geod_fun = curves_r3.metric.geodesic(curve_a, curve_b)
n_times = 16
times = gs.linspace(0.0, 1.0, n_times)
geod = geod_fun(times)

cdx = 0
cdy = 1
cdz = 2
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot(geod[0, :, cdx], geod[0, :, cdy], geod[0, :, cdz], "o-b")
#plt.plot(interpolated_curves[a][:,0],interpolated_curves[a][:,1],label=filename_a)
for i in range(1, n_times - 1):
    r = i / (n_times - 1)
    ax.plot(geod[i, :, cdx], geod[i, :, cdy], geod[i, :, cdz], "--k",alpha=0.5)
for j in range(0,geod.shape[1],3):
        if curvature_a[j] > 0.1:
            c = "r"
        elif curvature_b[j] >0.1:
            c = "b"
        else:
             c =    "k"
        ax.plot(geod[:, j, 0], geod[:, j, 1], geod[:, j, 2], "-",color=c)
ax.plot(geod[-1, :, cdx], geod[-1, :, cdy], geod[-1, :, cdz], "o-r")
plt.title("Geodesic for the Square Root Velocity metric")
plt.legend()
# plt.grid(linestyle="--",alpha=0.5)
ax.invert_yaxis()
plt.show()