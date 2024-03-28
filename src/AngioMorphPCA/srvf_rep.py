import numpy as np 
from AngioMorphPCA.preprocessing import parameterize_curve

def compute_srvf_func(resampled_curve):
    """
    Compute the Square Root Velocity Function (SRVF) of a given curve and re-parameterize it.
    
    Parameters:
    - resampled_curve: A curve that has been resampled and scaled. 
                       It's expected to be a numpy array of shape (n_points, n_dimensions)
                       
    Returns:
    - SRVF_func: SRVF function.
    """
    
    # 计算导数
    derivatives = np.gradient(resampled_curve, axis=0, edge_order=2)
    # 计算单位长度曲线的导数的幅度
    magnitude = np.linalg.norm(derivatives, axis=1)
    # 计算 SRVF
    SRVF_velocity = derivatives / np.sqrt(magnitude[:, None] + np.finfo(float).eps)  # 避免除以零

    # 假设 parameterize_curve 和 generate_diff_homeomorphism 已经定义
    SRVF_func = parameterize_curve(SRVF_velocity)
    return SRVF_func


def reconstruct_curve_from_srvf(SRVF, initial_point):
    """
    通过给定的SRVF和初始点重构原始曲线。
    
    Parameters:
    - SRVF: Square Root Velocity Function，预期是一个numpy数组，形状为(n_points, n_dimensions)
    - initial_point: 原始曲线的起始点，预期是一个形状为(n_dimensions,)的numpy数组
    
    Returns:
    - reconstructed_curve: 重构的原始曲线，numpy数组，形状为(n_points, n_dimensions)
    """
    
    # 计算SRVF的模长
    magnitude = np.sqrt(np.sum(SRVF**2, axis=1))
    
    # 从SRVF恢复曲线的导数
    derivatives = SRVF * magnitude[:, None]
    
    # 通过积分（累积和）恢复原始曲线
    # np.cumsum在0轴上累加，因此对导数累加就是对速度积分
    # 加上初始点以确定曲线的起始位置
    reconstructed_curve = np.cumsum(derivatives, axis=0) + initial_point
    
    return reconstructed_curve
