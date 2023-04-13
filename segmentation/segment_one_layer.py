from scipy import ndimage
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter, label
from PIL import Image, ImageOps
from numpy import asarray
from scipy.spatial.distance import cdist


def get_absolute_path(file_name):
    absolute_path = os.path.dirname(__file__)
    return os.path.join(absolute_path, "..", "mesh", file_name)
    

def open_image_as_bool_array(path):
    img = Image.open(path)

    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)

    a = asarray(img)
    return a.astype('bool')


def euclidean_distance_map(a):
    a = ndimage.distance_transform_edt(a)
    return a

def cluster_maxima(map):
    maxima = maximum_filter(map, size=4, mode='constant')

    mask = (maxima == map)

    labeled_maxima_before, num_labels = label(mask)

    
    #костыль чтобы убрать внешнюю поверхность
    labeled_maxima = np.zeros_like(labeled_maxima_before)
    for i in range(labeled_maxima_before.shape[0]):
        for j in range(labeled_maxima_before.shape[1]):    
            if labeled_maxima_before[i][j] > 0 and labeled_maxima_before[i][j] < 2:
                labeled_maxima[i][j] = 0
            else:
                labeled_maxima[i][j] = labeled_maxima_before[i][j]

    return labeled_maxima_before, labeled_maxima, mask


def show(a):
    plt.imshow(a, cmap = plt.cm.viridis)
    plt.show()

def region_growth(bool_array, labeled_maxima):
    maxima_coords = np.argwhere(labeled_maxima > 0)

    # get the coordinates of the elements in the boolean array
    element_coords = np.argwhere(bool_array)

    # compute the distance between each element and each maximum using the cdist function from scipy.spatial.distance
    distances = cdist(element_coords, maxima_coords)

    # find the index of the nearest maximum for each element
    nearest_maxima_indices = np.argmin(distances, axis=1)

    # create a new array where each element is assigned to the nearest maximum
    assigned_maxima = np.zeros_like(bool_array, dtype=np.int32)
    for i in range(len(element_coords)):
        coord = element_coords[i]
        nearest_maxima_index = nearest_maxima_indices[i]
        nearest_maxima_coord = maxima_coords[nearest_maxima_index]
        assigned_maxima[coord[0], coord[1]] = labeled_maxima[nearest_maxima_coord[0], nearest_maxima_coord[1]]

    return assigned_maxima





path = get_absolute_path('building100x100.png')
arr = open_image_as_bool_array(path)
map = euclidean_distance_map(arr)
clusters_before, clusters, mask = cluster_maxima(map)

segments = region_growth(map, clusters)


f, axarr = plt.subplots(2, 2)
axarr[0, 0].imshow(arr, cmap = plt.cm.hot)
axarr[0, 1].imshow(map, cmap = plt.cm.hot)
axarr[1, 0].imshow(clusters_before, cmap = plt.cm.hot)
axarr[1, 1].imshow(segments, cmap = plt.cm.hot)
plt.show()
