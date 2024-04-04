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


# 定义旋转矩阵函数
def rotate_y_matrix(theta):
    theta = np.radians(theta)  # 将角度转换为弧度
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

theta = 45  # 旋转角度，这里是45度

root_dir = "save_orbits/24-04-03-14-59-10/"

total_files = np.load("total_files.npy", allow_pickle=True)
min_reparam = np.load(root_dir+'min_reparam.npy',allow_pickle=True)
resampled_unit_curves = np.load(root_dir+'resampled_unit_curves.npy',allow_pickle=True)
curves = []
for i in range(len(total_files)):
    curve = reconstruct_curve_from_srvf(min_reparam[i][:,:3], np.zeros(3))
    curves.append(curve)
curves = np.array(curves)

fig = plt.figure(figsize=(3,10))
ax = fig.add_subplot(111)
for theta in [0,45,90]:
    rotated_points = curves[7].dot(rotate_y_matrix(theta))
    # rotated_points = resampled_unit_curves[0].dot(rotate_y_matrix(theta))
    ax.plot(rotated_points[:,0], rotated_points[:,1],linewidth=1)
    ax.scatter(rotated_points[::3,0], rotated_points[::3,1], s=15, c='k')
ax.invert_yaxis()
plt.show()