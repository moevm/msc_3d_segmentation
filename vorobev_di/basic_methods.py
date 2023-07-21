import numpy as np
import plyfile


def simplify_point_cloud_from_ply(file_path, grid_size, output_file_path, point_range):
    data = plyfile.PlyData.read(file_path)['vertex']
    original_points = np.vstack([data['x'], data['y'], data['z']]).T
    num_original_points = len(original_points)

    simplified_points = simplify_point_cloud(original_points, grid_size, point_range)
    num_simplified_points_local = len(simplified_points)

    save_point_cloud_to_ply(output_file_path, simplified_points)

    return num_original_points, num_simplified_points_local


def save_point_cloud_to_ply(file_path, points):
    vertex = np.zeros(len(points), dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    vertex['x'] = points[:, 0]
    vertex['y'] = points[:, 1]
    vertex['z'] = points[:, 2]
    vertex_ply = plyfile.PlyElement.describe(vertex, 'vertex')

    plyfile.PlyData([vertex_ply]).write(file_path)


def simplify_point_cloud(points, grid_size_local, point_range):
    grid = create_grid(grid_size_local, point_range)
    merged_points = merge_vertices(points, grid)  # Добавлен вызов merge_vertices
    simplified_points = []

    for point in merged_points:  # Используем merged_points вместо points
        nearest_point = find_nearest_point(point, grid)
        simplified_points.append(nearest_point)

    simplified_points = np.unique(simplified_points, axis=0)  # Удаление дубликатов точек

    return simplified_points


def create_grid(grid_size_local, point_range_local):
    x = np.arange(point_range_local[0], point_range_local[1], grid_size_local)
    y = np.arange(point_range_local[0], point_range_local[1], grid_size_local)
    z = np.arange(point_range_local[0], point_range_local[1], grid_size_local)
    grid = np.array(np.meshgrid(x, y, z)).T.reshape(-1, 3)

    return grid


def find_nearest_point(point, grid):
    distances = np.linalg.norm(grid - point, axis=1)
    nearest_index = np.argmin(distances)
    nearest_point = grid[nearest_index]

    return nearest_point


def merge_vertices(points, grid):
    merged_points = []

    for point in points:
        nearest_point = find_nearest_point(tuple(point), grid)
        merged_points.append(nearest_point)

    return merged_points


def remove_small_polygons(points):
    # Удаляем полигоны с менее чем тремя вершинами
    polygons = np.array(points).reshape(-1, 3)
    polygon_sizes = np.shape(polygons)[0]

    valid_polygons = []
    for i in range(polygon_sizes):
        if len(polygons[i]) >= 3:
            valid_polygons.append(polygons[i])

    return np.array(valid_polygons)


# Пример использования
file_path = 'input/odm_25dmesh.ply'
grid_size = 0.11636497040789147
output_file_path = 'output.ply'
point_range = (-6.294316, 2.3773432)

num_original_points, num_simplified_points = \
    simplify_point_cloud_from_ply(file_path, grid_size, output_file_path, point_range)

print(f"Количество точек в исходном облаке точек: {num_original_points}")
print(f"Количество точек в упрощенном облаке точек: {num_simplified_points}")
