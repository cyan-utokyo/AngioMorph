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