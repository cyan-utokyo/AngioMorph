import numpy as np
import matplotlib.pyplot as plt

def generate_diff_homeomorphism():
    def poly5(x, coeffs):
        # 5次多项式函数
        return coeffs[0]*x**5 + coeffs[1]*x**4 + coeffs[2]*x**3 + coeffs[3]*x**2 + coeffs[4]*x
    
    def poly5_derivative(x, coeffs):
        # 5次多项式的导数
        return 5*coeffs[0]*x**4 + 4*coeffs[1]*x**3 + 3*coeffs[2]*x**2 + 2*coeffs[3]*x + coeffs[4]
    
    # 确保生成的函数是单调递增的
    is_monotonic_increasing = False
    while not is_monotonic_increasing:
        # 随机选择系数a, b, c, d, e，使得它们的和为1，保证f(1) = 1
        coeffs = np.random.uniform(-1, 1, 5)
        coeffs /= coeffs.sum()
        
        # 检查导数在[0, 1]上是否始终大于0
        x_test = np.linspace(0, 1, 1000)
        derivative_test = poly5_derivative(x_test, coeffs)
        
        if np.all(derivative_test > 0):
            is_monotonic_increasing = True
    
    # 返回满足条件的多项式函数和它的系数
    return lambda x: poly5(x, coeffs), coeffs

# plt.figure(figsize=(8, 6))
# for i in range(100):
#     # 生成微分同胚并测试
#     diff_homeo, coeffs = generate_diff_homeomorphism()
#     # 绘图
#     x = np.linspace(0, 1, 1000)
#     y = diff_homeo(x)
#     plt.plot(x, y)
# plt.grid(True)
# plt.show()
