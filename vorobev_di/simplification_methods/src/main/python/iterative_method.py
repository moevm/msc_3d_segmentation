import numpy as np
import plyfile
from scipy.spatial.qhull import Delaunay
import pymongo


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
    center_point = points[0]
    points = points[1:]
    a, b, c = calculate_tangent_plane(points, center_point)
    local_approximation = np.array([a, b, c]) * center_point

    local_surface = reconstruct_local_surface(points, center_point)

    discarded_points_set = set(map(tuple, discarded_points))

    for vertex in local_surface:
        vertex_tuple = tuple(vertex.tolist())
        if vertex_tuple not in discarded_points_set:
            discarded_points_set.add(vertex_tuple)

    discarded_points = list(discarded_points_set)

    points = sort_points_by_significance(points, local_approximation, discarded_points)

    return points[threshold:]


def simplify_point_cloud_from_ply(file_path_local, threshold_local):
    data = plyfile.PlyData.read(file_path_local)['vertex']
    original_points = np.vstack([data['x'], data['y'], data['z']]).T
    num_original_points = len(original_points)

    simplified_points = simplify_point_cloud(original_points, threshold_local)
    num_simplified_points_local = len(simplified_points)

    save_point_cloud_to_mongodb(implified_points)

    return num_original_points, num_simplified_points_local


def save_point_cloud_to_mongodb(points):
    client = pymongo.MongoClient("mongodb://localhost:27017")  # Замените на вашу строку подключения к MongoDB
    db = client["mydatabase"]
    collection = db["output"]

    point_documents = []
    for point in points:
        point_document = {
            'x': point[0],
            'y': point[1],
            'z': point[2]
        }
        point_documents.append(point_document)

    collection.drop()
    collection.insert_many(point_documents)


# Пример использования
file_path = 'input/model.ply'
output_file_path = 'output2.ply'

# Итоговое количество точек
threshold = 20000

# Упрощение облака точек
num_original_points, num_simplified_points = \
    simplify_point_cloud_from_ply(file_path, threshold, output_file_path)

print(f"Количество точек в исходном облаке точек: {num_original_points}")
print(f"Количество точек в упрощенном облаке точек: {num_simplified_points}")
