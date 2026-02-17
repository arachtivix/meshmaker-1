"""
MazeGenerator - Creates solvable 3D mazes with parameterizable dimensions.
"""
import random
from typing import Tuple, List, Optional
from .cube_grid import CubeGrid
from .cube_appearance import CubeAppearance


class MazeGenerator:
    """
    Generates solvable mazes with walls represented as cubes.
    Uses recursive backtracking algorithm to ensure mazes are solvable.
    """
    
    def __init__(self, width: int, height: int, wall_appearance: Optional[CubeAppearance] = None,
                 path_appearance: Optional[CubeAppearance] = None,
                 solution_appearance: Optional[CubeAppearance] = None):
        """
        Initialize the maze generator.
        
        Args:
            width: Width of the maze in cubes (must be odd, >= 3)
            height: Height of the maze in cubes (must be odd, >= 3)
            wall_appearance: Appearance for wall cubes (default: white)
            path_appearance: Appearance for path/floor cubes (default: black/empty)
            solution_appearance: Appearance for solution path cubes (default: yellow)
        """
        if width < 3 or height < 3:
            raise ValueError("Maze dimensions must be at least 3x3")
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("Maze dimensions must be odd numbers")
        
        self.width = width
        self.height = height
        self.wall_appearance = wall_appearance or CubeAppearance(color=(0.8, 0.8, 0.8))
        self.path_appearance = path_appearance
        self.solution_appearance = solution_appearance or CubeAppearance(color=(1.0, 1.0, 0.0))
        
        # Internal maze representation: True = wall, False = path
        self._maze = [[True for _ in range(width)] for _ in range(height)]
        self._solution_path = []
    
    def generate(self, seed: Optional[int] = None) -> None:
        """
        Generate a new maze using recursive backtracking algorithm.
        
        Args:
            seed: Optional random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        # Reset maze - all walls
        self._maze = [[True for _ in range(self.width)] for _ in range(self.height)]
        
        # Start position (top-left corner, adjusted to be on path grid)
        start = (1, 1)
        
        # Use recursive backtracking to carve paths
        self._carve_path(start[0], start[1])
        
        # Set entry and exit
        self._maze[0][1] = False  # Entry at top
        self._maze[self.height - 1][self.width - 2] = False  # Exit at bottom
        
        # Find solution path
        self._solution_path = self._find_solution()
    
    def _carve_path(self, x: int, y: int) -> None:
        """
        Recursively carve paths through the maze.
        
        Args:
            x: X coordinate in maze grid
            y: Y coordinate in maze grid
        """
        # Mark current cell as path
        self._maze[y][x] = False
        
        # Define possible directions: up, right, down, left
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is valid and unvisited (still a wall)
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self._maze[ny][nx]):
                
                # Carve path between current and next cell
                self._maze[y + dy // 2][x + dx // 2] = False
                
                # Recursively carve from new cell
                self._carve_path(nx, ny)
    
    def _find_solution(self) -> List[Tuple[int, int]]:
        """
        Find the solution path from entry to exit using BFS.
        
        Returns:
            List of (x, y) coordinates representing the solution path
            
        Raises:
            RuntimeError: If no solution path is found (should not happen with proper generation)
        """
        from collections import deque
        
        # Entry and exit positions
        start = (1, 0)
        end = (self.width - 2, self.height - 1)
        
        # BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == end:
                return path
            
            # Check all four directions
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self._maze[ny][nx] and (nx, ny) not in visited):
                    
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        raise RuntimeError("No solution path found - maze generation failed")
    
    def to_cube_grid(self, include_solution: bool = False) -> CubeGrid:
        """
        Convert the maze to a CubeGrid.
        
        Args:
            include_solution: If True, mark solution path with distinct appearance
            
        Returns:
            CubeGrid representing the maze
        """
        # Create a grid with height=1 (2D maze in 3D space)
        grid = CubeGrid((self.width, 1, self.height))
        
        # Solution coordinates set for quick lookup
        solution_set = set(self._solution_path) if include_solution else set()
        
        # Add cubes for walls and paths
        for y in range(self.height):
            for x in range(self.width):
                if self._maze[y][x]:
                    # Wall cube
                    grid.set_cube((x, 0, y), occupied=True, appearance=self.wall_appearance)
                elif (x, y) in solution_set and self.solution_appearance:
                    # Solution path cube
                    grid.set_cube((x, 0, y), occupied=True, appearance=self.solution_appearance)
                elif self.path_appearance:
                    # Regular path cube (optional)
                    grid.set_cube((x, 0, y), occupied=True, appearance=self.path_appearance)
        
        return grid
    
    def get_solution_path(self) -> List[Tuple[int, int]]:
        """
        Get the solution path coordinates.
        
        Returns:
            List of (x, y) tuples representing the solution path
        """
        return self._solution_path.copy()
    
    def print_maze(self, show_solution: bool = False) -> None:
        """
        Print a text representation of the maze (for debugging).
        
        Args:
            show_solution: If True, mark solution path with 'o'
        """
        solution_set = set(self._solution_path) if show_solution else set()
        
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in solution_set:
                    row += "o"
                elif self._maze[y][x]:
                    row += "█"
                else:
                    row += " "
            print(row)
