import numpy as np
import plyfile


def create_bounding_box(points):
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    min_z = float('inf')
    max_z = float('-inf')

    for point in points:
        x, y, z = point
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        if z < min_z:
            min_z = z
        if z > max_z:
            max_z = z

    # Формируем параллелепипед
    bounding_box = [
        (min_x, min_y, min_z),
        (max_x, min_y, min_z),
        (min_x, max_y, min_z),
        (max_x, max_y, min_z),
        (min_x, min_y, max_z),
        (max_x, min_y, max_z),
        (min_x, max_y, max_z),
        (max_x, max_y, max_z)
    ]

    return bounding_box


def find_forming_points(vertices):
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    min_z = float('inf')
    max_z = float('-inf')

    for vertex in vertices:
        x, y, z = vertex  # Предполагается, что вершина представлена в виде кортежа (x, y, z)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        if z < min_z:
            min_z = z
        if z > max_z:
            max_z = z

    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def calculate_division_bounds(bounding_box, divisions_local):
    min_x, min_y, min_z = bounding_box[0]
    max_x, max_y, max_z = bounding_box[7]

    x_range = max_x - min_x
    y_range = max_y - min_y
    z_range = max_z - min_z

    division_size_x = x_range / divisions_local
    division_size_y = y_range / divisions_local
    division_size_z = z_range / divisions_local

    division_bounds = []

    for i in range(divisions_local):
        division_min_x = min_x + i * division_size_x
        division_max_x = min_x + (i + 1) * division_size_x

        for j in range(divisions_local):
            division_min_y = min_y + j * division_size_y
            division_max_y = min_y + (j + 1) * division_size_y

            for k in range(divisions_local):
                division_min_z = min_z + k * division_size_z
                division_max_z = min_z + (k + 1) * division_size_z

                division_bounds.append([(division_min_x, division_min_y, division_min_z),
                                        (division_max_x, division_max_y, division_max_z)])

    return division_bounds


def assign_vertices_to_divisions(vertices, division_bounds):
    vertex_divisions = [[] for _ in range(len(division_bounds))]

    for vertex in vertices:
        for i, bounds in enumerate(division_bounds):
            min_bound, max_bound = bounds
            x, y, z = vertex

            if min_bound[0] <= x <= max_bound[0] and min_bound[1] <= y <= max_bound[1] and min_bound[2] <= z <= \
                    max_bound[2]:
                vertex_divisions[i].append(vertex)
                break

    return vertex_divisions


def calculate_distances_to_center(vertex_divisions):
    point_distances = []

    for division in vertex_divisions:
        if len(division) == 0:
            continue
        center = calculate_center(division)
        division_point_distances = []

        for vertex in division:
            distance = calculate_distance_squared(vertex, center)
            division_point_distances.append((vertex, distance))

        point_distances.append(division_point_distances)

    return point_distances


def calculate_center(vertices):
    center = [0, 0, 0]

    for vertex in vertices:
        for i in range(3):
            center[i] += vertex[i]

    num_vertices = len(vertices)
    center = [coord / num_vertices for coord in center]

    return center


def calculate_distance_squared(vertex1, vertex2):
    distance_squared = sum([(coord1 - coord2) ** 2 for coord1, coord2 in zip(vertex1, vertex2)])
    return distance_squared


def get_min_max_distances(distances):
    min_distances = []
    max_distances = []

    for division_distances in distances:
        division_points, division_distances = zip(*division_distances)
        min_distance = min(division_distances)
        max_distance = max(division_distances)
        min_point = division_points[division_distances.index(min_distance)]
        max_point = division_points[division_distances.index(max_distance)]
        min_distances.append(min_point)
        max_distances.append(max_point)

    return min_distances, max_distances


def simplify_point_cloud(vertices, divisions_local):
    # Создание ограничивающего объема
    bounding_box = create_bounding_box(vertices)

    # Разделение ограничивающего объема на подразделения
    division_bounds = calculate_division_bounds(bounding_box, divisions_local)

    # Назначение вершин подразделениям
    vertex_divisions = assign_vertices_to_divisions(vertices, division_bounds)

    # Расчет расстояний от вершин до центров подразделений
    points_per_distances = calculate_distances_to_center(vertex_divisions)

    # Получение минимальных и максимальных расстояний
    min_distances, max_distances = get_min_max_distances(points_per_distances)

    anchor_vertices_local = min_distances + max_distances

    return anchor_vertices_local


def save_point_cloud_to_ply(file_path, points):
    vertex = np.zeros(len(points), dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    for i, point in enumerate(points):
        vertex['x'][i] = point[0]
        vertex['y'][i] = point[1]
        vertex['z'][i] = point[2]
    vertex_ply = plyfile.PlyElement.describe(vertex, 'vertex')

    plyfile.PlyData([vertex_ply]).write(file_path)


def simplify_point_cloud_from_ply(file_path_local, divisions_local, output_file_path_local):
    data = plyfile.PlyData.read(file_path_local)['vertex']
    original_points = np.vstack([data['x'], data['y'], data['z']]).T
    num_original_points = len(original_points)

    simplified_points = simplify_point_cloud(original_points, divisions_local)
    num_simplified_points_local = len(simplified_points)

    save_point_cloud_to_ply(output_file_path_local, simplified_points)

    return num_original_points, num_simplified_points_local


# Пример использования

file_path = 'input/odm_25dmesh.ply'
output_file_path = 'output1.ply'

# Число подразделений
divisions = 24

# Упрощение облака точек

num_original_points, num_simplified_points = \
    simplify_point_cloud_from_ply(file_path, divisions, output_file_path)

print(f"Количество точек в исходном облаке точек: {num_original_points}")
print(f"Количество точек в упрощенном облаке точек: {num_simplified_points}")
