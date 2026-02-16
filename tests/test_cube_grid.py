"""
Unit tests for CubeGrid class.
"""
import pytest
import numpy as np
from meshmaker.cube_grid import CubeGrid
from meshmaker.cube_appearance import CubeAppearance


class TestCubeGrid:
    """Test suite for CubeGrid."""
    
    def test_grid_creation(self):
        """Test basic grid creation."""
        grid = CubeGrid((5, 5, 5))
        assert grid.dimensions == (5, 5, 5)
    
    def test_invalid_dimensions(self):
        """Test that invalid dimensions raise error."""
        with pytest.raises(ValueError, match="All dimensions must be positive"):
            CubeGrid((0, 5, 5))
        
        with pytest.raises(ValueError, match="All dimensions must be positive"):
            CubeGrid((5, -1, 5))
    
    def test_set_and_get_cube(self):
        """Test setting and getting cube occupancy."""
        grid = CubeGrid((3, 3, 3))
        
        # Initially all empty
        assert not grid.get_cube((0, 0, 0))
        
        # Set a cube
        grid.set_cube((1, 1, 1), occupied=True)
        assert grid.get_cube((1, 1, 1))
        
        # Unset a cube
        grid.set_cube((1, 1, 1), occupied=False)
        assert not grid.get_cube((1, 1, 1))
    
    def test_out_of_bounds(self):
        """Test that out of bounds positions raise error."""
        grid = CubeGrid((3, 3, 3))
        
        with pytest.raises(ValueError, match="outside grid bounds"):
            grid.set_cube((5, 0, 0))
        
        with pytest.raises(ValueError, match="outside grid bounds"):
            grid.get_cube((0, 0, 5))
    
    def test_cube_appearance(self):
        """Test setting and getting cube appearance."""
        grid = CubeGrid((3, 3, 3))
        red = CubeAppearance(color=(1.0, 0.0, 0.0))
        
        grid.set_cube((1, 1, 1), occupied=True, appearance=red)
        
        appearance = grid.get_appearance((1, 1, 1))
        assert appearance.color == (1.0, 0.0, 0.0)
    
    def test_default_appearance(self):
        """Test default appearance for cubes."""
        grid = CubeGrid((3, 3, 3))
        grid.set_cube((0, 0, 0), occupied=True)
        
        # Should return default appearance
        appearance = grid.get_appearance((0, 0, 0))
        assert appearance.color == (0.5, 0.5, 0.5)
        
        # Set custom default
        blue = CubeAppearance(color=(0.0, 0.0, 1.0))
        grid.set_default_appearance(blue)
        grid.set_cube((1, 1, 1), occupied=True)
        
        appearance = grid.get_appearance((1, 1, 1))
        assert appearance.color == (0.0, 0.0, 1.0)
    
    def test_get_occupied_positions(self):
        """Test getting all occupied positions."""
        grid = CubeGrid((3, 3, 3))
        
        grid.set_cube((0, 0, 0), occupied=True)
        grid.set_cube((1, 1, 1), occupied=True)
        grid.set_cube((2, 2, 2), occupied=True)
        
        positions = grid.get_occupied_positions()
        assert len(positions) == 3
        assert (0, 0, 0) in positions
        assert (1, 1, 1) in positions
        assert (2, 2, 2) in positions
    
    def test_clear(self):
        """Test clearing the grid."""
        grid = CubeGrid((3, 3, 3))
        
        grid.set_cube((0, 0, 0), occupied=True)
        grid.set_cube((1, 1, 1), occupied=True)
        
        grid.clear()
        
        assert len(grid.get_occupied_positions()) == 0
        assert not grid.get_cube((0, 0, 0))
        assert not grid.get_cube((1, 1, 1))
    
    def test_repr(self):
        """Test string representation."""
        grid = CubeGrid((5, 5, 5))
        grid.set_cube((0, 0, 0), occupied=True)
        grid.set_cube((1, 1, 1), occupied=True)
        
        repr_str = repr(grid)
        assert "CubeGrid" in repr_str
        assert "(5, 5, 5)" in repr_str
        assert "occupied=2" in repr_str
