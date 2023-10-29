# Инструкция по использованию
Для начала нужно перейти в рабочую директорию
```
cd .\simplification_methods
```
## Установка зависимостией
```
pip install -r src/main/python/requirements.txt 
```
## Сборка и подготовка
Для сборки необходим Maven
```
mvn clean
mvn package
```
Далее надо запустить mongoDB. Легче всего использовать image с docker hub. Перед этим необходимо убедиться, что у вас есть Docker и он запущен.
```
docker pull mongo:latest
docker run --name my-mongodb-container -d -p 27017:27017 mongo   
```
## Запуск геометрического и итеративного метода
Для запуска нужно перейти в сгенерированную папку /target и оттуда запускать jar файл. Метод определяет какие флаги будут использоваться в качестве аргументов. Подробнее об этом ниже в соответствующих разделах.
##  Упрощения полигональных моделей с применением основных методов (basic_methods.py)
Данный скрипт находится на уровне папки simplification_methods
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
Для использования нужно использовать флаг '-g' с указанием количства разделов после него. Пример:
```
 java -jar .\simplification_methods-1.0.jar -g 36
```
Запуск
```
cd .\simplification_methods\target
java -jar .\simplification_methods-1.0.jar -g <количество разделов>
```
## Алгоритм итеративного упрощения (iterative_method.py)
Для использования нужно заменить значения переменных в файле simplification_methods\src\main\python\iterative_method.py на строке 133 на нужные входные значения
```
threshold = <num of points> - количество точек в итоговой модели
```
Для использования нужно использовать флаг '-i' с указанием количства разделов после него. Пример:
```
 java -jar .\simplification_methods-1.0.jar -i
```
Запуск
```
cd .\simplification_methods\target
java -jar .\simplification_methods-1.0.jar -i
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
