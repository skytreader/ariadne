from ..mazes import Maze, MazeCellStates
from ..generators import RecursiveBacktracker

import unittest

class RecursiveBacktrackerTest(unittest.TestCase):
    """
    Some shallow tests for the generator.

    Just makes sure that all cells have been carved.
    """

    def setUp(self):
        self.generator = RecursiveBacktracker()
    
    def test_generate(self):
        gen_maze = self.generator.generate(10, 10)

        for row in gen_maze.maze:
            for cell in row:
                self.assertNotEqual(cell, MazeCellStates.NO_OPEN)
