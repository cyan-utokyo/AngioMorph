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


def cut_curve(coords, cut_points):
    if cut_points >= len(coords):
        raise ValueError("cut_points exceeds the number of points in the curve.")
    return coords[:-cut_points]


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
    if len(sys.argv) != 5:
        print("Usage: python script.py inputfile.vtk cut_points num_interpolated outputfile.vtk")
        sys.exit(1)

    input_file = sys.argv[1]
    cut_points = int(sys.argv[2])
    num_interpolated = int(sys.argv[3])
    output_file = sys.argv[4]

    coords = read_vtk_curve(input_file)
    cut_coords = cut_curve(coords, cut_points)
    interpolated_coords = interpolate_curve(cut_coords, num_interpolated)
    write_vtk_curve(interpolated_coords, output_file)
