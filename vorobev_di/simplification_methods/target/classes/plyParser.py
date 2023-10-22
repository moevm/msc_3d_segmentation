import numpy as np
from pymongo import MongoClient
import plyfile

# Подключение к MongoDB (замените URL и порт на ваши настройки)
client = MongoClient("mongodb://localhost:27017")

# Выберите базу данных
db = client["mydatabase"]

# Создайте коллекцию
collection = db["input"]

file_path = 'input/model.ply'

# Считайте данные из PLY файла
data = plyfile.PlyData.read(file_path)['vertex']

# Преобразуйте данные в список словарей
original_points = np.vstack([data['x'], data['y'], data['z']]).T
points_list = [{"x": float(x), "y": float(y), "z": float(z)} for x, y, z in original_points]

# удаление старых данных
collection.drop()
# Вставка данных в коллекцию
result = collection.insert_many(points_list)
