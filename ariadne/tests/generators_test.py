from ..mazes import Maze, MazeCellStates
from ..generators import RecursiveBacktracker, EllersAlgorithm

import unittest

class RecursiveBacktrackerTest(unittest.TestCase):
    """
    Some shallow tests for the generator.

    Just makes sure that all cells have been carved and that the generated maze
    is up to spec.

    # Using this as master class for testing other generators.

    Just override `setUp` and make sure `self.generator` points to an instance
    of the generator you want to test.
    """

    def setUp(self):
        self.generator = RecursiveBacktracker()
    
    def test_generate(self):
        gen_maze = self.generator.generate(100, 100)

        for row in gen_maze.maze:
            for cell in row:
                self.assertNotEqual(cell, MazeCellStates.NO_OPEN)

        gen_maze = self.generator.generate(2, 3)

        for row in gen_maze.maze:
            self.assertEqual(len(row), 2)
            for cell in row:
                self.assertNotEqual(cell, MazeCellStates.NO_OPEN)

        self.assertEqual(len(gen_maze.maze), 3)


class EllersAlgorithmTest(RecursiveBacktrackerTest):
    
    def setUp(self):
        self.generator = EllersAlgorithm()
