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
from datetime import datetime
import os
import pandas as pd


def mkdir(super_path,testname):
    #dir_path = test_dir_path+"{}\\".format(testname)
    dir_path = super_path+"{}/".format(testname)
    if os.path.exists(dir_path)==False:
        #print("making new directory {}...".format(dir_path))
        os.mkdir(dir_path)
    # else:
    #     print("generating in directory {}...".format(dir_path))
    return dir_path


brava_files = glob.glob('brava_ica_mirrored/*.vtk')
aneurisk_files = []
# aneurisk_files = glob.glob('aneurisk_ica_mirrored/*.vtk')
# pre_brava_files = glob.glob('brava_ica_mirrored/*.vtk')
# print (len(pre_brava_files), len(aneurisk_files))
# ill=pd.read_csv("./illcases.txt",header=None)
# ill = np.array(ill[0])

# print (ill)
# brava_files = []
# for i in range(len(pre_brava_files)):
#     fname = pre_brava_files[i].split('\\')[-1].split('.')[0].split('_')[0]
#     print (fname)
#     if fname not in ill:
#         brava_files.append(pre_brava_files[i])
# print (len(brava_files), len(aneurisk_files))
total_files = brava_files + aneurisk_files
np.save("total_files.npy", total_files)

start_time = datetime.now()
dir_formatted_time = start_time.strftime('%y-%m-%d-%H-%M-%S')
bkup_dir = mkdir("./", "save_orbits")
bkup_dir = mkdir(bkup_dir, dir_formatted_time)
log = open(bkup_dir+"log.txt", "w")
log.write("Start at: {}\n".format(dir_formatted_time))


# 原始曲线是f，SRVF是q
# 应当首先对f进行缩放使其长度为1，注意这有数学定义。（论文P1922）
# 接下来求q
# 最后求q的轨道[q]

first_resample_num = 1000
make_diffhomeo_num = 10000
second_resample_num = 100 #001^002:200;003:400
log.write("first_resample_num: {}\n".format(first_resample_num))
log.write("make_diffhomeo_num: {}\n".format(make_diffhomeo_num))
log.write("second_resample_num: {}\n".format(second_resample_num))


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
diff_homeo_record = []
L2_distance_record = []


def generalized_procrustes(curves):
    mean_curve = np.mean(curves, axis=0)
    new_curves = []
    for i in range(len(curves)):
        curves[i] = rotational(mean_curve, curves[i])['new_a']
        new_curves.append(curves[i])
    return new_curves


for j in tqdm(range(make_diffhomeo_num)):
    SRVFs_reparam = []
    # for j in tqdm(range(make_diffhomeo_num)):
    dh = []
    for i in range(len(SRVF_functions)):
        SRVF_func = SRVF_functions[i]
        diff_homeo, coeffs = generate_diff_homeomorphism()
        y = diff_homeo(np.linspace(0, 1, second_resample_num))  
        dh.append(y)
        SRVF_reparam = SRVF_func(y)
        SRVFs_reparam.append(SRVF_reparam)
    diff_homeo_record.append(dh)

    average_SRVF_reparam = np.mean(SRVFs_reparam, axis=0)

    shapes_stack = np.array(SRVFs_reparam)
    # aligned_shapes, new_distance_gpa = generalized(shapes_stack)
    aligned_shapes = generalized_procrustes(shapes_stack)
    new_distance_gpa = 0

    average_aligned_shape = np.mean(aligned_shapes, axis=0)
    total_L2 = 0
    for i in range(len(aligned_shapes)):
        total_L2 += calculate_l2_distance(aligned_shapes[i], average_aligned_shape)
        
    L2_distance_record.append(total_L2)
    distance_record.append(new_distance_gpa)
    aligned_shapes_record.append(aligned_shapes)
    # average_aligned_shape = np.mean(aligned_shapes, axis=0)

plt.hist(distance_record, bins=100)
plt.savefig(bkup_dir+'distance_record.png')
plt.close()


# 只需要寻找令new_distance_gpa最小的reparameterization即可。
# print(np.min(distance_record))
print(np.min(L2_distance_record))
min_idx = np.argmin(L2_distance_record)
min_reparam = aligned_shapes_record[min_idx]
min_dh = np.array(diff_homeo_record[min_idx])
print ("min_dh.shape", min_dh.shape)

fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
for i in range(len(min_reparam)):
    ax1.plot(min_reparam[i][:, 0], min_reparam[i][:, 1],color='black',alpha=0.5)
    ax2.plot(min_reparam[i][:, 0], min_reparam[i][:, 2],color='black',alpha=0.5)
    ax3.plot(min_reparam[i][:, 1], min_reparam[i][:, 2],color='black',alpha=0.5)
plt.grid(True)
fig.savefig(bkup_dir+'min_reparam.png')
plt.close()

average_min_reparam = np.mean(min_reparam, axis=0)

reconstruct_average_min = reconstruct_curve_from_srvf(average_min_reparam, np.array([0, 0, 0]))
reconstruct_average = reconstruct_curve_from_srvf(average_SRVF_reparam, np.array([0, 0, 0]))
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
ax1.plot(reconstruct_average_min[:, 0], reconstruct_average_min[:, 1], color='red')
ax2.plot(reconstruct_average_min[:, 0], reconstruct_average_min[:, 2], color='red')
ax3.plot(reconstruct_average_min[:, 1], reconstruct_average_min[:, 2], color='red')
ax1.plot(reconstruct_average[:, 0], reconstruct_average[:, 1], color='k')
ax2.plot(reconstruct_average[:, 0], reconstruct_average[:, 2], color='k')
ax3.plot(reconstruct_average[:, 1], reconstruct_average[:, 2], color='k')
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
fig.savefig(bkup_dir+'average_min_reparam.png')
plt.close()


np.save(bkup_dir+'average_min_reparam.npy', average_min_reparam)
np.save(bkup_dir+'min_reparam.npy', min_reparam)
np.save(bkup_dir+'min_dh.npy', min_dh)
