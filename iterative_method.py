import numpy as np
import plyfile
from scipy.spatial.qhull import Delaunay


def calculate_tangent_plane(points, center_point):
    # Преобразование массива точек в матрицу numpy
    points = np.array(points)

    # Вычисление отклонений координат точек от центральной точки
    deviations = points - center_point

    # Вычисление матрицы ковариации
    covariance_matrix = np.cov(deviations.T)

    # Вычисление собственных значений и собственных векторов матрицы ковариации
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    # Находим индекс максимального собственного значения
    max_eigenvalue_index = np.argmax(eigenvalues)

    # Получаем собственный вектор, соответствующий максимальному собственному значению
    tangent_vector = eigenvectors[:, max_eigenvalue_index]

    # Коэффициенты аппроксимирующей плоскости
    a, b, c = tangent_vector

    return a, b, c


def reconstruct_local_surface(points, center_point):
    # Добавление центральной точки в массив точек
    points = np.vstack([points, center_point])

    # Преобразование массива точек в numpy массив
    points = np.array(points)

    # Выполнение триангуляции Делоне
    triangulation = Delaunay(points)

    # Индексы вершин треугольников, содержащих центральную точку
    triangle_indices = triangulation.vertex_neighbor_vertices[1]

    # Получение вершин треугольников
    triangle_vertices = triangulation.points[triangle_indices]

    # Удаление центральной точки из массива точек
    points = points[:-1]

    return triangle_vertices






def calculate_point_significance(current_point, local_approximation, discarded_points):
    # Вычисление отклонения текущей точки от локальной аппроксимации
    deviation = np.linalg.norm(current_point - local_approximation)

    # Вычисление отклонения отброшенных точек от локальной аппроксимации
    discarded_deviations = np.linalg.norm(discarded_points - local_approximation, axis=1)

    # Вычисление суммарного отклонения отброшенных точек
    total_discarded_deviation = np.sum(discarded_deviations)

    # Мера значимости точки
    significance = deviation + total_discarded_deviation

    return significance


def sort_points_by_significance(points, local_approximation, discarded_points):
    # Сортировка точек по мере значимости
    sorted_points = sorted(points, key=lambda p: calculate_point_significance(p, local_approximation, discarded_points))

    return sorted_points


def simplify_point_cloud(points, threshold):
    discarded_points = []
    while len(points) > threshold:
        center_point = points[0]
        points = points[1:]
        a, b, c = calculate_tangent_plane(points, center_point)
        local_approximation = np.array([a, b, c]) * center_point

        local_surface = reconstruct_local_surface(points, center_point)

        for vertex in local_surface:
            if vertex.tolist() not in discarded_points:
                discarded_points.append(vertex.tolist())

        points = sort_points_by_significance(points, local_approximation, discarded_points)

    return points


def simplify_point_cloud_from_ply(file_path_local, threshold_local, output_file_path_local):
    data = plyfile.PlyData.read(file_path_local)['vertex']
    original_points = np.vstack([data['x'], data['y'], data['z']]).T
    num_original_points = len(original_points)

    simplified_points = simplify_point_cloud(original_points, threshold_local)
    num_simplified_points_local = len(simplified_points)

    save_point_cloud_to_ply(output_file_path_local, simplified_points)

    return num_original_points, num_simplified_points_local


def save_point_cloud_to_ply(file_path_local, points):
    vertex = np.zeros(len(points), dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    for i, point in enumerate(points):
        vertex['x'][i] = point[0]
        vertex['y'][i] = point[1]
        vertex['z'][i] = point[2]
    vertex_ply = plyfile.PlyElement.describe(vertex, 'vertex')

    plyfile.PlyData([vertex_ply]).write(file_path_local)


# Пример использования
file_path = 'input/odm_25dmesh.ply'
output_file_path = 'output2.ply'

# Итоговое количество точек
threshold = 2700

# Упрощение облака точек

num_original_points, num_simplified_points = \
    simplify_point_cloud_from_ply(file_path, threshold, output_file_path)

print(f"Количество точек в исходном облаке точек: {num_original_points}")
print(f"Количество точек в упрощенном облаке точек: {num_simplified_points}")
