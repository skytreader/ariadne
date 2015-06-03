import math
import random

from .mazes import Maze, MazeCellStates
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
            
            Return the direction of the opening to which the carve was made. It
            is further guaranteed that the opening made is an element of
            MazeCellStates.CARDINAL.
            """
            try:
                random_carve = random.choice(MazeCellStates.CARDINAL)
                if list(maze.move_to_opening(row, col, random_carve))[0] not in visited:
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
        stack = [(row, col)]
        visited = set()
        
        while stack:
            # backtracking clause
            while len(stack) and are_neighbors_visited(maze, row, col, visited):
                row, col = stack.pop()

            if not len(stack):
                break
                
            visited.add((row, col))
            carve = carve_randomly(maze, row, col, visited)

            while not carve and len(visited) != (width * height):
                carve = carve_randomly(maze, row, col, visited)

            if carve:
                row, col = list(maze.move_to_opening(row, col, carve))[0]
                stack.append((row, col))

        return maze

class EllersAlgorithm(MazeGenerator):

    def generate(self, width, height):
        def make_sets_and_merge(maze, cur_row_index, set_count = None):
            if set_count is not None:
                # This is the first case set_count must not be None
                # The first merge is always uniformly-distributed.
                start = 0
                for limit in range(set_count, width, set_count):
                    for cur_cell in range(start, set_count):
                        maze.tear_down_wall(cur_row_index, cur_cell, MazeCellStates.OPEN_EAST)
                    start += set_count + 1
            else:
                """
                For Eller's Algorithm, sets are actually defined by their boundaries.
                Hence, we don't need an actual set data structure, We just need
                to keep track of the "last" element in each set as that element
                is what is mergeable.
                """
                set_bounds = []
                last_cell_state = None

                for ci in range(width):
                    if last_cell_state and 
                      (maze.maze[cur_row_index][ci] & MazeCellStates.OPEN_NORTH) != (last_cell_state & MazeCellStates.OPEN_NORTH):
                        set_bounds.append(ci - 1)

                    last_cell_state = maze.maze[cur_row_index][ci]

                # Do the merge
                for bound in set_bounds:
                    if random.choice((True, False)):
                        maze.tear_down_wall(cur_row_index, bound, MazeCellStates.OPEN_EAST)
                        

        maze = Maze(width, height)
        # Ensure sets won't be singletons
        set_count = random.choice(range(width - 1))
        divisions = math.floor(width / set_count)
        # Construct the initial sets. They are in a tuple to indicate adjacency
        
        return maze
