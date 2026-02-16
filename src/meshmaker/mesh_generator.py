"""
MeshGenerator - Generates 3D mesh data from a cube grid.
"""
import numpy as np
from typing import List, Tuple, Dict
from .cube_grid import CubeGrid


class MeshGenerator:
    """
    Generates 3D mesh data from a CubeGrid.
    Produces vertices, faces, and color information for rendering.
    """
    
    def __init__(self, cube_size: float = 1.0):
        """
        Initialize mesh generator.
        
        Args:
            cube_size: Size of each cube in the mesh
        """
        if cube_size <= 0:
            raise ValueError("Cube size must be positive")
        self.cube_size = cube_size
    
    def generate_mesh(self, grid: CubeGrid) -> Dict:
        """
        Generate a mesh from a cube grid.
        
        Args:
            grid: CubeGrid to generate mesh from
            
        Returns:
            Dictionary containing:
                - 'vertices': numpy array of vertex positions (N, 3)
                - 'faces': numpy array of face indices (M, 3)
                - 'colors': numpy array of vertex colors (N, 4) RGBA
        """
        vertices = []
        faces = []
        colors = []
        
        vertex_offset = 0
        
        for position in grid.get_occupied_positions():
            cube_vertices, cube_faces = self._generate_cube_geometry(position)
            appearance = grid.get_appearance(position)
            
            # Add vertices
            vertices.extend(cube_vertices)
            
            # Add faces with vertex offset
            for face in cube_faces:
                faces.append([f + vertex_offset for f in face])
            
            # Add colors for each vertex
            color_rgba = (*appearance.color, appearance.alpha)
            colors.extend([color_rgba] * len(cube_vertices))
            
            vertex_offset += len(cube_vertices)
        
        return {
            'vertices': np.array(vertices, dtype=np.float32),
            'faces': np.array(faces, dtype=np.int32),
            'colors': np.array(colors, dtype=np.float32)
        }
    
    def _generate_cube_geometry(self, position: Tuple[int, int, int]) -> Tuple[List, List]:
        """
        Generate vertices and faces for a single cube.
        
        Args:
            position: Grid position (x, y, z)
            
        Returns:
            Tuple of (vertices, faces) where vertices is a list of 3D points
            and faces is a list of triangular face indices
        """
        x, y, z = position
        s = self.cube_size
        
        # Calculate cube corner positions
        x0, y0, z0 = x * s, y * s, z * s
        x1, y1, z1 = x0 + s, y0 + s, z0 + s
        
        # 8 vertices of the cube
        vertices = [
            [x0, y0, z0],  # 0: back-bottom-left
            [x1, y0, z0],  # 1: back-bottom-right
            [x1, y1, z0],  # 2: back-top-right
            [x0, y1, z0],  # 3: back-top-left
            [x0, y0, z1],  # 4: front-bottom-left
            [x1, y0, z1],  # 5: front-bottom-right
            [x1, y1, z1],  # 6: front-top-right
            [x0, y1, z1],  # 7: front-top-left
        ]
        
        # 12 triangular faces (2 per cube face)
        faces = [
            # Back face (z=z0)
            [0, 1, 2], [0, 2, 3],
            # Front face (z=z1)
            [4, 6, 5], [4, 7, 6],
            # Left face (x=x0)
            [0, 3, 7], [0, 7, 4],
            # Right face (x=x1)
            [1, 5, 6], [1, 6, 2],
            # Bottom face (y=y0)
            [0, 4, 5], [0, 5, 1],
            # Top face (y=y1)
            [3, 2, 6], [3, 6, 7],
        ]
        
        return vertices, faces
    
    def export_obj(self, mesh_data: Dict, filename: str):
        """
        Export mesh to Wavefront OBJ format.
        
        Args:
            mesh_data: Mesh data dictionary from generate_mesh()
            filename: Output filename
        """
        vertices = mesh_data['vertices']
        faces = mesh_data['faces']
        colors = mesh_data['colors']
        
        with open(filename, 'w') as f:
            # Write vertices with colors as comments
            for i, (v, c) in enumerate(zip(vertices, colors)):
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f} "
                       f"# color: {c[0]:.3f} {c[1]:.3f} {c[2]:.3f} {c[3]:.3f}\n")
            
            # Write faces (OBJ uses 1-based indexing)
            for face in faces:
                f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
