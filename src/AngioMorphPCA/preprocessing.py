import numpy as np 
import glob 
import vtk
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def parameterize_curve(Curve):
    """
    Create a function to parameterize a 3D curve.

    :param Curve: A numpy array of shape (64, 3) representing the curve's discrete points.
    :return: A function that takes a vector of parameter values (t) and returns interpolated points on the curve.
    """
    # 假设 Curve 是一个 (64, 3) 的数组
    # Curve = np.random.rand(64, 3)  # 用随机数代替实际数据进行示例

    # 使用函数
    # curve_func = parameterize_curve(Curve)
    # t_vector = np.array([0.0, 0.5, 1.0])  # 示例参数t
    # points_on_curve = curve_func(t_vector)  # 这将给出t = 0.0, 0.5, 1.0时曲线上的点

    # `points_on_curve` 将包含根据提供的t值在曲线上插值得到的点。

    # 创建参数t的值，均匀分布在0到1之间
    t_values = np.linspace(0, 1, Curve.shape[0])

    # 创建三个独立的插值函数，分别对应x, y, z坐标
    interpolate_x = interp1d(t_values, Curve[:, 0], kind='cubic')
    interpolate_y = interp1d(t_values, Curve[:, 1], kind='cubic')
    interpolate_z = interp1d(t_values, Curve[:, 2], kind='cubic')

    def curve_function(t_vector):
        # Clamp the values in t_vector to be within [0, 1]
        t_vector_clamped = np.clip(t_vector, 0, 1)
        
        x = interpolate_x(t_vector_clamped)
        y = interpolate_y(t_vector_clamped)
        z = interpolate_z(t_vector_clamped)
        return np.array([x, y, z]).T  # Combine x, y, z coordinates


    return curve_function    