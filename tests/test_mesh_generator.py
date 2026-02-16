"""
Unit tests for MeshGenerator class.
"""
import pytest
import numpy as np
from meshmaker.mesh_generator import MeshGenerator
from meshmaker.cube_grid import CubeGrid
from meshmaker.cube_appearance import CubeAppearance


class TestMeshGenerator:
    """Test suite for MeshGenerator."""
    
    def test_generator_creation(self):
        """Test basic generator creation."""
        gen = MeshGenerator(cube_size=1.0)
        assert gen.cube_size == 1.0
    
    def test_invalid_cube_size(self):
        """Test that invalid cube size raises error."""
        with pytest.raises(ValueError, match="Cube size must be positive"):
            MeshGenerator(cube_size=0)
        
        with pytest.raises(ValueError, match="Cube size must be positive"):
            MeshGenerator(cube_size=-1.0)
    
    def test_empty_grid_mesh(self):
        """Test generating mesh from empty grid."""
        grid = CubeGrid((3, 3, 3))
        gen = MeshGenerator()
        
        mesh = gen.generate_mesh(grid)
        
        assert len(mesh['vertices']) == 0
        assert len(mesh['faces']) == 0
        assert len(mesh['colors']) == 0
    
    def test_single_cube_mesh(self):
        """Test generating mesh from single cube."""
        grid = CubeGrid((3, 3, 3))
        grid.set_cube((0, 0, 0), occupied=True)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # A cube has 8 vertices
        assert len(mesh['vertices']) == 8
        # A cube has 12 triangular faces
        assert len(mesh['faces']) == 12
        # Colors should match vertices
        assert len(mesh['colors']) == 8
        
        # Check data types
        assert mesh['vertices'].dtype == np.float32
        assert mesh['faces'].dtype == np.int32
        assert mesh['colors'].dtype == np.float32
    
    def test_multiple_cubes_mesh(self):
        """Test generating mesh from multiple cubes."""
        grid = CubeGrid((3, 3, 3))
        grid.set_cube((0, 0, 0), occupied=True)
        grid.set_cube((1, 0, 0), occupied=True)
        grid.set_cube((0, 1, 0), occupied=True)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # 3 cubes * 8 vertices each
        assert len(mesh['vertices']) == 24
        # 3 cubes * 12 faces each
        assert len(mesh['faces']) == 36
        # Colors should match vertices
        assert len(mesh['colors']) == 24
    
    def test_cube_with_custom_appearance(self):
        """Test that cube colors are applied correctly."""
        grid = CubeGrid((2, 2, 2))
        red = CubeAppearance(color=(1.0, 0.0, 0.0), alpha=0.8)
        grid.set_cube((0, 0, 0), occupied=True, appearance=red)
        
        gen = MeshGenerator()
        mesh = gen.generate_mesh(grid)
        
        # All vertices of this cube should have the red color
        for color in mesh['colors']:
            assert color[0] == 1.0  # Red channel
            assert color[1] == 0.0  # Green channel
            assert color[2] == 0.0  # Blue channel
            assert color[3] == 0.8  # Alpha channel
    
    def test_cube_size_scaling(self):
        """Test that cube size affects vertex positions."""
        grid = CubeGrid((2, 2, 2))
        grid.set_cube((0, 0, 0), occupied=True)
        
        gen1 = MeshGenerator(cube_size=1.0)
        mesh1 = gen1.generate_mesh(grid)
        
        gen2 = MeshGenerator(cube_size=2.0)
        mesh2 = gen2.generate_mesh(grid)
        
        # Vertices should be scaled by cube size
        assert not np.allclose(mesh1['vertices'], mesh2['vertices'])
        # But the number of vertices should be the same
        assert len(mesh1['vertices']) == len(mesh2['vertices'])
    
    def test_cube_geometry(self):
        """Test cube vertex positions."""
        grid = CubeGrid((2, 2, 2))
        grid.set_cube((0, 0, 0), occupied=True)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        vertices = mesh['vertices']
        
        # Check that all vertices are within expected bounds [0, 1]
        assert np.all(vertices >= 0)
        assert np.all(vertices <= 1)
        
        # Check that we have 8 unique vertex positions
        unique_vertices = np.unique(vertices, axis=0)
        assert len(unique_vertices) == 8
    
    def test_face_indices(self):
        """Test that face indices are valid."""
        grid = CubeGrid((2, 2, 2))
        grid.set_cube((0, 0, 0), occupied=True)
        
        gen = MeshGenerator()
        mesh = gen.generate_mesh(grid)
        
        faces = mesh['faces']
        num_vertices = len(mesh['vertices'])
        
        # All face indices should be valid (< num_vertices)
        assert np.all(faces >= 0)
        assert np.all(faces < num_vertices)
        
        # Each face should have 3 vertices
        assert faces.shape[1] == 3
    
    def test_export_obj(self, tmp_path):
        """Test exporting mesh to OBJ format."""
        grid = CubeGrid((2, 2, 2))
        grid.set_cube((0, 0, 0), occupied=True)
        
        gen = MeshGenerator()
        mesh = gen.generate_mesh(grid)
        
        output_file = tmp_path / "test_mesh.obj"
        gen.export_obj(mesh, str(output_file))
        
        # Check that file was created
        assert output_file.exists()
        
        # Read and verify content
        content = output_file.read_text()
        
        # Should have vertex lines starting with 'v'
        v_lines = [line for line in content.split('\n') if line.startswith('v ')]
        assert len(v_lines) == 8
        
        # Should have face lines starting with 'f'
        f_lines = [line for line in content.split('\n') if line.startswith('f ')]
        assert len(f_lines) == 12
