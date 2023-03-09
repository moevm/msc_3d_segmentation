import open3d as o3d
import os

absolute_path = os.path.dirname(__file__)
mesh_path = os.path.join(absolute_path, "..", "mesh", 'factory.ply')
mesh = o3d.io.read_triangle_mesh(mesh_path)

print('voxelization')
voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=0.01)
o3d.visualization.RenderOption.light_on = True
o3d.visualization.draw_geometries([voxel_grid])
