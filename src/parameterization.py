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


total_files = np.load("total_files.npy", allow_pickle=True)
min_dh = np.load('save_orbits/24-04-01-12-44-52/min_dh.npy',allow_pickle=True)

print (len(total_files), len(min_dh))

# 原始曲线是f，SRVF是q
# 应当首先对f进行缩放使其长度为1，注意这有数学定义。（论文P1922）
# 接下来求q
# 最后求q的轨道[q]

first_resample_num = 100
make_diffhomeo_num = 1000
second_resample_num = 100


all_L2_table = []
interpolation_nums = np.array([100])


def scale_curve(curve):
    derivatives = np.gradient(curve, axis=0, edge_order=2)# 计算导数
    magnitude = np.linalg.norm(derivatives, axis=1)# 使用Simpson法则计算积分来得到曲线的长度，并缩放曲线
    integral = simps(magnitude, np.linspace(0, 1, len(curve)))
    curve /= integral
    return curve

fig=plt.figure()
ax1=fig.add_subplot(131)
ax2=fig.add_subplot(132)
ax3=fig.add_subplot(133)


for second_resample_num in interpolation_nums:
    # all_orbits = []
    SRVF_functions = []
    non_param_curves = []
    SRVFs_unit_parameterized = []
    SRVFs_re_parameterized = []
    re_param_curves = []
    for i in range(len(total_files)):
        casename = total_files[i].split('\\')[-1].split('.')[0]
        temp = Get_simple_vtk(total_files[i])
        temp_func = parameterize_curve(temp)

        t_resampled = np.linspace(0, 1, first_resample_num)
        unit_sampled_curve = temp_func(t_resampled)
        non_param_curves.append(unit_sampled_curve)
        unit_sampled_curve = scale_curve(unit_sampled_curve)
        SRVF_func = compute_srvf_func(unit_sampled_curve)
        SRVF_functions.append(SRVF_func)

    for i in range(len(SRVF_functions)):
        SRVF_unit_parameterized = SRVF_functions[i](np.linspace(0, 1, second_resample_num))
        SRVFs_unit_parameterized.append(SRVF_unit_parameterized)
        SRVF_re_parameterized = SRVF_functions[i](min_dh[i])
        SRVFs_re_parameterized.append(SRVF_re_parameterized)
    SRVFs_unit_parameterized, _ = generalized(SRVFs_unit_parameterized)
    average_SRVF_unit_parameterized = np.mean(SRVFs_unit_parameterized, axis=0)
    average_SRVF_unit_curve = scale_curve(reconstruct_curve_from_srvf(average_SRVF_unit_parameterized, np.array([0,0,0])))
    ax2.plot(average_SRVF_unit_curve[:, 0], average_SRVF_unit_curve[:, 1],label=second_resample_num, marker='.', alpha=0.7)

    SRVFs_re_parameterized, _ = generalized(SRVFs_re_parameterized)
    average_SRVF_re_parameterized = np.mean(SRVFs_re_parameterized, axis=0)
    average_SRVF_re_curve = scale_curve(reconstruct_curve_from_srvf(average_SRVF_re_parameterized, np.array([0,0,0])))
    ax3.plot(average_SRVF_re_curve[:, 0], average_SRVF_re_curve[:, 1],label=second_resample_num, marker='.', alpha=0.7)

    non_param_curves, _ = generalized(non_param_curves)
    average_non_param_curve = scale_curve(np.mean(non_param_curves, axis=0))
    ax1.plot(average_non_param_curve[:, 0], average_non_param_curve[:, 1],label=second_resample_num, marker='.', alpha=0.7)
ax1.legend()
ax2.legend()
ax3.legend()
fig.savefig('average_curves.png')
plt.close(fig)


for i in range(len(min_dh)):
    plt.plot(range(len(min_dh[i])), min_dh[i])
plt.show()