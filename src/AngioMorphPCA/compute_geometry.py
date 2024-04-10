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
# from procrustes import rotational
from tqdm import tqdm

def compute_curvature_and_torsion(curve):

    # calculate first, second, and third derivatives using finite differences
    r_prime = np.diff(curve, axis=0)
    r_double_prime = np.diff(r_prime, axis=0)
    r_triple_prime = np.diff(r_double_prime, axis=0)
    
    # Pad derivatives to align array sizes
    r_prime = np.vstack((r_prime, np.zeros((1, 3))))
    r_double_prime = np.vstack((np.zeros((1, 3)), r_double_prime, np.zeros((1, 3))))
    r_triple_prime = np.vstack((np.zeros((2, 3)), r_triple_prime, np.zeros((2, 3))))

    # Ensure that r_prime, r_double_prime, and r_triple_prime have the same shape
    min_length = min(len(r_prime), len(r_double_prime), len(r_triple_prime))
    r_prime = r_prime[:min_length]
    r_double_prime = r_double_prime[:min_length]
    r_triple_prime = r_triple_prime[:min_length]

    cross_product = np.cross(r_prime, r_double_prime)
    cross_norm = np.linalg.norm(cross_product, axis=1)
    r_prime_norm = np.linalg.norm(r_prime, axis=1)

    epsilon = 1e-7
    curvature = np.where(r_prime_norm**3 > epsilon, cross_norm / (r_prime_norm ** 3), 0)

    torsion_numerator = np.einsum('ij,ij->i', r_prime, np.cross(r_double_prime, r_triple_prime))
    torsion = np.where(cross_norm**2 > epsilon, torsion_numerator / (cross_norm ** 2), 0)

    # Apply non-linear transformation
    curvature = np.tanh(curvature)
    torsion = np.tanh(torsion)


    # Create the interpolator functions for curvature and torsion
    # We are using 'linear' interpolation and 'extrapolate' to allow extension beyond the original range
    interp_curvature = interp1d(np.arange(len(curvature)), curvature, kind='linear', fill_value="extrapolate")
    interp_torsion = interp1d(np.arange(len(torsion)), torsion, kind='linear', fill_value="extrapolate")

    # Use the interpolator functions to extend the arrays to the original curve length
    interpolated_curvature = interp_curvature(np.arange(len(curve)))
    interpolated_torsion = interp_torsion(np.arange(len(curve)))

    return interpolated_curvature, interpolated_torsion

def build_curve_from_curvatures(curvatures, step_length=0.1):
    # 初始化起点和初始方向角
    x, y, theta = 0.0, 0.0, 0.0
    xs, ys = [x], [y]  # 存储曲线上的点

    for k in curvatures:
        # 计算这一段的终点坐标
        delta_theta = k * step_length
        theta += delta_theta
        x += step_length * np.cos(theta)
        y += step_length * np.sin(theta)
        
        # 保存这一段的终点坐标
        xs.append(x)
        ys.append(y)

    return xs, ys
