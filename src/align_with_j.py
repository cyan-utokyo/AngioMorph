import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from AngioMorphPCA.preprocessing import parameterize_curve, calculate_3d_curve_abscissas,remove_high_freq_components
from AngioMorphPCA.io import Get_simple_vtk, makeVtkFile, mkdir
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism
from AngioMorphPCA.srvf_rep import compute_srvf_func, reconstruct_curve_from_srvf
from AngioMorphPCA.L2distance import calculate_l2_distance
from AngioMorphPCA.compute_geometry import compute_curvature_and_torsion,build_curve_from_curvatures
from tqdm import tqdm
import matplotlib.pyplot as plt
from geomstats.learning.frechet_mean import FrechetMean
import geomstats.backend as gs
from geomstats.geometry.discrete_curves import (
    DiscreteCurvesStartingAtOrigin,
    SRVMetric,
    insert_zeros,
)


# 生成VTK文件内容
def generate_vtk(data, filename):
    with open(filename, 'w') as vtk_file:
        vtk_file.write("# vtk DataFile Version 3.0\n")
        vtk_file.write("Curve data\n")
        vtk_file.write("ASCII\n")
        vtk_file.write("DATASET POLYDATA\n")
        
        # 写入点数据
        num_points = len(data)
        vtk_file.write(f"POINTS {num_points} float\n")
        # for index, row in data.iterrows():
            # vtk_file.write(f"{row['x']} {row['y']} {row['z']}\n")
        for row in data:
            vtk_file.write(f"{row[0]} {row[1]} {row[2]}\n")
        
        # 写入拓扑数据
        vtk_file.write(f"LINES 1 {num_points + 1}\n")
        vtk_file.write(f"{num_points} " + " ".join(map(str, range(num_points))) + "\n")
        
        # # 写入点数据属性
        # vtk_file.write(f"POINT_DATA {num_points}\n")
        
        # # 写入 r 数据
        # vtk_file.write("SCALARS r float 1\n")
        # vtk_file.write("LOOKUP_TABLE default\n")
        # for value in data['r']:
        #     vtk_file.write(f"{value}\n")
        
        # # 写入 curvature 数据
        # vtk_file.write("SCALARS curvature float 1\n")
        # vtk_file.write("LOOKUP_TABLE default\n")
        # for value in data['curvature']:
        #     vtk_file.write(f"{value}\n")
        
        # # 写入 torsion 数据
        # vtk_file.write("SCALARS torsion float 1\n")
        # vtk_file.write("LOOKUP_TABLE default\n")
        # for value in data['torsion']:
        #     vtk_file.write(f"{value}\n")


def compute_centroid(curves):
    centroid = np.mean(curves, axis=0)
    return np.array(centroid)
def translate_to_centroid(curves):
    centroid = compute_centroid(curves)
    new_curves = []
    for i in range(len(curves)):
        new_curves.append(curves[i] - centroid)
    return np.array(new_curves)

def plot_curve(curve, ax=None, add_origin=True):
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

    if add_origin:
        curve = insert_zeros(curve, axis=-2)

    ax.plot(*[curve[:, k] for k in range(3)])
    ax.scatter(*[curve[0, k] for k in range(3)])
    return ax


def plot_geodesic(geod_points, ax=None, add_origin=True):
    n_times = geod_points.shape[0]
    k_sampling_points = geod_points.shape[-2] + 1

    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

    if add_origin:
        geod_points = insert_zeros(geod_points, axis=-2)

    ax.plot(*[geod_points[0, :, k] for k in range(3)],  c="b", linewidth=2)
    ax.plot(*[geod_points[-1, :, k] for k in range(3)], c="r", linewidth=2)

    for i in range(1, n_times - 1):
        ax.plot(*[geod_points[i, :, k] for k in range(3)], c="k", linewidth=1)

    for j in range(k_sampling_points - 1):
        ax.plot(*[geod_points[:, j, k] for k in range(3)], c="k", linewidth=1)

    return ax


brava_files = glob.glob('brava_cut_mirrored/*.vtk')
# aneurisk_files = glob.glob('aneurisk_cut_mirrored/*.vtk')
total_files = brava_files
print (len(total_files))
np.save("total_files_{}.npy".format(len(total_files)), total_files)
# total_files = glob.glob('vtk_files_85/*.vtk')
# print (total_files)
# np.save("total_files_85.npy", total_files)

resample_num=120
k_sampling_points = resample_num
# cutoffs = [100,100,95,97]
curves = []
# freq_threshold = 0.06
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
for i in range(len(total_files)):
    casename = total_files[i].split('\\')[-1].split('.')[0]
    print (total_files[i])
    temp = Get_simple_vtk(total_files[i])
    temp = translate_to_centroid(temp)
    temp_func = parameterize_curve(temp)
    t_resampled = np.linspace(0, 1, resample_num)
    resampled_curve = temp_func(t_resampled)
    curves.append(resampled_curve)
#     ax1.plot(resampled_curve[:,0],resampled_curve[:,1],label=casename)
#     # generate_vtk(resampled_curve, f"vtk_files_with_j/{casename}_interpolation.vtk")

curves = np.array(curves)
np.save("unaligned_curves_{}.npy".format(len(total_files)), curves)
# plt.tight_layout()
# plt.show()



# for i in range(len(total_files)):
#     casename = total_files[i].split('\\')[-1].split('.')[0]
#     temp = Get_simple_vtk(total_files[i])
#     temp = translate_to_centroid(temp)
#     temp_func = parameterize_curve(temp)
#     t_resampled = np.linspace(0, 1, resample_num)
#     resampled_curve = temp_func(t_resampled)
#     curves.append(resampled_curve)
#     # generate_vtk(resampled_curve, f"vtk_files_with_j/{casename}_interpolation.vtk")
# curves = np.array(curves)

curves_r3 = DiscreteCurvesStartingAtOrigin(
    ambient_dim=3, k_sampling_points=k_sampling_points, equip=False
)

curves_r3.equip_with_metric(SRVMetric)
curves_r3.equip_with_group_action(("rotations", "reparametrizations"))
curves_r3.equip_with_quotient()
curve_a = curves_r3.projection(curves[0])
curve_a = curves_r3.normalize(curve_a)
curve_bs = []
curve_bs.append(curve_a)
# fig= plt.figure(dpi=200)
# ax1 = fig.add_subplot(111,projection='3d')
# # ax2 = fig.add_subplot(122,projection='3d')
# plot_curve(curve_a, ax=ax1)
for i in tqdm(range(1,len(brava_files))):
    curve_b = curves_r3.projection(curves[i])
    curve_b = curves_r3.normalize(curve_b)




    curve_b_aligned = curves_r3.fiber_bundle.align(curve_b, curve_a)
    curve_bs.append(np.array(curve_b))

    hgeod_fun = curves_r3.quotient.metric.geodesic(curve_a, curve_b)

    n_times = 10
    times = gs.linspace(0.0, 1.0, n_times)
    hgeod = hgeod_fun(times)

#     plot_curve(curve_b_aligned, ax=ax1)
curve_bs = np.array(curve_bs)
# ax1.set_title("Aligned curves")
# # plot_geodesic(hgeod, ax=ax2)
# # ax2.set_title("Horizontal geodesic")
# # plt.show()
# plt.savefig("aligned_curves_bravawithj.png")
# plt.close()

save_dir = mkdir("./", "geom_aligned_curves_{}".format(len(total_files)))
# curve_bs = np.array(curve_bs)
np.save(save_dir+"geomstats_aligned_to_first_{}.npy".format(len(total_files)), curve_bs)

# mean = FrechetMean(curves_r3)
# mean.fit(curve_bs)
# mean_estimate = mean.estimate_
# curve_a = curves_r3.projection(mean_estimate)
# curve_a = curves_r3.normalize(curve_a)
# curve_cs = []
# curve_cs.append(curve_a)
# fig= plt.figure(dpi=200)
# ax1 = fig.add_subplot(111,projection='3d')
# # ax2 = fig.add_subplot(122,projection='3d')
# plot_curve(curve_a, ax=ax1)
# for i in tqdm(range(len(brava_files),len(total_files))):
# # for i in range(4):
#     curve_b = curves_r3.projection(curves[i])
#     curve_b = curves_r3.normalize(curve_b)

#     curves_r3.equip_with_group_action("rotations and reparametrizations")
#     curves_r3.equip_with_quotient_structure()

#     curve_b_aligned = curves_r3.fiber_bundle.align(curve_b, curve_a)
#     curve_cs.append(np.array(curve_b))

#     # hgeod_fun = curves_r3.quotient.metric.geodesic(curve_a, curve_b)
#     # n_times = 10
#     # times = gs.linspace(0.0, 1.0, n_times)
#     # hgeod = hgeod_fun(times)

#     plot_curve(curve_b_aligned, ax=ax1)
# curve_cs = np.array(curve_cs)
# ax1.set_title("Aligned curves")
# # plot_geodesic(hgeod, ax=ax2)
# # ax2.set_title("Horizontal geodesic")
# # plt.show()
# plt.savefig("aligned_curves_frechet_aneurisk.png")
# plt.close()

# # mean = FrechetMean(curves_r3)
# # mean.fit(curve_cs)

# # mean_estimate = mean.estimate_


# np.save(save_dir+"geomstats_aligned_to_frechet_aneurisk.npy", curve_cs)
