#!/usr/bin/env python
"""
Example script demonstrating the MazeGenerator feature.
This creates solvable mazes with parameterizable dimensions and shows the solution path.
"""

from meshmaker import MazeGenerator, MeshGenerator, CubeAppearance


def main():
    print("=" * 60)
    print("MeshMaker - Maze Generation Example")
    print("=" * 60)
    
    # Create a maze with specific dimensions
    # Note: dimensions must be odd numbers >= 3
    maze_width = 15
    maze_height = 15
    
    print(f"\nCreating a {maze_width}x{maze_height} maze...")
    
    # Define appearances
    wall_appearance = CubeAppearance(color=(0.2, 0.2, 0.8))  # Blue walls
    solution_appearance = CubeAppearance(color=(1.0, 0.8, 0.0))  # Yellow/gold solution
    
    # Create the maze generator
    maze = MazeGenerator(
        width=maze_width,
        height=maze_height,
        wall_appearance=wall_appearance,
        solution_appearance=solution_appearance
    )
    
    # Generate the maze with a specific seed for reproducibility
    print("Generating maze...")
    maze.generate(seed=42)
    
    # Get solution path info
    solution_path = maze.get_solution_path()
    print(f"Maze generated successfully!")
    print(f"  - Solution path length: {len(solution_path)} steps")
    
    # Print text representation
    print("\nText representation of the maze:")
    print("(Entry at top, Exit at bottom)")
    maze.print_maze(show_solution=False)
    
    # Create mesh generator
    mesh_gen = MeshGenerator(cube_size=1.0)
    
    # Export maze without solution
    print("\n" + "=" * 60)
    print("Exporting maze WITHOUT solution...")
    grid_no_solution = maze.to_cube_grid(include_solution=False)
    mesh_no_solution = mesh_gen.generate_mesh(grid_no_solution)
    
    output_file_no_solution = "example_maze.obj"
    mesh_gen.export_obj(mesh_no_solution, output_file_no_solution)
    print(f"✓ Maze exported to {output_file_no_solution}")
    print(f"  - {len(mesh_no_solution['vertices'])} vertices")
    print(f"  - {len(mesh_no_solution['faces'])} faces")
    
    # Export maze with solution
    print("\n" + "=" * 60)
    print("Exporting maze WITH solution path...")
    grid_with_solution = maze.to_cube_grid(include_solution=True)
    mesh_with_solution = mesh_gen.generate_mesh(grid_with_solution)
    
    output_file_with_solution = "example_maze_solution.obj"
    mesh_gen.export_obj(mesh_with_solution, output_file_with_solution)
    print(f"✓ Maze with solution exported to {output_file_with_solution}")
    print(f"  - {len(mesh_with_solution['vertices'])} vertices")
    print(f"  - {len(mesh_with_solution['faces'])} faces")
    
    # Create a smaller maze for visual comparison
    print("\n" + "=" * 60)
    print("Creating a smaller 9x9 maze for easier visualization...")
    
    small_maze = MazeGenerator(
        width=9,
        height=9,
        wall_appearance=CubeAppearance(color=(0.7, 0.3, 0.3)),  # Reddish walls
        solution_appearance=CubeAppearance(color=(0.3, 1.0, 0.3))  # Green solution
    )
    small_maze.generate(seed=123)
    
    print("\nSmall maze without solution:")
    small_maze.print_maze(show_solution=False)
    
    print("\nSmall maze WITH solution (shown as 'o'):")
    small_maze.print_maze(show_solution=True)
    
    # Export small mazes
    grid_small = small_maze.to_cube_grid(include_solution=False)
    mesh_small = mesh_gen.generate_mesh(grid_small)
    mesh_gen.export_obj(mesh_small, "example_maze_small.obj")
    print(f"\n✓ Small maze exported to example_maze_small.obj")
    
    grid_small_solution = small_maze.to_cube_grid(include_solution=True)
    mesh_small_solution = mesh_gen.generate_mesh(grid_small_solution)
    mesh_gen.export_obj(mesh_small_solution, "example_maze_small_solution.obj")
    print(f"✓ Small maze with solution exported to example_maze_small_solution.obj")
    
    print("\n" + "=" * 60)
    print("All mazes exported successfully!")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  1. {output_file_no_solution} - Large maze (15x15)")
    print(f"  2. {output_file_with_solution} - Large maze with solution")
    print(f"  3. example_maze_small.obj - Small maze (9x9)")
    print(f"  4. example_maze_small_solution.obj - Small maze with solution")
    print("\nThese OBJ files can be opened in 3D modeling software like Blender or MeshLab.")


if __name__ == "__main__":
    main()
