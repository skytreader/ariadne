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
            try:
                random_carve = random.choice(MazeCellState.CARDINAL)
                if maze.move_to_opening(row, col, random_carve) not in visited:
                    maze.tear_down_wall(row, col, random_carve)
                    return random_carve

                return None
            except CantTearWallException:
                return None

        maze = Maze(width, height)
        row = random.choice(range(height))
        col = random.choice(range(width))
        visited = []
        
        while stack:
            visited.append((row, col))
            carve = carve_randomly(maze, row, col)

            while !carve:
                carve = carve_randomly(maze, row, col)

            row, col = maze.move_to_opening(row, col, carve)
