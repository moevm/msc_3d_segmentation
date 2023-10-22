import open3d as o3d
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["input"]

# Извлечение данных из коллекции
cursor = collection.find({}, {"x": 1, "y": 1, "z": 1})
points = [(doc["x"], doc["y"], doc["z"]) for doc in cursor]

# Создание объекта PointCloud из данных
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Сохранение в PLY файл
o3d.io.write_point_cloud("output/output_geometric_46656.ply", pcd)

print("PLY файл создан: output.ply")
