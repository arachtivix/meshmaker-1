#!/usr/bin/env python
"""
Example script demonstrating a tree structure using the MeshMaker library.
This creates a tree with a trunk and layered foliage.
"""

from meshmaker import CubeGrid, MeshGenerator, CubeAppearance


def main():
    print("=" * 60)
    print("MeshMaker - Tree Example")
    print("=" * 60)
    
    # Create a 11x15x11 grid (wide enough for foliage, tall for tree)
    print("\nCreating a 11x15x11 cube grid...")
    grid = CubeGrid((11, 15, 11))
    
    # Define colors for the tree
    trunk_brown = CubeAppearance(color=(0.55, 0.27, 0.07))  # Brown trunk
    dark_green = CubeAppearance(color=(0.0, 0.5, 0.0))      # Dark green foliage
    light_green = CubeAppearance(color=(0.2, 0.8, 0.2))     # Light green foliage
    
    print("Building tree structure...")
    
    # Build the trunk (centered at x=5, z=5)
    trunk_x, trunk_z = 5, 5
    trunk_height = 7
    
    # Trunk base (2x2)
    for y in range(trunk_height):
        for x in range(trunk_x - 1, trunk_x + 1):
            for z in range(trunk_z - 1, trunk_z + 1):
                grid.set_cube((x, y, z), occupied=True, appearance=trunk_brown)
    
    # Build the foliage in layers (pyramid/cone shape)
    # Layer 1 (bottom, largest) - y = 7
    foliage_base_y = trunk_height
    layer_configs = [
        # (y_offset, radius, appearance)
        (0, 4, dark_green),   # Bottom layer - widest
        (1, 4, light_green),  # Second layer
        (2, 3, dark_green),   # Third layer
        (3, 3, light_green),  # Fourth layer
        (4, 2, dark_green),   # Fifth layer
        (5, 2, light_green),  # Sixth layer
        (6, 1, dark_green),   # Top layer - smallest
    ]
    
    for y_offset, radius, appearance in layer_configs:
        y = foliage_base_y + y_offset
        for x in range(trunk_x - radius, trunk_x + radius + 1):
            for z in range(trunk_z - radius, trunk_z + radius + 1):
                # Create a circular/diamond pattern for more natural look
                distance = abs(x - trunk_x) + abs(z - trunk_z)
                if distance <= radius:
                    # Don't overwrite trunk cubes
                    if not (trunk_x - 1 <= x < trunk_x + 1 and trunk_z - 1 <= z < trunk_z + 1 and y < foliage_base_y + 1):
                        grid.set_cube((x, y, z), occupied=True, appearance=appearance)
    
    # Add a star/tip at the very top
    top_y = foliage_base_y + len(layer_configs)
    grid.set_cube((trunk_x, top_y, trunk_z), occupied=True, appearance=light_green)
    
    occupied_count = len(grid.get_occupied_positions())
    print(f"✓ Tree created with {occupied_count} cubes")
    print(f"  - Trunk: {trunk_height} cubes tall")
    print(f"  - Foliage: {len(layer_configs)} layers")
    
    # Generate the mesh
    print("\nGenerating mesh...")
    generator = MeshGenerator(cube_size=1.0)
    mesh = generator.generate_mesh(grid)
    
    print(f"✓ Mesh generated:")
    print(f"  - {len(mesh['vertices'])} vertices")
    print(f"  - {len(mesh['faces'])} faces")
    print(f"  - {len(mesh['colors'])} colors")
    
    # Export to OBJ
    output_file = "example_tree.obj"
    print(f"\nExporting to {output_file}...")
    generator.export_obj(mesh, output_file)
    print(f"✓ Tree mesh exported to {output_file}")
    
    print("\n" + "=" * 60)
    print("Tree example completed successfully!")
    print("=" * 60)
    print(f"\nFile created: {output_file}")
    print("This OBJ file can be opened in 3D modeling software like Blender or MeshLab.")


if __name__ == "__main__":
    main()
