import trimesh
import numpy as np
import os

# Load the rooster mesh. Trimesh directly detects that the mesh is textured and contains a material
absolute_path = os.path.dirname(__file__)
mesh_path = os.path.join(absolute_path, "..", "mesh", 'factory.ply')
mesh = trimesh.load(mesh_path, force='mesh')

# Voxelize the loaded mesh with a voxel size of 0.01. We also call hollow() to remove the inside voxels, which will help with color calculation
angel_voxel = mesh.voxelized(0.005)

# Extract the mesh vertices
mesh_verts = mesh.vertices

# We use the ProximityQuery built-in function to get the closest voxel point centers to each vertex of the mesh
_,vert_idx = trimesh.proximity.ProximityQuery(mesh).vertex(angel_voxel.points)

# We loop through all the calculated closest voxel points
for idx, vert in enumerate(vert_idx):
    # Get the voxel grid index of each closets voxel center point
    vox_verts = angel_voxel.points_to_indices(mesh_verts[vert])
    # Get the color vertex color

# generate a voxelized mesh from the voxel grid representation, using the calculated colors 
voxelized_mesh = angel_voxel.as_boxes()

# Initialize a scene
s = trimesh.Scene()
# Add the voxelized mesh to the scene. If want to also show the intial mesh uncomment the second line and change the alpha channel of in the loop to something <100
s.add_geometry(voxelized_mesh)
# s.add_geometry(mesh)
s.show()
