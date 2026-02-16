#!/usr/bin/env python
"""
Example script demonstrating the MeshMaker library.
This creates a simple 3D structure and exports it.
"""

from meshmaker import CubeGrid, MeshGenerator, CubeAppearance


def main():
    # Create a 6x7x6 grid (to have room for a chimney)
    print("Creating a 6x7x6 cube grid...")
    grid = CubeGrid((6, 7, 6))
    
    # Define some colors
    red = CubeAppearance(color=(1.0, 0.0, 0.0))
    green = CubeAppearance(color=(0.0, 1.0, 0.0))
    blue = CubeAppearance(color=(0.0, 0.0, 1.0))
    yellow = CubeAppearance(color=(1.0, 1.0, 0.0))
    
    # Create a simple house-like structure
    print("Adding cubes to create a structure...")
    
    # Base (floor)
    for x in range(5):
        for z in range(5):
            grid.set_cube((x, 0, z), occupied=True, appearance=red)
    
    # Walls
    for y in range(1, 4):
        # Front and back walls
        for x in range(5):
            grid.set_cube((x, y, 0), occupied=True, appearance=green)
            grid.set_cube((x, y, 4), occupied=True, appearance=green)
        
        # Left and right walls
        for z in range(1, 4):
            grid.set_cube((0, y, z), occupied=True, appearance=green)
            grid.set_cube((4, y, z), occupied=True, appearance=green)
    
    # Roof
    for x in range(5):
        for z in range(5):
            grid.set_cube((x, 4, z), occupied=True, appearance=blue)
    
    # Add a yellow chimney
    grid.set_cube((1, 5, 1), occupied=True, appearance=yellow)
    grid.set_cube((1, 6, 1), occupied=True, appearance=yellow)
    
    print(f"Grid created with {len(grid.get_occupied_positions())} occupied cubes")
    
    # Generate the mesh
    print("Generating mesh...")
    generator = MeshGenerator(cube_size=1.0)
    mesh = generator.generate_mesh(grid)
    
    print(f"Mesh generated:")
    print(f"  - {len(mesh['vertices'])} vertices")
    print(f"  - {len(mesh['faces'])} faces")
    print(f"  - {len(mesh['colors'])} colors")
    
    # Export to OBJ
    output_file = "example_house.obj"
    print(f"Exporting to {output_file}...")
    generator.export_obj(mesh, output_file)
    print(f"Done! Mesh exported to {output_file}")


if __name__ == "__main__":
    main()
