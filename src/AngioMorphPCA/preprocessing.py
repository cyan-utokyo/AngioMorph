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

def calculate_3d_curve_abscissas(curve):
    # 初始化长度列表，起始点的长度为0
    abscissas = [0]

    # 遍历曲线上的点，计算累积长度
    for i in range(1, len(curve)):
        # 计算当前点与前一个点之间的距离
        distance = np.linalg.norm(np.array(curve[i]) - np.array(curve[i-1]))
        # 将这个距离加到最后一个累积长度上，得到新的累积长度
        abscissas.append(abscissas[-1] + distance)
    return abscissas


def remove_high_freq_components(data, freq_threshold):
    """
    使用傅立叶变换去除高频成分。
    
    参数:
    - data: 一维数组，输入数据。
    - freq_threshold: float，频率阈值，用于确定哪些频率成分被视为高频并需要被去除。
    
    返回:
    - filtered_data: 一维数组，滤波后的数据。
    """
    # 执行傅立叶变换
    data_fft = np.fft.fft(data)
    # 获取频率
    freq = np.fft.fftfreq(len(data))
    
    # 根据频率阈值滤除高频成分
    data_fft[np.abs(freq) > freq_threshold] = 0
    
    # 执行逆傅立叶变换
    filtered_data = np.fft.ifft(data_fft)
    
    # 返回实部，去除由于计算引入的虚部（应该接近于零）
    return filtered_data.real
