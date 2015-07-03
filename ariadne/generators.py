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
                # Before moving in to the opening, check if all neighbors have
                # been visited. If no, append back to stack.
                old_row, old_col = row, col
                if not are_neighbors_visited(maze, row, col, visited):
                    stack.append((row, col))
                row, col = list(maze.move_to_opening(row, col, carve))[0]
                stack.append((row, col))

        return maze


class EllersAlgorithm(MazeGenerator):

    def generate(self, width, height):
        def make_sets_and_merge(maze, cur_row_index, set_count = None):
            if set_count is not None:
                # This is the first case set_count must not be None
                start = 0
                for limit in range(set_count, width, set_count):
                    for cur_cell in range(start, set_count):
                        if random.choice((True, False)):
                            maze.tear_down_wall(cur_row_index, cur_cell, MazeCellStates.OPEN_EAST)
                    start += set_count + 1
            else:
                prev_regions = get_regions(cur_row_index - 1)
                cur_regions = label_regions(prev_regions, cur_row_index)
                # Do the merge
                for ir, region in enumerate(cur_regions[1:], 1):
                    if region != cur_regions[ir - 1] and (random.choice((True, False)) or cur_row_index == (height - 1)):
                        cur_regions[ir - 1] = region
                        maze.tear_down_wall(cur_row_index, ir, MazeCellStates.OPEN_WEST)

        def label_regions(prev_regions, row_index):
            """
            Given the regions of the previous row, determine the current set
            memberships of each cell in the given row_index.

            This assumes that the walls between the previous row and the current
            row have been broken down. For distinction, those whose set derives
            from a cell in the previous row will have a negative label while
            those whose set is "organic" to the row will have a positive label.

            The absolute value of labels range from [1, width].
            """
            labels = [0 for _ in range(width)]
            cur_label = 1

            for ci, cell in enumerate(maze.maze[row_index]):
                if (cell & MazeCellStates.OPEN_NORTH) == MazeCellStates.OPEN_NORTH:
                    labels[ci] = -prev_regions[ci]
                else:
                    labels[ci] = cur_label
                    cur_label += 1

            return labels

        def get_regions(row_index):
            """
            Labels the continuous regions in a row in the maze. Returns a list
            of size width. The list has numbers for labels on what cell belongs
            to which region. The numbers range from [1, width].
            """
            regions = [1 for _ in range(width)]

            for cell_index in range(1, width):
                if (maze.maze[row_index][cell_index] & MazeCellStates.OPEN_WEST) == MazeCellStates.OPEN_WEST:
                    regions[cell_index] = regions[cell_index - 1]
                else:
                    regions[cell_index] = regions[cell_index - 1] + 1
            
            return regions

        maze = Maze(width, height)
        set_count = None
        # Base case: single row, where the first row is also the last row.
        if width != 2:
            # Ensure sets won't be singletons
            set_count = random.choice(range(1, width - 1))

        for i in range(height):
            if i == 0:
                make_sets_and_merge(maze, i, set_count)
            else:
                make_sets_and_merge(maze, i)

            # With the sets made, merge vertically, at least once per set.
            is_curset_merged = False
            if i != (height - 1):
                for j in range(width):
                    is_new_set_next = (maze.maze[i][j] & MazeCellStates.OPEN_EAST) != MazeCellStates.OPEN_EAST

                    if is_new_set_next and not is_curset_merged:
                        maze.tear_down_wall(i, j, MazeCellStates.OPEN_SOUTH)
                    elif random.choice((True, False)):
                        maze.tear_down_wall(i, j, MazeCellStates.OPEN_SOUTH)
                        is_curset_merged = True

                    if is_new_set_next:
                        is_curset_merged = False
        
        return maze


class KruskalsAlgorithm(MazeGenerator):
    
    def generate(self, width, height):
        maze = Maze(width, height)
        return maze
