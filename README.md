# Инструкция по использованию
## Установка зависимостией
```
pip install -r requirements.txt
```
##  Упрощения полигональных моделей с применением основных методов (basic_methods.py)
Для использования нужно заменить значения переменных на строках 83-86 на нужные входные значения
```
file_path = <path> - путь к упрощаемому объекту
grid_size = <size of grid> - размер накладываемой сетки
output_file_path = <path> - путь к итоговому объекту
point_range = (<min point value>, <max point value>) - диапазон точек упрощаемого объекта
```
Запуск
```
python basic_methods.py
```
Для расчета grid_size и point_range можно использовать скрипт util/point_range.py
### Расчет grid_size и point_range (util/point_range.py)
Для использования нужно заменить значения переменных на строках 36-37 на нужные входные значения
```
file_path = <path> - путь к упрощаемому объекту
target_num_points = <num of points> - количество точек в итоговой модели
```
Запуск
```
python point_range.py
```
## Метод геометрического упрощения 3D полигональных объектов (geometric_simplification_algorithm.py)
Для использования нужно заменить значения переменных на строках 216-220 на нужные входные значения
```
file_path = <path> - путь к упрощаемому объекту
output_file_path = <path> - путь к итоговому объекту
divisions = <num of divisions> - количество разделов, на которое будет поделено итоговое облако точек
```
Запуск
```
python geometric_simplification_algorithm.py
```
## Алгоритм итеративного упрощения (iterative_method.py)
Для использования нужно заменить значения переменных на строках 124-128 на нужные входные значения
```
file_path = <path> - путь к упрощаемому объекту
output_file_path = <path> - путь к итоговому объекту
threshold = <num of points> - количество точек в итоговой модели
```
Запуск
```
python iterative_method.py
```
# Алгоритмы упрощения облаков точек
## Пример упрощения с использованием алгоритма упрощения полигональных моделей с применением основных методов (basic_methods.py)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/original.jpg?raw=true)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/basic_methods.jpg?raw=true)
## Пример упрощения с использованием метода геометрического упрощения 3D полигональных объектов (geometric_simplification_algorithm.py)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/original.jpg?raw=true)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/geometric_simplification.jpg?raw=true)
## Пример упрощения с использованием алгоритма итеративного упрощения (iterative_method.py)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/original.jpg?raw=true)
![alt text](https://github.com/moevm/msc_3d_segmentation/blob/vorobev_denis_8310/images/iterative_method.jpg?raw=true)
