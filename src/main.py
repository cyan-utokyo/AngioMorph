import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from AngioMorphPCA.preprocessing import parameterize_curve
from AngioMorphPCA.io import Get_simple_vtk
from scipy.integrate import simps
from AngioMorphPCA.GenerateDiffHemeo import generate_diff_homeomorphism

brava_files = glob.glob('brava_ica_mirrored/*.vtk')
aneurisk_files = glob.glob('aneurisk_ica_mirrored/*.vtk')
total_files = brava_files + aneurisk_files

# 原始曲线是f，SRVF是q
# 应当首先对f进行缩放使其长度为1，注意这有数学定义。（论文P1922）
# 接下来求q
# 最后求q的轨道[q]

# for i in range(len(total_files)):
for i in range(15,16):
    print (total_files[i])
    temp = Get_simple_vtk(total_files[i])
    temp_func = parameterize_curve(temp)
    t_resampled = np.linspace(0, 1, 100)
    resampled_curve = temp_func(t_resampled)

    # 计算导数
    derivatives = np.gradient(resampled_curve, axis=0, edge_order=2)

    # 使用Simpson法则计算积分来得到曲线的长度，并缩放曲线
    magnitude = np.linalg.norm(derivatives, axis=1)
    integral = simps(magnitude, t_resampled)
    resampled_curve /= integral

    # 重新计算单位长度曲线的导数
    derivatives = np.gradient(resampled_curve, axis=0, edge_order=2)
    magnitude = np.linalg.norm(derivatives, axis=1)

    # 计算 SRVF
    SRVF_velocity = derivatives / np.sqrt(magnitude[:, None] + np.finfo(float).eps)  # 避免除以零
    print (SRVF_velocity.shape)
    SRVF_func = parameterize_curve(SRVF_velocity)
    # re-parameterize SRVF
    diff_homeo, coeffs = generate_diff_homeomorphism()
    x = np.linspace(0, 1, 300)
    y = diff_homeo(x)
    SRVF_reparameterized = SRVF_func(y)

    plt.plot(SRVF_velocity[:, 0], SRVF_velocity[:, 2], label="Original SRVF", marker='o')
    plt.plot(SRVF_reparameterized[:, 0], SRVF_reparameterized[:, 2], label="Reparameterized SRVF", marker='x')
    plt.title("SRVF reparameterization")
    plt.legend()
    plt.show()

