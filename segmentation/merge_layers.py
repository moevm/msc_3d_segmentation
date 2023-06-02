from scipy import ndimage
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter, label
from scipy.spatial.distance import cdist
import trimesh
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from scipy.interpolate import interp1d

heatmap = 'nipy_spectral'

# file = 'sagrada-familia-la-passio.STL'
# file = 'torres-sagrada-familia.STL'
# file = 'sagrada-familia-nave-sacristias.STL'
# file = 'sagrada-familia-la-gloria.STL'

file = 'sagrada-familia-complete.obj'
# file = 'taj-mahal.stl'
# file = 'st-basils.stl'
# file = 'notre-dame.stl'


def get_voxel_model(filename):
    print("get model")
    mesh_path = get_absolute_path(filename)
    mesh = trimesh.load(mesh_path, force='mesh')

    print("got model")
    angel_voxel = mesh.voxelized(0.5)
    print("voxelized model")
    
    return angel_voxel 


def make_voxel_model_from_array(arr):
    mesh = trimesh.voxel.VoxelGrid(arr)
    return mesh


def show_model(voxel_grid, arr):
    cmap = plt.cm.get_cmap(heatmap)
    norm = plt.Normalize(vmin=arr.min(), vmax=arr.max())

    colors = cmap(norm(arr))

    mesh = voxel_grid.as_boxes(colors=colors)


    mesh_path = get_absolute_path(file)
    init_mesh = trimesh.load(mesh_path, force='mesh')
    
    # Interpolate vertex_colors
    vertex_input_array = mesh.visual.vertex_colors

    # Define the desired output array shape (135740, 4)
    vertex_output_shape = init_mesh.visual.vertex_colors.shape

    # Create a new array with the desired number of rows and the same number of columns
    vertex_output_array = np.zeros(vertex_output_shape)

    for i in range(4):
        # Create a 1D interpolating function for the current column
        f = interp1d(np.arange(vertex_input_array.shape[0]), vertex_input_array[:, i], kind='nearest')
        # Evaluate the interpolating function at the indices of the output array
        vertex_output_array[:, i] = f(np.linspace(0, vertex_input_array.shape[0] - 1, vertex_output_shape[0]))
    
    init_mesh.visual.vertex_colors = vertex_output_array

    print('vertex_colors.shape ', mesh.visual.vertex_colors.shape, init_mesh.visual.vertex_colors.shape, vertex_output_array.shape)

    sv = trimesh.Scene()
    sv.add_geometry(mesh)
    sv.show(resolution=(800, 600), flags={'axis': True})

    s = trimesh.Scene()
    s.add_geometry(init_mesh)
    s.show(resolution=(800, 600), flags={'axis': True})


def get_absolute_path(file_name):
    absolute_path = os.path.dirname(__file__)
    return os.path.join(absolute_path, "..", "mesh", file_name)


def euclidean_distance_map(a):
    map = ndimage.distance_transform_edt(a)
    return map


def cluster_maxima(map):
    maxima = maximum_filter(map, size=4, mode='constant')

    mask = (maxima == map)

    labeled_maxima_before, _ = label(mask)
    
    #костыль чтобы убрать внешнюю поверхность
    labeled_maxima = np.zeros_like(labeled_maxima_before)
    for i in range(labeled_maxima_before.shape[0]):
        for j in range(labeled_maxima_before.shape[1]):    
            if labeled_maxima_before[i][j] > 0 and labeled_maxima_before[i][j] < 2:
                labeled_maxima[i][j] = 0
            else:
                labeled_maxima[i][j] = labeled_maxima_before[i][j]

    # compute the coordinates of the maxima
    coordinates = np.argwhere(labeled_maxima > 0)
    threshold = 5

    # check the distances between each pair of maxima and merge clusters if their distance is below the threshold
    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            distance = cdist([coordinates[i]], [coordinates[j]])
            # print(distance)
            if distance <= threshold:
                # merge clusters by relabeling
                labeled_maxima[coordinates[j][0]][coordinates[j][1]] = labeled_maxima[coordinates[i][0]][coordinates[i][1]]

    return labeled_maxima, mask


def merge_segments(arr_3d):
    # Get the shape of the 3D array
    depth, height, width = arr_3d.shape

    # Initialize the merged array with zeros
    merged_array = np.zeros((height * depth, width), dtype=arr_3d.dtype)

    # Merge the 2D arrays together
    for d in range(depth):
        merged_array[d * height : (d + 1) * height, :] = arr_3d[d, :, :]

    return merged_array

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
    cmap = plt.cm.get_cmap(heatmap)
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
    # plt.show(block = False)
    plt.show()

def add_padding(arr, n):
    new_arr = np.zeros((arr.shape[0]+n*2, arr.shape[1]+n*2, arr.shape[2]+n*2), dtype=arr.dtype)
    new_arr[n:-n, n:-n, n:-n] = arr

    print(new_arr)
    return new_arr

def print_layer(before, after):
    f, axarr = plt.subplots(2)
    axarr[0].imshow(before, cmap = 'hot')
    axarr[1].imshow(after, cmap = heatmap)
    plt.show()



model = get_voxel_model(file)

arr = model.matrix

# arr = np.rot90(arr, k=1, axes=(0, 1))
# print_voxels(arr)

res_arr = []

for a in arr:
    map = euclidean_distance_map(a)
    clusters, mask = cluster_maxima(map)

    print_layer(map, clusters)

    segments = region_growth(map, clusters)

    res_arr.append(segments)

res_arr = np.array(res_arr)
# res_arr = np.rot90(res_arr, k=-1, axes=(1, 2))


# print("до мержа:", res_arr.shape)
# res_arr = merge_segments(res_arr)
# print("после мержа:", res_arr.shape)

# print_voxels(res_arr)


res_model = make_voxel_model_from_array(arr)
# print(model.scale, res_model.scale)

# mesh_path = get_absolute_path('sagrada-familia-complete.obj')
# init_mesh = trimesh.load(mesh_path, force='mesh')
# print(model.shape, arr.shape, res_arr.shape, res_model, init_mesh)

# show_model(res_model, res_arr)
