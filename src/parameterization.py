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

root_dir = "save_orbits/24-04-03-14-59-10/"

total_files = np.load("total_files.npy", allow_pickle=True)
min_reparam = np.load(root_dir+'min_reparam.npy',allow_pickle=True)
resampled_unit_curves = np.load(root_dir+'resampled_unit_curves.npy',allow_pickle=True)
colors = np.zeros(len(min_reparam))
colors[82:]=1
aneurisk_meta = pd.read_csv('aneuriskmeta.csv')

# print (aneurisk_meta.case_id)
aneurysmLocation = np.array(['N']*len(total_files))
aneurysmType = np.array(['N']*len(total_files))
ruptureStatus = np.array(['N']*len(total_files))
sacVolume = np.zeros(len(total_files))
for i in range(len(total_files)):
    filename = total_files[i].split('\\')[-1].split('_')[0]
    if filename in aneurisk_meta.case_id.values:
        aneurysmLocation[i] = aneurisk_meta.loc[aneurisk_meta.case_id==filename].aneurysmLocation.values[0]
        aneurysmType[i] = aneurisk_meta.loc[aneurisk_meta.case_id==filename].aneurysmType.values[0]
        ruptureStatus[i] = aneurisk_meta.loc[aneurisk_meta.case_id==filename].ruptureStatus.values[0]
        sacVolume[i] = aneurisk_meta.loc[aneurisk_meta.case_id==filename].sacVolume.values[0]

print (aneurysmLocation)
print (aneurysmType)
print (ruptureStatus)
print (sacVolume)

def compute_srvf_distance(q1, q2):
    """
    计算两个SRVF之间的距离。

    参数:
    - q1: numpy数组，第一个SRVF表示。
    - q2: numpy数组，第二个SRVF表示。

    返回:
    - distance: 两个SRVF之间的距离。
    """
    # 计算差值
    diff = q1 - q2
    
    # 计算L^2范数
    distance = np.sqrt(np.sum(diff**2))
    
    return distance

# 初始化距离矩阵
distance_matrix = np.zeros((len(min_reparam), len(min_reparam)))
# 计算距离矩阵
for i in range(len(min_reparam)):
    for j in range(i+1, len(min_reparam)):  # 避免重复计算
        dist = compute_srvf_distance(min_reparam[i], min_reparam[j])
        distance_matrix[i, j] = dist
        distance_matrix[j, i] = dist  # 距离矩阵是对称的

# from scipy.cluster.hierarchy import dendrogram, linkage
# from matplotlib import pyplot as plt

# # 使用层次聚类算法
# linked = linkage(distance_matrix, 'single')

# plt.figure(figsize=(10, 7))
# dendrogram(linked,
#             orientation='top',
#             labels=range(1, distance_matrix.shape[0]+1),
#             distance_sort='descending',
#             show_leaf_counts=True)
# plt.show()


from sklearn.manifold import MDS

# 初始化MDS模型，设置降维到2维
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=6)

# 对距离矩阵应用MDS算法
results = mds.fit_transform(distance_matrix)

# 提取两个维度
x = results[:, 0]
y = results[:, 1]

# 绘制结果
plt.figure(figsize=(8, 6))
plt.scatter(x, y, c=colors, cmap='viridis')
plt.title('MDS结果')
plt.xlabel('MDS1')
plt.ylabel('MDS2')
for i, txt in enumerate(range(1, distance_matrix.shape[0]+1)):
    plt.annotate(ruptureStatus[i], (x[i], y[i]))
plt.savefig(root_dir+'MDS.png')
plt.close()


import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 假设 min_reparam 是形状为 (n, 100, 3) 的 numpy 数组
# 例如：min_reparam = np.random.rand(n_samples, 100, 3)

# 步骤1: 重塑数据
n_samples = min_reparam.shape[0]
data_reshaped = min_reparam.reshape(n_samples, -1)  # 变成 (n, 300)

# 步骤2: 标准化数据
scaler = StandardScaler()
data_standardized = scaler.fit_transform(data_reshaped)

# 步骤3: 应用PCA
pca = PCA(n_components=2)  # 例如，降至2维进行可视化
principal_components = pca.fit_transform(data_standardized)

# 步骤4: 分析和可视化结果
plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1], c=colors, cmap='viridis')
for i, txt in enumerate(range(1, distance_matrix.shape[0]+1)):
    plt.annotate(ruptureStatus[i], (principal_components[i, 0], principal_components[i, 1]))
plt.title('PCA结果')
plt.xlabel('主成分1')
plt.ylabel('主成分2')
plt.savefig(root_dir+'PCA.png')
plt.close()

# 可以通过pca.explained_variance_ratio_查看每个主成分解释的方差比例
print("主成分解释的方差比例:", pca.explained_variance_ratio_)


fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
for i in range(len(resampled_unit_curves)):
    c,t = compute_curvature_and_torsion(resampled_unit_curves[i][5:-5])
    max_c_idx = np.argmax(c)
    filename = total_files[i].split('/')[-1].split('.')[0]
    # plt.annotate(filename, (max_c_idx, c[max_c_idx]))
    ax1.plot(range(len(c)), c)
    ax2.plot(range(len(t)), t)
plt.savefig(root_dir+'curvature_torsion.png')
plt.close()

