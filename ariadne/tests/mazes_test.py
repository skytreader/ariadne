from ..mazes import Maze, MazeCellStates

import unittest

class MazeTest(unittest.TestCase):
    
    def setUp(self):
        self.maze = Maze(4, 4)

    def test_cell_state(self):
        self.maze.set_cell_state(0, 0, MazeCellStates.OPEN_WEST)
        self.assertEqual(self.maze.maze[0][0], MazeCellStates.OPEN_WEST)
        self.maze.set_cell_state(0, 0, MazeCellStates.OPEN_SOUTH)
        self.assertEqual(self.maze.maze[0][1], MazeCellStates.OPEN_NORTH)
        self.assertEqual(self.maze.maze[0][0], MazeCellStates.OPEN_SOUTH_WEST)

if __name__ == "__main__":
    unittest.main()
