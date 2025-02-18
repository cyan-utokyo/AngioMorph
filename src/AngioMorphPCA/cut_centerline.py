"""
本程序用于处理vtk格式的三维曲线数据。它能够截取曲线的某一段，并对该段进行插值，以生成等距采样的曲线点集。
适用于血管中心线、路径轨迹等需要曲线处理的场景。

This program processes 3D curve data in vtk format. It extracts a segment of the curve and interpolates it to generate
equidistantly sampled points. It is suitable for applications such as vascular centerlines or path trajectories.

功能概述 / Functionality:
1. 读取vtk曲线文件，提取点坐标数据。
2. 截取曲线第n个点到第m个点之间的曲线段。
3. 在截取的曲线段上进行弧长均匀插值，生成指定数量的等距点。
4. 将处理后的曲线段写入新的vtk文件，以ASCII POLYDATA格式保存。

使用方法 / Usage:
python script.py inputfile.vtk n m num_interpolated outputfile.vtk

参数说明 / Parameters:
- inputfile.vtk: 输入vtk曲线文件路径 / Input vtk curve file path
- n: 起始点索引（包含） / Start point index (inclusive)
- m: 结束点索引（包含） / End point index (inclusive)
- num_interpolated: 插值生成的点数 / Number of interpolated points
- outputfile.vtk: 输出vtk曲线文件路径 / Output vtk curve file path

示例 / Example:
python script.py vessel.vtk 10 50 100 output_segment.vtk

该示例将读取“vessel.vtk”，截取第10到第50个点的曲线段，并在该段上插值生成100个等距点，保存到“output_segment.vtk”。

注意 / Notes:
- n和m必须满足 0 <= n <= m < 曲线总点数 / n and m must satisfy 0 <= n <= m < total number of points
- 本程序假设vtk文件是ASCII格式，数据类型为POLYDATA曲线 / This program assumes that the vtk file is in ASCII format with POLYDATA curve type.
"""


import sys
import vtk
import numpy as np


def read_vtk_curve(file_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    points = polydata.GetPoints()
    coords = np.array([points.GetPoint(i) for i in range(points.GetNumberOfPoints())])
    return coords


def cut_curve(coords, n, m):
    if n < 0 or m >= len(coords) or n > m:
        raise ValueError("Invalid range: n and m must satisfy 0 <= n <= m < len(coords)")
    return coords[n:m + 1]


def interpolate_curve(coords, num_interpolated):
    distances = np.cumsum(np.linalg.norm(np.diff(coords, axis=0), axis=1))
    distances = np.insert(distances, 0, 0)

    interpolated_distances = np.linspace(0, distances[-1], num_interpolated)
    interpolated_coords = np.empty((num_interpolated, 3))

    for i in range(num_interpolated):
        d = interpolated_distances[i]
        idx = np.searchsorted(distances, d) - 1
        if idx == len(distances) - 1:
            interpolated_coords[i] = coords[-1]
        else:
            t = (d - distances[idx]) / (distances[idx + 1] - distances[idx])
            interpolated_coords[i] = (1 - t) * coords[idx] + t * coords[idx + 1]

    return interpolated_coords


def write_vtk_curve(coords, output_path):
    with open(output_path, 'w') as f:
        f.write("# vtk DataFile Version 2.0\n")
        f.write("Vessel Segment\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n")
        f.write(f"POINTS {len(coords)} float\n")

        for p in coords:
            f.write(f"{p[0]} {p[1]} {p[2]}\n")

        f.write(f"LINES 1 {len(coords) + 1}\n")
        f.write(f"{len(coords)} " + " ".join(str(i) for i in range(len(coords))) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py inputfile.vtk n m num_interpolated outputfile.vtk")
        sys.exit(1)

    input_file = sys.argv[1]
    n = int(sys.argv[2])
    m = int(sys.argv[3])
    num_interpolated = int(sys.argv[4])
    output_file = sys.argv[5]

    coords = read_vtk_curve(input_file)
    cut_coords = cut_curve(coords, n, m)
    interpolated_coords = interpolate_curve(cut_coords, num_interpolated)
    write_vtk_curve(interpolated_coords, output_file)
