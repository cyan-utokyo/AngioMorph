import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
from AngioMorphPCA.preprocessing import parameterize_curve, calculate_3d_curve_abscissas,remove_high_freq_components, min_max_normalize, autocovariance_function
from AngioMorphPCA.io import Get_simple_vtk, makeVtkFile
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism
from AngioMorphPCA.srvf_rep import compute_srvf_func, reconstruct_curve_from_srvf
from AngioMorphPCA.L2distance import calculate_l2_distance
from AngioMorphPCA.compute_geometry import compute_curvature_and_torsion,build_curve_from_curvatures
from tqdm import tqdm
import warnings
import matplotlib.pyplot as plt
# from geomstats.learning.frechet_mean import FrechetMean
# import geomstats.backend as gs
# from geomstats.geometry.discrete_curves import (
#     DiscreteCurvesStartingAtOrigin,
#     SRVMetric,
#     insert_zeros,
# )
# from geomstats.learning.pca import TangentPCA
import seaborn as sns
import matplotlib.cm as cm
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes
from AngioMorphPCA.cut_centerline import read_vtk_curve, cut_curve, interpolate_curve, write_vtk_curve
from AngioMorphPCA.io import Get_simple_vtk, makeVtkFile, mkdir
from datetime import datetime
from sklearn.mixture import GaussianMixture
from skopt import gp_minimize
from skopt.space import Integer, Real
from scipy.stats import gamma, kstest, shapiro, norm as norm_dist
import warnings
from geneticalgorithm import geneticalgorithm as ga
from functools import partial

# 屏蔽 skopt 优化器重复点警告
warnings.filterwarnings(
    "ignore",
    message="The objective has been evaluated at point",
    category=UserWarning
)

# 屏蔽 sklearn KMeans MKL 内存泄漏警告
warnings.filterwarnings(
    "ignore",
    message="KMeans is known to have a memory leak on Windows with MKL",
    category=UserWarning
)

# 屏蔽 seaborn 的 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

warnings.filterwarnings("ignore", category=RuntimeWarning)

np.seterr(all='ignore')




def calculate_curve_length(curve):
    """
    计算形状为 (n, 3) 的 3D 曲线的总长度。
    参数:
        curve (numpy.ndarray): 形状为 (n, 3) 的 3D 曲线，包含 n 个点的坐标 (x, y, z)。
    返回:
        float: 曲线的总长度。
    """
    # 计算相邻点之间的差值
    diffs = np.diff(curve, axis=0)

    # 计算每个差值的欧氏距离，并求和
    segment_lengths = np.sqrt((diffs ** 2).sum(axis=1))
    total_length = segment_lengths.sum()
    
    return total_length

def calculate_norm(curve):
    """
    计算3D曲线的norm（曲线的范数）。
    参数:
        curve (numpy.ndarray): 形状为 (n, 3) 的 3D 曲线，包含 n 个点的坐标 (x, y, z)。
    返回:
        float: 曲线的norm。
    """
    if len(curve) < 2:
        raise ValueError("曲线至少需要两个点")

    # 计算端点距离
    end_to_end_distance = np.linalg.norm(curve[-1] - curve[0])

    if end_to_end_distance == 0:
        raise ValueError("曲线起点和终点重合，无法计算norm")

    return end_to_end_distance

def calculate_tortuosity(curve):
    """
    计算3D曲线的tortuosity（曲折度）。
    参数:
        curve (numpy.ndarray): 形状为 (n, 3) 的 3D 曲线，包含 n 个点的坐标 (x, y, z)。
    返回:
        float: 曲线的tortuosity。
    """
    if len(curve) < 2:
        raise ValueError("曲线至少需要两个点")

    # 计算曲线长度
    curve_length = calculate_curve_length(curve)

    # 计算端点距离
    end_to_end_distance = calculate_norm(curve)

    # 计算tortuosity
    tortuosity = curve_length / end_to_end_distance

    return tortuosity


def calculate_abscissas(curve):
    """
    计算形状为 (n, 3) 的 3D 曲线每个点的累计弧长（abscissas）。
    
    参数:
        curve (numpy.ndarray): 形状为 (n, 3) 的 3D 曲线，包含 n 个点的坐标 (x, y, z)。
    
    返回:
        numpy.ndarray: 一个形状为 (n,) 的数组，包含每个点对应的累计弧长。
    """
    # 计算相邻点之间的差值
    diffs = np.diff(curve, axis=0)
    
    # 计算每个相邻点对之间的距离
    segment_lengths = np.sqrt((diffs ** 2).sum(axis=1))
    
    # 计算累计弧长，起始点的弧长为 0
    abscissas = np.concatenate(([0], np.cumsum(segment_lengths)))
    
    return abscissas


def resample_standardized_curves(standardized_centerlines, standardized_abscissas, m):
    """
    Resample each curve in standardized_centerlines to have exactly m points.

    :param standardized_centerlines: List of (n,3) numpy arrays representing 3D curves.
    :param standardized_abscissas: List of (n,) numpy arrays representing abscissas corresponding to each curve.
    :param m: The number of points each resampled curve should have.
    :return: (new_centerlines, new_abscissas), both resampled to m points.
    """
    new_centerlines = []
    new_abscissas = []

    for i in range(len(standardized_centerlines)):
        curve = standardized_centerlines[i]  # (n,3)
        abscissas = standardized_abscissas[i]  # (n,)

        # 生成新的m个等间距 abscissas
        new_t = np.linspace(abscissas[0], abscissas[-1], m)

        # 分别对 x, y, z 进行插值
        interp_x = interp1d(abscissas, curve[:, 0], kind='cubic', fill_value="extrapolate")
        interp_y = interp1d(abscissas, curve[:, 1], kind='cubic', fill_value="extrapolate")
        interp_z = interp1d(abscissas, curve[:, 2], kind='cubic', fill_value="extrapolate")

        # 计算新的坐标
        new_x = interp_x(new_t)
        new_y = interp_y(new_t)
        new_z = interp_z(new_t)

        # 组合 x, y, z
        new_curve = np.vstack((new_x, new_y, new_z)).T  # (m, 3)

        # 存储结果
        new_centerlines.append(new_curve)
        new_abscissas.append(new_t)

    return new_centerlines, new_abscissas

def align_centerlines_procrustes(original_centerlines):
    num_curves, num_points, dim = original_centerlines.shape
    
    # 选择第一条曲线作为参考
    reference_curve = original_centerlines[0]

    aligned_centerlines = np.zeros_like(original_centerlines)

    for i in range(num_curves):
        _, aligned_curve, _ = procrustes(reference_curve, original_centerlines[i])
        aligned_centerlines[i] = aligned_curve

    return aligned_centerlines



brava_files = glob.glob('brava_cut_mirrored/*.vtk')
added_brava_files = glob.glob('250216tuika/*.vtk')
# curve_bs = 
total_files = brava_files + added_brava_files
root_dir = mkdir("./", "cut_for_better_distribution_{}".format(len(total_files)))
timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
print (timestamp)
# save_dir = mkdir(root_dir, timestamp)

output_files = []
coords_list = []
tortuosities = []
lengths = []
curve_norms = []
std_coords = []
abscissas_list = []
std_abscissas = []

for input_file in total_files:
    filename = input_file.split("\\")[-1]
    # output_file = save_dir + filename
    coords = read_vtk_curve(input_file)
    coords = coords - coords[0]
    coords_list.append(coords)
    # output_files.append(output_file)
    lengths.append(round(calculate_curve_length(coords),2))
    tortuosities.append(round(calculate_tortuosity(coords),2))
    curve_norms.append(round(calculate_norm(coords),2))
    std_coords.append(coords/calculate_curve_length(coords))
    abscissas_list.append(calculate_abscissas(coords))
    std_abscissas.append(calculate_abscissas(coords)/calculate_curve_length(coords))


coords_list = np.array(coords_list)
std_coords = np.array(std_coords)
abscissas_list = np.array(abscissas_list)
std_abscissas = np.array(std_abscissas)

M=120

resampled_standardized_centerlines, resampled_standardized_abscissas = resample_standardized_curves(std_coords, std_abscissas, M)
resampled_standardized_centerlines = np.array(resampled_standardized_centerlines)
align_resampled_standardized_centerlines = align_centerlines_procrustes(resampled_standardized_centerlines)

# fig2 = plt.figure(figsize=(7,2), dpi=100)
# # fig2.suptitle(f"interval={interval} (scaled to 75mm)")
# ax2_1 = fig2.add_subplot(131)
# ax2_2 = fig2.add_subplot(132)
# ax2_3 = fig2.add_subplot(133)
# for j in range(len(align_resampled_standardized_centerlines)):
#     ax2_1.scatter(resampled_standardized_abscissas[j], align_resampled_standardized_centerlines [j][:,0], s=1)
#     ax2_2.scatter(resampled_standardized_abscissas[j], align_resampled_standardized_centerlines [j][:,1], s=1)
#     ax2_3.scatter(resampled_standardized_abscissas[j], align_resampled_standardized_centerlines [j][:,2], s=1)
# ax2_1.set_title("x")
# ax2_2.set_title("y")
# ax2_3.set_title("z")
# plt.show()



# 构建数据框
df = pd.DataFrame({
    'Length': lengths,
    'Tortuosity': tortuosities,
    'Norm': curve_norms
})

df_before = pd.DataFrame({
    'Length': lengths,
    'Tortuosity': tortuosities,
    'Norm': curve_norms
})

# 设置绘图风格
sns.set(style="whitegrid")

correlation_matrix = df.corr(method='pearson')
print(correlation_matrix)

'''
              Length  Tortuosity      Norm
Length      1.000000    0.602379  0.449706
Tortuosity  0.602379    1.000000 -0.435910
Norm        0.449706   -0.435910  1.000000

长曲线倾向于更曲折，但长曲线的起点和终点不一定很远。
说明解剖学上的scale是有一定范围的，如果length过于长，那其实是因为血管折叠起来了，而不是因为此人的scale很大。

'''
pca = PCA(n_components=10)
scaler = StandardScaler()
coords_scaled = scaler.fit_transform(align_resampled_standardized_centerlines.reshape(len(align_resampled_standardized_centerlines), -1))
results = pca.fit_transform(coords_scaled)
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
print("Explained variance ratio: ", explained_variance_ratio)
print("Cumulative variance ratio: ", cumulative_variance_ratio)

def scale_curve(coords, scale_factor):
    return coords * scale_factor


min_length = min(lengths)
max_length = max(lengths)

tortuosities = np.array(tortuosities).reshape(-1, 1)

gmm = GaussianMixture(n_components=2, random_state=42)
gmm.fit(tortuosities)
means = gmm.means_.flatten()
stds = np.sqrt(gmm.covariances_).flatten()

tortuosities = np.array(tortuosities).flatten()

print(f"峰1：均值={means[0]:.2f}, 标准差={stds[0]:.2f}")
print(f"峰2：均值={means[1]:.2f}, 标准差={stds[1]:.2f}")

if means[0] > means[1]:
    means = means[::-1]
    stds = stds[::-1]

suspect_indices = []
for i, t in enumerate(tortuosities.flatten()):
    if t > means[1] + 1.5 * stds[1]:
        suspect_indices.append(i)

print(f"疑似异常曲线索引: {suspect_indices}, 异常曲线文件名：{np.array(total_files)[suspect_indices]}")

# 保存修剪后的 tortuosity、length、norm
tortuosities_after = tortuosities.copy()
lengths_after = lengths.copy()
curve_norms_after = curve_norms.copy()

# 长度和 Norm 的目标分布
length_shape, length_loc, length_scale = gamma.fit(lengths)
target_length_dist = gamma(length_shape, loc=length_loc, scale=length_scale)

norm_mean, norm_std = np.mean(curve_norms_after), np.std(curve_norms_after)
target_norm_dist = norm_dist(norm_mean, norm_std)


def global_objective(X, coords_list, min_length, max_length, gmm, target_length_dist, target_norm_dist):
    X = X.reshape(-1, 3)
    loss = 0
    penalty = 0
    eps = 1e-6

    for i in range(len(X)):
        n, m, s = int(round(X[i, 0])), int(round(X[i, 1])), X[i, 2]
        coords = coords_list[i]

        # 柔和的惩罚：如果 n + m 太大，惩罚，但不是直接死刑
        if n + m >= len(coords) - 2:
            penalty += 1
            loss += 500
            print(f"Evaluating: n={n}, m={m}, s={s:.2f}, length=裁剪失败, loss={loss:.2f}, penalty={penalty}")
            continue

        cut_coords = cut_curve(coords, n, len(coords) - 1 - m)
        scaled_coords = scale_curve(cut_coords, s)

        new_t = calculate_tortuosity(scaled_coords)
        new_l = calculate_curve_length(scaled_coords)
        new_n = calculate_norm(scaled_coords)

        # 柔和的惩罚：如果长度超界，增加惩罚，而不是直接炸掉
        length_penalty = 0
        if new_l < min_length:
            length_penalty = (min_length - new_l) / min_length * 50
        if new_l > max_length:
            length_penalty = (new_l - max_length) / max_length * 50

        t_nll = -np.log(max(gmm.score_samples([[new_t]])[0], eps))
        l_nll = -np.log(max(target_length_dist.pdf(new_l), eps))
        n_nll = -np.log(max(target_norm_dist.pdf(new_n), eps))

        loss += t_nll + 0.2 * l_nll + 0.2 * n_nll + length_penalty

        print(f"Evaluating: n={n}, m={m}, s={s:.2f}, length={new_l:.2f}, loss={loss:.2f}, penalty={penalty}")

    loss += penalty * 500
    return loss

# coords_list = coords_list[:3]

# partial 绑定参数
objective_with_data = partial(
    global_objective,
    coords_list=coords_list,
    min_length=min_length,
    max_length=max_length,
    gmm=gmm,
    target_length_dist=target_length_dist,
    target_norm_dist=target_norm_dist
)

varbound = np.array([[0, 10], [0, 10], [0.8, 1.5]] * len(coords_list))

algorithm_param = {
    'max_num_iteration': 500,
    'population_size': 300,
    'mutation_probability': 0.3,
    'elit_ratio': 0.01,
    'crossover_probability': 0.7,
    'parents_portion': 0.3,
    'crossover_type': 'uniform',
    'max_iteration_without_improv': 100  # 不建议写 None，否则有时死循环
}


model = ga(
    function=objective_with_data,
    dimension=len(coords_list) * 3,
    variable_type='real',
    variable_boundaries=varbound,
    algorithm_parameters=algorithm_param
)

# 运行遗传算法优化
model.run()

# 取出优化结果
result = model.output_dict

# 最优参数
best_params = result['variable']
optimized_params = best_params.reshape(-1, 3)

print("优化完成！参数如下：")
for i, (n, m, s) in enumerate(optimized_params):
    n = int(round(n))
    m = int(round(m))
    s = float(s)
    print(f"曲线 {i}: 剪切头部 {n} 个点，剪切尾部 {m} 个点，缩放 {s:.2f} 倍")

# 输出最终目标函数值
print(f"最终目标函数值: {result['function']}")

# 应用优化参数到曲线
coords_list_after = []

for i, (n, m, s) in enumerate(optimized_params):
    n = int(round(n))
    m = int(round(m))
    s = float(s)

    coords = coords_list[i]
    cut_coords = cut_curve(coords, n, len(coords) - 1 - m)
    scaled_coords = scale_curve(cut_coords, s)
    interpolated_coords = interpolate_curve(scaled_coords, num_interpolated=len(coords))

    coords_list_after.append(interpolated_coords)

coords_list_after = np.array(coords_list_after)

# 保存优化后的曲线数据
np.save("coords_list_after.npy", coords_list_after)
