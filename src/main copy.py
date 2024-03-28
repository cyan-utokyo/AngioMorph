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
from procrustes import rotational
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


all_L2_table = []
interpolation_nums = np.array([50, 100, 200, 400, 800, 1600])
for second_resample_num in interpolation_nums:
    # all_orbits = []
    SRVF_functions = []
    for i in range(len(total_files)):
        casename = total_files[i].split('\\')[-1].split('.')[0]
        temp = Get_simple_vtk(total_files[i])
        temp_func = parameterize_curve(temp)
        t_resampled = np.linspace(0, 1, first_resample_num)
        resampled_curve = temp_func(t_resampled)
        derivatives = np.gradient(resampled_curve, axis=0, edge_order=2)# 计算导数
        magnitude = np.linalg.norm(derivatives, axis=1)# 使用Simpson法则计算积分来得到曲线的长度，并缩放曲线
        integral = simps(magnitude, t_resampled)
        resampled_curve /= integral
        SRVF_func = compute_srvf_func(resampled_curve)
        SRVF_functions.append(SRVF_func)
    SRVFs_unit_parameterized = []
    for i in range(len(SRVF_functions)):
        SRVF_unit_parameterized = SRVF_functions[i](np.linspace(0, 1, second_resample_num))
        SRVFs_unit_parameterized.append(SRVF_unit_parameterized)
    average_SRVF_unit_parameterized = np.mean(SRVFs_unit_parameterized, axis=0)

    for i in range(len(SRVFs_unit_parameterized)):
        SRVFs_unit_parameterized[i] = rotational(SRVFs_unit_parameterized[i], average_SRVF_unit_parameterized,translate=False, scale=False)["new_a"]
        SRVF_functions[i] = compute_srvf_func(SRVFs_unit_parameterized[i])

    all_l2 = []
    print ("second_resample_num:", second_resample_num)
    for j in tqdm(range(make_diffhomeo_num)):
        SRVFs_reparameterized = []
        sum_L2 = 0
        for i in range(len(SRVF_functions)):
            diff_homeo, coeffs = generate_diff_homeomorphism()
            x = np.linspace(0, 1, second_resample_num)
            y = diff_homeo(x)
            SRVF_reparameterized = SRVF_func(y)
            # SRVF_reparameterized = rotational(SRVF_reparameterized, average_SRVF_unit_parameterized,translate=False, scale=False)["new_a"]
            SRVFs_reparameterized.append(SRVF_reparameterized)
        average_SRVF = np.mean(SRVFs_reparameterized, axis=0)
        for i in range(len(SRVFs_reparameterized)):
            sum_L2 += calculate_l2_distance(SRVFs_reparameterized[i], average_SRVF)/second_resample_num
        # print ("sum_L2:", sum_L2)
        all_l2.append(sum_L2)
    all_L2_table.append(all_l2)


fig = plt.figure(dpi=300)
ax = fig.add_subplot(111)
for i in range(len(all_L2_table)):
    ax.hist(all_L2_table[i], bins=100, alpha=0.5, label=str(interpolation_nums[i]))
plt.legend()
plt.savefig("L2_distance.png")
plt.close()

fig = plt.figure(dpi=300)
ax = fig.add_subplot(111)
ax.boxplot(all_L2_table, showfliers=False)
plt.xticks(np.arange(1, len(interpolation_nums)+1), interpolation_nums)
# plt.xticks(1/interpolation_nums)
plt.savefig("L2_distance_boxplot.png")
plt.close()

fig = plt.figure(dpi=300)
ax = fig.add_subplot(111)
ax.plot(1/interpolation_nums, np.mean(all_L2_table, axis=1))
plt.savefig("L2_distance_mean.png")
plt.close()



all_L2_table = np.array(all_L2_table)
np.save("all_L2_table.npy", all_L2_table)

# compute average curve resolution
