import numpy as np
import plyfile


def determine_grid_size_and_range(file_path, target_num_points):
    # Загружаем облако точек из файла PLY
    data = plyfile.PlyData.read(file_path)['vertex']
    points = np.vstack([data['x'], data['y'], data['z']]).T

    num_original_points = len(points)

    print(f"Количество точек: {num_original_points}")

    # Определяем диапазон значений точек
    min_coords = np.min(points, axis=0)
    max_coords = np.max(points, axis=0)
    point_range = (min_coords, max_coords)

    # Вычисляем общее количество точек в облаке
    num_points = len(points)

    # Вычисляем примерный объем облака точек
    volume = max_coords - min_coords
    total_volume = np.prod(volume)

    # Вычисляем плотность точек
    point_density = num_points / total_volume

    # Вычисляем необходимый размер сетки
    grid_size = np.power(target_num_points / point_density, 1 / 3)

    return grid_size, point_range


# Пример использования
file_path = '../input/odm_25dmesh.ply'
target_num_points = 1799

grid_size, point_range = determine_grid_size_and_range(file_path, target_num_points)


min_point = np.array(point_range[0], dtype=np.float32)
max_point = np.array(point_range[1], dtype=np.float32)

point_range = (np.min(min_point), np.max(max_point))

print(f"Рекомендуемый размер сетки: {grid_size / 22.61}")
print(f"Диапазон значений точек (point_range): {point_range}")
