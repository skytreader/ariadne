import random

from .mazes import Maze, MazeCellState
from .errors import CantTearWallException

"""
Don't think of Python generators. This is None of those!
"""

class MazeGenerator(object):
    
    def generate(self, width, height):
        """
        Returns a Maze with the walls carved with the given dimensions.
        """
        raise NotImplementedError("Can't generate a Maze :C")

class RecursiveBacktracker(MazeGenerator):
    
    def generate(self, width, height):

        def carve_randomly(maze, row, col, visited):
            """
            Carves a random wall in the specified cell of the maze. The cell to
            which the resulting opening leads is guaranteed to be unvisited.
            """
            try:
                random_carve = random.choice(MazeCellState.CARDINAL)
                if maze.move_to_opening(row, col, random_carve) not in visited:
                    maze.tear_down_wall(row, col, random_carve)
                    return random_carve

                return None
            except CantTearWallException:
                return None

        def are_neighbors_visited(maze, row, col, visited):
            """
            Return True if and only if all the neighbors of the indicated cell
            has been visited.
            """
            neighbors = maze.get_adjacent(row, col)
            
            for n in neighbors:
                if n not in visited:
                    return False

            return True

        maze = Maze(width, height)
        row = random.choice(range(height))
        col = random.choice(range(width))
        stack = []
        visited = set()
        
        while stack:
            # backtracking clause
            while are_neighbors_visited(maze, row, col, visited):
                row, col = stack.pop()
                
            visited.add((row, col))
            stack.append((row, col))
            carve = carve_randomly(maze, row, col)

            while !carve:
                carve = carve_randomly(maze, row, col)

            row, col = maze.move_to_opening(row, col, carve)

        return maze
