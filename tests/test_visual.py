"""
Visual tests that generate output files for manual inspection.
These tests create visualizations and export files to verify the mesh generation works correctly.
"""
import pytest
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

from meshmaker.cube_grid import CubeGrid
from meshmaker.cube_appearance import CubeAppearance
from meshmaker.mesh_generator import MeshGenerator


# Create output directory for visual tests
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'visual_tests_output')


@pytest.fixture(scope="module", autouse=True)
def setup_output_dir():
    """Create output directory for visual tests."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    yield
    # Keep the directory for inspection


class TestVisualOutput:
    """Visual tests that generate viewable output."""
    
    def test_single_cube_visualization(self):
        """Generate visualization of a single cube."""
        grid = CubeGrid((3, 3, 3))
        grid.set_cube((1, 1, 1), occupied=True, 
                     appearance=CubeAppearance(color=(0.0, 0.5, 1.0)))
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # Create 3D visualization
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        self._plot_mesh(ax, mesh)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Single Cube Mesh')
        
        output_file = os.path.join(OUTPUT_DIR, 'single_cube.png')
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        assert os.path.exists(output_file)
    
    def test_multiple_cubes_visualization(self):
        """Generate visualization of multiple cubes with different colors."""
        grid = CubeGrid((5, 5, 5))
        
        # Create a pattern of cubes with different colors
        red = CubeAppearance(color=(1.0, 0.0, 0.0))
        green = CubeAppearance(color=(0.0, 1.0, 0.0))
        blue = CubeAppearance(color=(0.0, 0.0, 1.0))
        
        grid.set_cube((0, 0, 0), occupied=True, appearance=red)
        grid.set_cube((1, 0, 0), occupied=True, appearance=green)
        grid.set_cube((2, 0, 0), occupied=True, appearance=blue)
        grid.set_cube((0, 1, 0), occupied=True, appearance=green)
        grid.set_cube((1, 1, 0), occupied=True, appearance=blue)
        grid.set_cube((2, 1, 0), occupied=True, appearance=red)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # Create 3D visualization
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        self._plot_mesh(ax, mesh)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Multiple Colored Cubes')
        
        output_file = os.path.join(OUTPUT_DIR, 'multiple_cubes.png')
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        assert os.path.exists(output_file)
    
    def test_cube_structure_visualization(self):
        """Generate visualization of a more complex structure."""
        grid = CubeGrid((5, 5, 5))
        
        # Create a simple structure (like a cross)
        yellow = CubeAppearance(color=(1.0, 1.0, 0.0))
        
        # Vertical line
        for y in range(5):
            grid.set_cube((2, y, 2), occupied=True, appearance=yellow)
        
        # Horizontal line (x-axis)
        for x in range(5):
            grid.set_cube((x, 2, 2), occupied=True, appearance=yellow)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # Create 3D visualization
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        self._plot_mesh(ax, mesh)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Cross Structure')
        
        output_file = os.path.join(OUTPUT_DIR, 'cross_structure.png')
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        assert os.path.exists(output_file)
    
    def test_transparency_visualization(self):
        """Generate visualization showing transparency."""
        grid = CubeGrid((4, 4, 4))
        
        # Create cubes with different transparency levels
        opaque = CubeAppearance(color=(1.0, 0.0, 0.0), alpha=1.0)
        semi = CubeAppearance(color=(0.0, 1.0, 0.0), alpha=0.5)
        transparent = CubeAppearance(color=(0.0, 0.0, 1.0), alpha=0.2)
        
        grid.set_cube((0, 0, 0), occupied=True, appearance=opaque)
        grid.set_cube((1, 1, 1), occupied=True, appearance=semi)
        grid.set_cube((2, 2, 2), occupied=True, appearance=transparent)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        # Create 3D visualization
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        self._plot_mesh(ax, mesh)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Cubes with Different Transparency Levels')
        
        output_file = os.path.join(OUTPUT_DIR, 'transparency.png')
        plt.savefig(output_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        assert os.path.exists(output_file)
    
    def test_obj_export(self):
        """Test OBJ file export."""
        grid = CubeGrid((3, 3, 3))
        
        # Create a small structure
        red = CubeAppearance(color=(1.0, 0.0, 0.0))
        blue = CubeAppearance(color=(0.0, 0.0, 1.0))
        
        grid.set_cube((0, 0, 0), occupied=True, appearance=red)
        grid.set_cube((1, 0, 0), occupied=True, appearance=blue)
        grid.set_cube((1, 1, 0), occupied=True, appearance=red)
        
        gen = MeshGenerator(cube_size=1.0)
        mesh = gen.generate_mesh(grid)
        
        output_file = os.path.join(OUTPUT_DIR, 'test_export.obj')
        gen.export_obj(mesh, output_file)
        
        assert os.path.exists(output_file)
        
        # Verify OBJ file contents
        with open(output_file, 'r') as f:
            content = f.read()
            assert 'v ' in content  # Has vertices
            assert 'f ' in content  # Has faces
            assert 'color:' in content  # Has color comments
    
    def _plot_mesh(self, ax, mesh):
        """Helper to plot mesh data on a 3D axis."""
        vertices = mesh['vertices']
        faces = mesh['faces']
        colors = mesh['colors']
        
        # Create face color array (one color per face, using first vertex color)
        face_colors = []
        for face in faces:
            # Use the color of the first vertex in the face
            face_colors.append(colors[face[0]])
        
        # Create 3D polygon collection
        triangles = vertices[faces]
        collection = Poly3DCollection(triangles, facecolors=face_colors, 
                                     edgecolors='black', linewidths=0.5, alpha=0.9)
        ax.add_collection3d(collection)
        
        # Set axis limits
        if len(vertices) > 0:
            ax.set_xlim([vertices[:, 0].min() - 0.5, vertices[:, 0].max() + 0.5])
            ax.set_ylim([vertices[:, 1].min() - 0.5, vertices[:, 1].max() + 0.5])
            ax.set_zlim([vertices[:, 2].min() - 0.5, vertices[:, 2].max() + 0.5])
