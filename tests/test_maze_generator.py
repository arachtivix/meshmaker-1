"""
Unit tests for MazeGenerator class.
"""
import pytest
from meshmaker.maze_generator import MazeGenerator
from meshmaker.cube_appearance import CubeAppearance


class TestMazeGenerator:
    """Test suite for MazeGenerator."""
    
    def test_maze_creation(self):
        """Test basic maze creation with valid dimensions."""
        maze = MazeGenerator(width=5, height=5)
        assert maze.width == 5
        assert maze.height == 5
    
    def test_invalid_dimensions_too_small(self):
        """Test that dimensions smaller than 3 raise error."""
        with pytest.raises(ValueError, match="must be at least 3x3"):
            MazeGenerator(width=1, height=5)
        
        with pytest.raises(ValueError, match="must be at least 3x3"):
            MazeGenerator(width=5, height=2)
    
    def test_invalid_dimensions_even(self):
        """Test that even dimensions raise error."""
        with pytest.raises(ValueError, match="must be odd numbers"):
            MazeGenerator(width=4, height=5)
        
        with pytest.raises(ValueError, match="must be odd numbers"):
            MazeGenerator(width=5, height=6)
    
    def test_maze_generation(self):
        """Test maze generation creates a maze."""
        maze = MazeGenerator(width=7, height=7)
        maze.generate(seed=42)  # Use seed for reproducibility
        
        # Check that solution path exists
        solution = maze.get_solution_path()
        assert len(solution) > 0
        
        # Check that entry and exit are clear
        assert not maze._maze[0][1]  # Entry
        assert not maze._maze[maze.height - 1][maze.width - 2]  # Exit
    
    def test_maze_with_seed_reproducible(self):
        """Test that same seed produces same maze."""
        maze1 = MazeGenerator(width=7, height=7)
        maze1.generate(seed=123)
        
        maze2 = MazeGenerator(width=7, height=7)
        maze2.generate(seed=123)
        
        # Check that both mazes have same structure
        assert maze1._maze == maze2._maze
        assert maze1.get_solution_path() == maze2.get_solution_path()
    
    def test_different_seeds_different_mazes(self):
        """Test that different seeds produce different mazes."""
        maze1 = MazeGenerator(width=7, height=7)
        maze1.generate(seed=1)
        
        maze2 = MazeGenerator(width=7, height=7)
        maze2.generate(seed=2)
        
        # Mazes should be different
        assert maze1._maze != maze2._maze
    
    def test_solution_path_valid(self):
        """Test that solution path is valid (no walls)."""
        maze = MazeGenerator(width=9, height=9)
        maze.generate(seed=42)
        
        solution = maze.get_solution_path()
        
        # Check that all positions in solution are paths (not walls)
        for x, y in solution:
            assert not maze._maze[y][x], f"Solution passes through wall at ({x}, {y})"
    
    def test_solution_path_connected(self):
        """Test that solution path is connected (each step is adjacent)."""
        maze = MazeGenerator(width=9, height=9)
        maze.generate(seed=42)
        
        solution = maze.get_solution_path()
        assert len(solution) >= 2
        
        # Check that each consecutive pair is adjacent
        for i in range(len(solution) - 1):
            x1, y1 = solution[i]
            x2, y2 = solution[i + 1]
            
            # Manhattan distance should be 1
            distance = abs(x2 - x1) + abs(y2 - y1)
            assert distance == 1, f"Non-adjacent steps in solution: ({x1},{y1}) to ({x2},{y2})"
    
    def test_solution_starts_at_entry(self):
        """Test that solution path starts at entry point."""
        maze = MazeGenerator(width=7, height=7)
        maze.generate(seed=42)
        
        solution = maze.get_solution_path()
        assert len(solution) > 0
        assert solution[0] == (1, 0), "Solution should start at entry point"
    
    def test_solution_ends_at_exit(self):
        """Test that solution path ends at exit point."""
        maze = MazeGenerator(width=7, height=7)
        maze.generate(seed=42)
        
        solution = maze.get_solution_path()
        assert len(solution) > 0
        assert solution[-1] == (maze.width - 2, maze.height - 1), "Solution should end at exit point"
    
    def test_to_cube_grid_without_solution(self):
        """Test conversion to CubeGrid without solution."""
        maze = MazeGenerator(width=5, height=5)
        maze.generate(seed=42)
        
        grid = maze.to_cube_grid(include_solution=False)
        
        # Check grid dimensions (width x 1 x height)
        assert grid.dimensions == (5, 1, 5)
        
        # Check that walls are represented as occupied cubes
        for y in range(maze.height):
            for x in range(maze.width):
                is_wall = maze._maze[y][x]
                is_occupied = grid.get_cube((x, 0, y))
                
                # Without path_appearance, only walls should be occupied
                if is_wall:
                    assert is_occupied, f"Wall at ({x},{y}) should be occupied cube"
    
    def test_to_cube_grid_with_solution(self):
        """Test conversion to CubeGrid with solution."""
        maze = MazeGenerator(width=5, height=5)
        maze.generate(seed=42)
        
        grid = maze.to_cube_grid(include_solution=True)
        
        # Check that solution path cubes have correct appearance
        solution = maze.get_solution_path()
        for x, y in solution:
            assert grid.get_cube((x, 0, y))
            appearance = grid.get_appearance((x, 0, y))
            # Should be solution appearance (yellow by default)
            assert appearance.color == (1.0, 1.0, 0.0)
    
    def test_custom_appearances(self):
        """Test maze with custom appearances."""
        wall_app = CubeAppearance(color=(1.0, 0.0, 0.0))  # Red walls
        solution_app = CubeAppearance(color=(0.0, 1.0, 0.0))  # Green solution
        
        maze = MazeGenerator(
            width=5, 
            height=5,
            wall_appearance=wall_app,
            solution_appearance=solution_app
        )
        maze.generate(seed=42)
        
        assert maze.wall_appearance.color == (1.0, 0.0, 0.0)
        assert maze.solution_appearance.color == (0.0, 1.0, 0.0)
    
    def test_larger_maze(self):
        """Test generation of larger maze."""
        maze = MazeGenerator(width=21, height=21)
        maze.generate(seed=42)
        
        # Should have a valid solution
        solution = maze.get_solution_path()
        assert len(solution) > 0
        
        # Solution should be reasonably long for a 21x21 maze
        assert len(solution) > 10
    
    def test_get_solution_path_returns_copy(self):
        """Test that get_solution_path returns a copy, not reference."""
        maze = MazeGenerator(width=5, height=5)
        maze.generate(seed=42)
        
        solution1 = maze.get_solution_path()
        solution2 = maze.get_solution_path()
        
        # Should be equal but not the same object
        assert solution1 == solution2
        assert solution1 is not solution2
