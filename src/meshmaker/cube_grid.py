"""
CubeGrid - Manages a 3D grid of cubes.
"""
import numpy as np
from typing import Optional, Tuple
from .cube_appearance import CubeAppearance


class CubeGrid:
    """
    Represents a 3D grid where each cell can be occupied or unoccupied.
    Each occupied cell can have custom appearance properties.
    """
    
    def __init__(self, dimensions: Tuple[int, int, int]):
        """
        Initialize a cube grid.
        
        Args:
            dimensions: Tuple of (x, y, z) dimensions for the grid
        """
        if not all(d > 0 for d in dimensions):
            raise ValueError("All dimensions must be positive")
            
        self.dimensions = dimensions
        self._grid = np.zeros(dimensions, dtype=bool)
        self._appearances = {}  # Map of (x,y,z) -> CubeAppearance
        self._default_appearance = CubeAppearance()
    
    def set_cube(
        self, 
        position: Tuple[int, int, int], 
        occupied: bool = True,
        appearance: Optional[CubeAppearance] = None
    ):
        """
        Set a cube at the given position.
        
        Args:
            position: (x, y, z) position in the grid
            occupied: Whether the cube is occupied
            appearance: Optional appearance for the cube
        """
        x, y, z = position
        if not self._is_valid_position(position):
            raise ValueError(f"Position {position} is outside grid bounds {self.dimensions}")
        
        self._grid[x, y, z] = occupied
        
        if occupied and appearance is not None:
            self._appearances[position] = appearance
        elif not occupied and position in self._appearances:
            del self._appearances[position]
    
    def get_cube(self, position: Tuple[int, int, int]) -> bool:
        """
        Check if a cube at the given position is occupied.
        
        Args:
            position: (x, y, z) position in the grid
            
        Returns:
            True if the cube is occupied, False otherwise
        """
        if not self._is_valid_position(position):
            raise ValueError(f"Position {position} is outside grid bounds {self.dimensions}")
        
        x, y, z = position
        return bool(self._grid[x, y, z])
    
    def get_appearance(self, position: Tuple[int, int, int]) -> CubeAppearance:
        """
        Get the appearance of a cube at the given position.
        
        Args:
            position: (x, y, z) position in the grid
            
        Returns:
            CubeAppearance object for the cube
        """
        return self._appearances.get(position, self._default_appearance)
    
    def set_default_appearance(self, appearance: CubeAppearance):
        """
        Set the default appearance for cubes without specific appearance.
        
        Args:
            appearance: Default CubeAppearance to use
        """
        self._default_appearance = appearance
    
    def get_occupied_positions(self):
        """
        Get all occupied positions in the grid.
        
        Returns:
            List of (x, y, z) tuples for occupied positions
        """
        return list(zip(*np.where(self._grid)))
    
    def clear(self):
        """Clear all cubes from the grid."""
        self._grid.fill(False)
        self._appearances.clear()
    
    def _is_valid_position(self, position: Tuple[int, int, int]) -> bool:
        """Check if a position is within grid bounds."""
        x, y, z = position
        return (0 <= x < self.dimensions[0] and 
                0 <= y < self.dimensions[1] and 
                0 <= z < self.dimensions[2])
    
    def __repr__(self):
        occupied_count = np.sum(self._grid)
        return f"CubeGrid(dimensions={self.dimensions}, occupied={occupied_count})"
