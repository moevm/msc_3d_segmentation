from scipy import ndimage
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter, label
from scipy.spatial.distance import cdist
import trimesh

def get_voxel_model(filename):
    mesh_path = get_absolute_path(filename)
    mesh = trimesh.load(mesh_path, force='mesh')

    angel_voxel = mesh.voxelized(0.5)
    return angel_voxel.matrix 

def get_absolute_path(file_name):
    absolute_path = os.path.dirname(__file__)
    return os.path.join(absolute_path, "..", "mesh", file_name)

def euclidean_distance_map(a):
    map = ndimage.distance_transform_edt(a)
    return map

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

def print_voxels(voxels):
    # Create a figure and a 3D axes object
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the colormap and normalize the voxel values to the range [0,1]
    cmap = plt.cm.get_cmap('hot')
    norm = plt.Normalize(vmin=voxels.min(), vmax=voxels.max())

    # Plot the voxel model with color mapped to the voxel values
    colors = cmap(norm(voxels))

    # Plot the voxel model
    ax.voxels(voxels, facecolors=colors)

    # Set the axis limits and labels
    ax.set_xlim(0, voxels.shape[0])
    ax.set_ylim(0, voxels.shape[1])
    ax.set_zlim(0, voxels.shape[2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Create a colorbar for the colormap
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm)

    # Show the plot
    plt.show()

def add_padding(arr, n):
    new_arr = np.zeros((arr.shape[0]+n*2, arr.shape[1]+n*2, arr.shape[2]+n*2), dtype=arr.dtype)
    new_arr[n:-n, n:-n, n:-n] = arr

    print(new_arr)
    return new_arr



arr = get_voxel_model('sagrada-familia-complete.obj')

arr = np.rot90(arr, k=1, axes=(0, 1))

# arr = add_padding(arr, 2)

print_voxels(arr)

res_arr = []

for a in arr:
    map = euclidean_distance_map(a)
    clusters_before, clusters, mask = cluster_maxima(map)

    segments = region_growth(map, clusters)

    plt.imshow(segments, cmap = plt.cm.hot)
    plt.show()

    res_arr.append(segments)

res_arr = np.array(res_arr)
print_voxels(res_arr)

# f, axarr = plt.subplots(2, 2)
# axarr[0, 0].imshow(arr, cmap = plt.cm.hot)
# axarr[0, 1].imshow(map, cmap = plt.cm.hot)
# axarr[1, 0].imshow(clusters_before, cmap = plt.cm.hot)
# axarr[1, 1].imshow(segments, cmap = plt.cm.hot)
# plt.show()
