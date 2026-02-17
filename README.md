# MeshMaker

A Python library for creating 3D meshes based on a grid of cubes where each cube can be occupied or unoccupied. Each occupied cube has parameterizable appearance properties (color, transparency, material).

## Features

- **Grid-based 3D mesh generation**: Create meshes from a 3D grid of cubes
- **Parameterizable appearance**: Each cube can have custom color, transparency, and material properties
- **Solvable maze generation**: Generate mazes with parameterizable dimensions (width and height)
- **Solution path visualization**: Display maze solutions with distinct colored cubes
- **Flexible mesh export**: Export meshes to OBJ format
- **Blender rendering**: Render 3D models with professional lighting using Blender
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

### MazeGenerator

Generates solvable mazes with parameterizable dimensions.

```python
from meshmaker import MazeGenerator, MeshGenerator, CubeAppearance

# Create a maze (dimensions must be odd numbers >= 3)
maze = MazeGenerator(
    width=15, 
    height=15,
    wall_appearance=CubeAppearance(color=(0.2, 0.2, 0.8)),  # Blue walls
    solution_appearance=CubeAppearance(color=(1.0, 1.0, 0.0))  # Yellow solution
)

# Generate the maze
maze.generate(seed=42)  # Optional seed for reproducibility

# Get solution path
solution_path = maze.get_solution_path()  # List of (x, y) coordinates

# Convert to CubeGrid
grid = maze.to_cube_grid(include_solution=False)  # Maze without solution
grid_with_solution = maze.to_cube_grid(include_solution=True)  # With solution

# Generate and export mesh
generator = MeshGenerator(cube_size=1.0)
mesh = generator.generate_mesh(grid_with_solution)
generator.export_obj(mesh, "maze_solution.obj")

# Print text representation (for debugging)
maze.print_maze(show_solution=True)
```

## Examples

### Organic Growth Example

The `example_organic_growth.py` script demonstrates a procedural shape generation algorithm that creates unique, branching structures:

```bash
python example_organic_growth.py
```

This example grows shapes using the following rules:
- Starts with a single cube
- Adds cubes one at a time to face-adjacent positions
- New cubes must touch exactly one existing cube
- New cubes cannot have corner-diagonal neighbors (prevents compact, blocky shapes)
- Uses an "openness bias" parameter to favor more branching, open structures
- Generates different shapes each time due to randomization
- Parameterizable by number of cubes and openness bias

The algorithm produces organic, coral-like or tree-like structures with natural variation. Each cube is colored with a gradient based on its height (blue at bottom → green in middle → yellow at top).

### MeshGenerator

Generates 3D mesh data from a CubeGrid.

```python
generator = MeshGenerator(cube_size=1.0)
mesh = generator.generate_mesh(grid)
generator.export_obj(mesh, "filename.obj")
```

## Blender Rendering

The project includes a Blender rendering script that can render OBJ files with professional lighting. This feature is used in the CI/CD pipeline to generate high-quality rendered images for the GitHub Pages site.

### Using the Blender Renderer

Requirements:
- Blender 3.0+ installed on your system

```bash
# Render an OBJ file with Blender
blender --background --python render_with_blender.py -- <input.obj> <output.png> [width] [height] [samples]

# Example: Render a house model
blender --background --python render_with_blender.py -- example_house.obj house_render.png 1920 1080 128

# Example with lower quality for faster rendering
blender --background --python render_with_blender.py -- example_tree.obj tree_render.png 800 600 32
```

The renderer features:
- **Three-point lighting setup**: Key light, fill light, and back/rim light for professional results
- **Vertex color support**: Automatically applies colors from OBJ file comments
- **Transparent background**: Empty spaces are rendered as transparent
- **Customizable resolution**: Set output image dimensions
- **Adjustable quality**: Control render samples for quality vs speed tradeoff

## Running Tests

Run all tests:

```bash
pytest
```

Run specific test categories:

```bash
# Unit tests only
pytest tests/test_cube_appearance.py tests/test_cube_grid.py tests/test_mesh_generator.py tests/test_maze_generator.py

# Visual tests (generates output images)
pytest tests/test_visual.py

# Test maze generation specifically
pytest tests/test_maze_generator.py -v
```

Visual test output is saved to `visual_tests_output/` directory.

## Continuous Integration and GitHub Pages

This project uses GitHub Actions to automatically run tests and deploy example outputs to GitHub Pages whenever changes are pushed to the main branch.

### Workflow Overview

The CI/CD workflow (`.github/workflows/ci-and-deploy.yml`) performs the following steps:

1. **Run Tests**: Executes all unit tests and visual tests using pytest
2. **Generate Examples**: Runs example scripts to create house, tree, and maze models
3. **Render with Blender**: Uses Blender to render the 3D models with professional lighting
4. **Deploy to Pages**: Publishes the generated 3D models, renders, and visualizations to GitHub Pages

### Viewing the Output

Once deployed, you can view the example output at: `https://arachtivix.github.io/meshmaker-1/`

The GitHub Pages site includes:
- **Blender-rendered images**: High-quality renders with professional lighting showcasing the 3D models
- Interactive gallery of visual test outputs
- Downloadable 3D model files (OBJ format) including house, tree, and maze examples
- Maze examples both with and without solution paths
- Documentation about the project

## Project Structure

```
meshmaker-1/
├── src/
│   └── meshmaker/
│       ├── __init__.py
│       ├── cube_appearance.py   # Cube appearance properties
│       ├── cube_grid.py          # 3D grid management
│       ├── maze_generator.py     # Maze generation
│       └── mesh_generator.py     # Mesh generation
├── tests/
│   ├── test_cube_appearance.py   # Unit tests
│   ├── test_cube_grid.py         # Unit tests
│   ├── test_maze_generator.py    # Maze generation tests
│   ├── test_mesh_generator.py    # Unit tests
│   └── test_visual.py            # Visual tests
├── example.py                    # House example
├── example_maze.py               # Maze examples
├── example_tree.py               # Tree example
├── example_organic_growth.py     # Organic growth example
├── pyproject.toml
└── README.md
```

## License

MIT