import numpy as np

# 假设 b1 和 b2 是形状为 (n,3) 的矩阵
# b1 = np.array([...])
# b2 = np.array([...])

# 计算 L2 距离
def calculate_l2_distance(b1, b2):
    return np.sqrt(((b1 - b2) ** 2).sum())

# 示例计算
# 生成两个随机的 (n,3) 矩阵
# n = 100  # 曲线的长度
# b1 = np.random.rand(n, 3)
# b2 = np.random.rand(n, 3)

# # 计算 L2 距离
# l2_distance = calculate_l2_distance(b1, b2)
# print("The L2 distance between b1 and b2 is:", l2_distance)




