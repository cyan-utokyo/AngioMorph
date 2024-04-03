import pandas as pd
import re
# Given text data without spaces

f = open("aneuriskmeta.txt", "r")
data = f.read()
f.close()


# 将数据分割成行
lines = data.strip().split('\n')

# 初始化用于保存分割数据的列表
data_list = []

# 遍历每行，使用正则表达式提取信息
for line in lines:
    # 使用正则表达式匹配和分割数据
    match = re.match(r"(C\d{4})(P\d+)([A-Z]{3})([A-Z]{3})([RU])(\d+\.\d+)", line)
    if match:
        # 将匹配的数据添加到列表中
        data_list.append(match.groups())

# 将数据列表转换为DataFrame
columns = ['case_id', 'patient_id', 'aneurysmLocation', 'aneurysmType', 'ruptureStatus', 'sacVolume']
df = pd.DataFrame(data_list, columns=columns)

# 转换sacVolume列为浮点数
df['sacVolume'] = df['sacVolume'].astype(float)

# 显示DataFrame
print(df.head())

df.to_csv("aneuriskmeta.csv", index=False)