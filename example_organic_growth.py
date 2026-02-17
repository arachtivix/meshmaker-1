#!/usr/bin/env python
"""
Example script demonstrating organic shape growth using the MeshMaker library.
This creates a shape that grows by adding cubes with specific rules:
- Start with a single cube
- Add cubes to faces where they touch only one existing cube
- Ensure new cubes have no diagonal neighbors
- Favor more open shapes with randomization
"""

import random
from meshmaker import CubeGrid, MeshGenerator, CubeAppearance


def get_adjacent_positions(position):
    """
    Get the 6 face-adjacent positions (up, down, left, right, forward, back).
    
    Args:
        position: (x, y, z) tuple
        
    Returns:
        List of 6 adjacent positions
    """
    x, y, z = position
    return [
        (x + 1, y, z),  # right
        (x - 1, y, z),  # left
        (x, y + 1, z),  # up
        (x, y - 1, z),  # down
        (x, y, z + 1),  # forward
        (x, y, z - 1),  # back
    ]


def get_diagonal_neighbors(position):
    """
    Get corner-diagonal neighbor positions (the 8 corners).
    These are positions that differ in all three coordinates.
    Edge-adjacent neighbors (differing in 2 coordinates) are allowed.
    
    Args:
        position: (x, y, z) tuple
        
    Returns:
        List of corner-diagonal neighbor positions
    """
    x, y, z = position
    neighbors = []
    
    # Only corner diagonals - all three coordinates differ
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            for dz in [-1, 1]:
                neighbors.append((x + dx, y + dy, z + dz))
    
    return neighbors


def count_adjacent_cubes(position, occupied_positions):
    """
    Count how many face-adjacent cubes are occupied.
    
    Args:
        position: (x, y, z) tuple to check
        occupied_positions: Set of occupied positions
        
    Returns:
        Number of adjacent occupied cubes
    """
    adjacent = get_adjacent_positions(position)
    return sum(1 for pos in adjacent if pos in occupied_positions)


def has_diagonal_neighbor(position, occupied_positions):
    """
    Check if a position has any diagonal neighbors.
    
    Args:
        position: (x, y, z) tuple to check
        occupied_positions: Set of occupied positions
        
    Returns:
        True if any diagonal neighbor is occupied
    """
    diagonals = get_diagonal_neighbors(position)
    return any(pos in occupied_positions for pos in diagonals)


def get_valid_growth_positions(occupied_positions):
    """
    Get all valid positions where a new cube can be added according to rules:
    - Must be adjacent to exactly one existing cube (face-adjacent)
    - Must not have any diagonal neighbors
    
    Args:
        occupied_positions: Set of currently occupied positions
        
    Returns:
        List of valid positions for growth
    """
    candidates = set()
    
    # Find all positions adjacent to occupied cubes
    for pos in occupied_positions:
        for adj_pos in get_adjacent_positions(pos):
            if adj_pos not in occupied_positions:
                candidates.add(adj_pos)
    
    # Filter candidates by rules
    valid_positions = []
    for candidate in candidates:
        # Rule 1: Must touch exactly one cube
        if count_adjacent_cubes(candidate, occupied_positions) == 1:
            # Rule 2: Must not have diagonal neighbors
            if not has_diagonal_neighbor(candidate, occupied_positions):
                valid_positions.append(candidate)
    
    return valid_positions


def calculate_openness_score(position, occupied_positions):
    """
    Calculate an "openness" score for a position.
    Higher score means more open (fewer nearby cubes).
    This helps favor more open, branching shapes.
    
    Args:
        position: (x, y, z) tuple
        occupied_positions: Set of occupied positions
        
    Returns:
        Openness score (higher = more open)
    """
    # Count cubes in a 3x3x3 neighborhood (excluding diagonals already checked)
    x, y, z = position
    nearby_count = 0
    
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            for dz in range(-2, 3):
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                check_pos = (x + dx, y + dy, z + dz)
                if check_pos in occupied_positions:
                    nearby_count += 1
    
    # Return inverse - fewer nearby cubes = higher score
    return 100 - nearby_count


def grow_organic_shape(num_cubes, seed=None, openness_bias=0.7):
    """
    Grow an organic shape by adding cubes according to rules.
    
    Args:
        num_cubes: Total number of cubes in the final shape
        seed: Random seed for reproducibility (None for random)
        openness_bias: Probability (0-1) of choosing more open positions.
                      Higher values favor more open, branching shapes.
                      Lower values create more compact shapes.
    
    Returns:
        Set of occupied positions
    """
    if seed is not None:
        random.seed(seed)
    
    if num_cubes < 1:
        raise ValueError("num_cubes must be at least 1")
    
    # Start with a single cube at origin
    occupied_positions = {(0, 0, 0)}
    
    # Grow the shape
    for i in range(num_cubes - 1):
        valid_positions = get_valid_growth_positions(occupied_positions)
        
        if not valid_positions:
            print(f"Warning: No valid positions found after adding {i + 1} cubes")
            break
        
        # Choose next position with bias toward openness
        if random.random() < openness_bias and len(valid_positions) > 1:
            # Score all positions by openness
            scored_positions = [
                (pos, calculate_openness_score(pos, occupied_positions))
                for pos in valid_positions
            ]
            # Sort by score (descending) and pick from top choices
            scored_positions.sort(key=lambda x: x[1], reverse=True)
            # Pick randomly from top 30% to maintain variety
            top_count = max(1, len(scored_positions) // 3)
            chosen_pos = random.choice([p for p, s in scored_positions[:top_count]])
        else:
            # Random choice
            chosen_pos = random.choice(valid_positions)
        
        occupied_positions.add(chosen_pos)
    
    return occupied_positions


def main():
    print("=" * 60)
    print("MeshMaker - Organic Growth Example")
    print("=" * 60)
    
    # Parameters
    num_cubes = 50
    openness_bias = 0.7  # 70% chance to prefer open positions
    
    print(f"\nGrowing an organic shape with {num_cubes} cubes...")
    print(f"Openness bias: {openness_bias} (higher = more branching)")
    
    # Grow the shape
    occupied_positions = grow_organic_shape(
        num_cubes=num_cubes,
        seed=None,  # Use None for random, or a number for reproducible shapes
        openness_bias=openness_bias
    )
    
    print(f"✓ Shape grown successfully with {len(occupied_positions)} cubes")
    
    # Find the bounding box
    if occupied_positions:
        xs = [pos[0] for pos in occupied_positions]
        ys = [pos[1] for pos in occupied_positions]
        zs = [pos[2] for pos in occupied_positions]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        
        print(f"  - Bounding box: X[{min_x}, {max_x}], Y[{min_y}, {max_y}], Z[{min_z}, {max_z}]")
        
        # Create grid with some padding
        padding = 2
        grid_dims = (
            max_x - min_x + 1 + 2 * padding,
            max_y - min_y + 1 + 2 * padding,
            max_z - min_z + 1 + 2 * padding
        )
        offset = (-min_x + padding, -min_y + padding, -min_z + padding)
        
        print(f"  - Grid dimensions: {grid_dims}")
        
        # Create the grid
        grid = CubeGrid(grid_dims)
        
        # Generate color gradient based on height (y-coordinate)
        height_range = max_y - min_y if max_y != min_y else 1
        
        for pos in occupied_positions:
            # Translate to grid coordinates
            grid_pos = (
                pos[0] + offset[0],
                pos[1] + offset[1],
                pos[2] + offset[2]
            )
            
            # Color based on height - blue at bottom, green in middle, yellow at top
            normalized_height = (pos[1] - min_y) / height_range if height_range > 0 else 0.5
            
            if normalized_height < 0.5:
                # Blue to green
                t = normalized_height * 2
                color = (0.0, 0.4 + t * 0.4, 1.0 - t * 0.5)
            else:
                # Green to yellow
                t = (normalized_height - 0.5) * 2
                color = (t * 0.9, 0.8, 0.5 - t * 0.5)
            
            appearance = CubeAppearance(color=color)
            grid.set_cube(grid_pos, occupied=True, appearance=appearance)
        
        # Generate and export mesh
        print("\nGenerating mesh...")
        generator = MeshGenerator(cube_size=1.0)
        mesh = generator.generate_mesh(grid)
        
        print(f"✓ Mesh generated:")
        print(f"  - {len(mesh['vertices'])} vertices")
        print(f"  - {len(mesh['faces'])} faces")
        
        output_file = "example_organic_growth.obj"
        print(f"\nExporting to {output_file}...")
        generator.export_obj(mesh, output_file)
        print(f"✓ Organic shape exported to {output_file}")
        
        print("\n" + "=" * 60)
        print("Organic growth example completed successfully!")
        print("=" * 60)
        print(f"\nFile created: {output_file}")
        print("Run this script multiple times to see different shapes!")
        print("This OBJ file can be opened in 3D modeling software like Blender or MeshLab.")


if __name__ == "__main__":
    main()
