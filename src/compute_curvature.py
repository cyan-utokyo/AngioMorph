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
from AngioMorphPCA.compute_geometry import compute_curvature_and_torsion


def mkdir(super_path,testname):
    #dir_path = test_dir_path+"{}\\".format(testname)
    dir_path = super_path+"{}/".format(testname)
    if os.path.exists(dir_path)==False:
        #print("making new directory {}...".format(dir_path))
        os.mkdir(dir_path)
    # else:
    #     print("generating in directory {}...".format(dir_path))
    return dir_path

def remove_high_freq_components(data, freq_threshold):
    """
    使用傅立叶变换去除高频成分。
    
    参数:
    - data: 一维数组，输入数据。
    - freq_threshold: float，频率阈值，用于确定哪些频率成分被视为高频并需要被去除。
    
    返回:
    - filtered_data: 一维数组，滤波后的数据。
    """
    # 执行傅立叶变换
    data_fft = np.fft.fft(data)
    # 获取频率
    freq = np.fft.fftfreq(len(data))
    
    # 根据频率阈值滤除高频成分
    data_fft[np.abs(freq) > freq_threshold] = 0
    
    # 执行逆傅立叶变换
    filtered_data = np.fft.ifft(data_fft)
    
    # 返回实部，去除由于计算引入的虚部（应该接近于零）
    return filtered_data.real

def compute_centroid(curves):
    centroid = np.mean(curves, axis=0)
    return np.array(centroid)
def translate_to_centroid(curves):
    centroid = compute_centroid(curves)
    new_curves = []
    for i in range(len(curves)):
        new_curves.append(curves[i] - centroid)
    return np.array(new_curves)

brava_files = glob.glob('brava_ica_mirrored/*.vtk')
# aneurisk_files = []
aneurisk_files = glob.glob('aneurisk_ica_mirrored/*.vtk')

total_files = brava_files + aneurisk_files
np.save("total_files.npy", total_files)

resample_num=120
start_time = datetime.now()
dir_formatted_time = start_time.strftime('%y-%m-%d-%H-%M-%S')
bkup_dir = mkdir("./", "save_orbits")
bkup_dir = mkdir(bkup_dir, dir_formatted_time)
log = open(bkup_dir+"log.txt", "w")
log.write("Start at: {}\n".format(dir_formatted_time))

curvatures=[]

from dtw import *

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

for i in range(len(total_files)):
    casename = total_files[i].split('\\')[-1].split('.')[0]
    temp = Get_simple_vtk(total_files[i])
    temp = translate_to_centroid(temp)
    temp_func = parameterize_curve(temp)
    t_resampled = np.linspace(0, 1, resample_num)
    resampled_curve = temp_func(t_resampled)
    c, t = compute_curvature_and_torsion(resampled_curve)
    ax1.plot(c, label=casename)
    fft_c = remove_high_freq_components(c, 0.05)
    ax2.plot(fft_c, label=casename)
    ax1.set_title('Curvature')
    ax2.set_title('Curvature (filtered)')
    print (len(c), len(fft_c))
    curvatures.append(fft_c)
curvatures = np.array(curvatures)
average_curvature = np.mean(curvatures, axis=0)
for i in range(len(curvatures)):
    alignment = dtw(average_curvature, curvatures[i], keep_internals=True)
    path = alignment.index1, alignment.index2
    aligned_c2 = curvatures[i][path[1]]
    ax3.plot(aligned_c2, label='Aligned '+str(i))
ax2.plot(np.mean(curvatures, axis=0), label='Mean',linewidth=3, color='black')
ax3.plot(np.mean(curvatures, axis=0), label='Mean',linewidth=3, color='black')
plt.show()


