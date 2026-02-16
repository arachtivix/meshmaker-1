# MeshMaker

A Python library for creating 3D meshes based on a grid of cubes where each cube can be occupied or unoccupied. Each occupied cube has parameterizable appearance properties (color, transparency, material).

## Features

- **Grid-based 3D mesh generation**: Create meshes from a 3D grid of cubes
- **Parameterizable appearance**: Each cube can have custom color, transparency, and material properties
- **Flexible mesh export**: Export meshes to OBJ format
- **Comprehensive testing**: Unit tests and visual tests with rendered output

## Installation

```bash
pip install -e .
```

For development with testing tools:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from meshmaker import CubeGrid, MeshGenerator, CubeAppearance

# Create a 5x5x5 grid
grid = CubeGrid((5, 5, 5))

# Add some cubes with different appearances
red = CubeAppearance(color=(1.0, 0.0, 0.0))
blue = CubeAppearance(color=(0.0, 0.0, 1.0), alpha=0.5)

grid.set_cube((0, 0, 0), occupied=True, appearance=red)
grid.set_cube((1, 1, 1), occupied=True, appearance=blue)

# Generate the mesh
generator = MeshGenerator(cube_size=1.0)
mesh = generator.generate_mesh(grid)

# Export to OBJ file
generator.export_obj(mesh, "output.obj")

# Access mesh data
vertices = mesh['vertices']  # Nx3 array of vertex positions
faces = mesh['faces']        # Mx3 array of triangle indices
colors = mesh['colors']      # Nx4 array of RGBA colors
```

## API Reference

### CubeGrid

Represents a 3D grid where each cell can be occupied or unoccupied.

```python
grid = CubeGrid(dimensions=(x, y, z))
grid.set_cube((x, y, z), occupied=True, appearance=appearance)
grid.get_cube((x, y, z))  # Returns True if occupied
grid.get_appearance((x, y, z))  # Returns CubeAppearance
grid.get_occupied_positions()  # Returns list of occupied positions
```

### CubeAppearance

Defines visual properties of a cube.

```python
appearance = CubeAppearance(
    color=(r, g, b),  # RGB values 0-1
    alpha=1.0,        # Transparency 0-1
    material="default"
)
```

### MeshGenerator

Generates 3D mesh data from a CubeGrid.

```python
generator = MeshGenerator(cube_size=1.0)
mesh = generator.generate_mesh(grid)
generator.export_obj(mesh, "filename.obj")
```

## Running Tests

Run all tests:

```bash
pytest
```

Run specific test categories:

```bash
# Unit tests only
pytest tests/test_cube_appearance.py tests/test_cube_grid.py tests/test_mesh_generator.py

# Visual tests (generates output images)
pytest tests/test_visual.py
```

Visual test output is saved to `visual_tests_output/` directory.

## Continuous Integration and GitHub Pages

This project uses GitHub Actions to automatically run tests and deploy example outputs to GitHub Pages whenever changes are pushed to the main branch.

### Workflow Overview

The CI/CD workflow (`.github/workflows/ci-and-deploy.yml`) performs the following steps:

1. **Run Tests**: Executes all unit tests and visual tests using pytest
2. **Generate Example**: Runs `example.py` to create the house model
3. **Deploy to Pages**: Publishes the generated 3D model and visualizations to GitHub Pages

### Viewing the Output

Once deployed, you can view the example output at: `https://arachtivix.github.io/meshmaker-1/`

The GitHub Pages site includes:
- Interactive gallery of visual test outputs
- Downloadable 3D model file (OBJ format)
- Documentation about the project

## Project Structure

```
meshmaker-1/
├── src/
│   └── meshmaker/
│       ├── __init__.py
│       ├── cube_appearance.py   # Cube appearance properties
│       ├── cube_grid.py          # 3D grid management
│       └── mesh_generator.py     # Mesh generation
├── tests/
│   ├── test_cube_appearance.py   # Unit tests
│   ├── test_cube_grid.py         # Unit tests
│   ├── test_mesh_generator.py    # Unit tests
│   └── test_visual.py            # Visual tests
├── pyproject.toml
└── README.md
```

## License

MIT