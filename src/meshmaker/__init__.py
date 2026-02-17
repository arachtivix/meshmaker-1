"""
MeshMaker - A 3D mesh generation library based on cube grids.
"""

__version__ = "0.1.0"

from .cube_grid import CubeGrid
from .mesh_generator import MeshGenerator
from .cube_appearance import CubeAppearance
from .maze_generator import MazeGenerator

__all__ = ['CubeGrid', 'MeshGenerator', 'CubeAppearance', 'MazeGenerator']
