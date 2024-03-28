import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from AngioMorphPCA.preprocessing import parameterize_curve
from AngioMorphPCA.io import Get_simple_vtk
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism
from AngioMorphPCA.srvf_rep import compute_srvf_func
from AngioMorphPCA.L2distance import calculate_l2_distance
from procrustes import rotational, orthogonal
from procrustes.generalized import generalized
from tqdm import tqdm

brava_files = glob.glob('brava_ica_mirrored/*.vtk')
aneurisk_files = glob.glob('aneurisk_ica_mirrored/*.vtk')
total_files = brava_files + aneurisk_files


# 原始曲线是f，SRVF是q
# 应当首先对f进行缩放使其长度为1，注意这有数学定义。（论文P1922）
# 接下来求q
# 最后求q的轨道[q]

first_resample_num = 1000
make_diffhomeo_num = 1000
second_resample_num = 100

# all_orbits = []
SRVF_functions = []

for i in range(len(total_files)):
    casename = total_files[i].split('\\')[-1].split('.')[0]
    temp = Get_simple_vtk(total_files[i])
    temp_centroid = np.mean(temp, axis=0)
    temp -= temp_centroid
    temp_func = parameterize_curve(temp)
    t_resampled = np.linspace(0, 1, first_resample_num)
    resampled_curve = temp_func(t_resampled)
    derivatives = np.gradient(resampled_curve, axis=0, edge_order=2)# 计算导数
    magnitude = np.linalg.norm(derivatives, axis=1)# 使用Simpson法则计算积分来得到曲线的长度，并缩放曲线
    integral = simps(magnitude, t_resampled)
    resampled_curve /= integral
    SRVF_func = compute_srvf_func(resampled_curve)
    SRVF_functions.append(SRVF_func)


distance_record = []  
aligned_shapes_record = [] 
for j in tqdm(range(make_diffhomeo_num)):
    SRVFs_reparam = []
    # for j in tqdm(range(make_diffhomeo_num)):
    for i in range(len(SRVF_functions)):
        SRVF_func = SRVF_functions[i]
        diff_homeo, coeffs = generate_diff_homeomorphism()
        y = diff_homeo(np.linspace(0, 1, second_resample_num))  
        SRVF_reparam = SRVF_func(y)
        SRVFs_reparam.append(SRVF_reparam)

    average_SRVF_reparam = np.mean(SRVFs_reparam, axis=0)

    shapes_stack = np.array(SRVFs_reparam)
    result = generalized(shapes_stack)

    # 从结果中提取对齐后的形状和平均形状
    aligned_shapes, new_distance_gpa = result
    distance_record.append(new_distance_gpa)
    aligned_shapes_record.append(aligned_shapes)
    # average_aligned_shape = np.mean(aligned_shapes, axis=0)

plt.hist(distance_record, bins=100)
plt.show()


# 只需要寻找令new_distance_gpa最小的reparameterization即可。