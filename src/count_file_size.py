import os
import csv
from collections import defaultdict

# 指定文件夹路径
base_dir = r'D:\!_Nagahama_src\20250523_all\20250523_all\04_ICA_MCA_ACA_surface'

# 所有目标后缀
suffixes = [
    'L_ICA_MCA.stl',
    'L_ICA_MCA_tube.stl',
    'L_ICA_tube.stl',
    'L_MCA_tube.stl',
    'R_ICA_MCA.stl',
    'R_ICA_MCA_tube.stl',
    'R_ICA_tube.stl',
    'R_MCA_tube.stl',
]

# 建立一个 dict 来收集编号对应的每个文件大小
file_sizes = defaultdict(lambda: {s: 0 for s in suffixes})

# 遍历文件夹中所有文件
for fname in os.listdir(base_dir):
    if not fname.endswith('.stl'):
        continue
    parts = fname.split('.nii_')
    if len(parts) != 2:
        continue
    nid = parts[0]
    suffix = parts[1]
    if suffix in suffixes:
        fpath = os.path.join(base_dir, fname)
        size = os.path.getsize(fpath)
        file_sizes[nid][suffix] = size

# 输出为CSV
csv_path = '../output_file_sizes.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['ID'] + suffixes
    writer.writerow(header)
    for nid in sorted(file_sizes.keys()):
        row = [nid] + [file_sizes[nid][s] for s in suffixes]
        writer.writerow(row)

print(f"Saved to {csv_path}")
