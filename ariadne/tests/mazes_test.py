from ..errors import CantTearWallException
from ..mazes import Maze, MazeCellStates

import unittest

class MazeTest(unittest.TestCase):
    
    def setUp(self):
        self.maze = Maze(4, 4)

    def test_set_cell_state(self):
        self.maze.set_cell_state(2, 2, MazeCellStates.OPEN_WEST)
        self.assertEqual(self.maze.maze[2][2], MazeCellStates.OPEN_WEST)

        self.maze.set_cell_state(2, 2, MazeCellStates.OPEN_SOUTH)
        self.assertEqual(self.maze.maze[3][2], MazeCellStates.OPEN_NORTH)
        self.assertEqual(self.maze.maze[2][2], MazeCellStates.OPEN_SOUTH_WEST)
        
        self.maze.set_cell_state(2, 2, MazeCellStates.NO_OPEN)
        self.assertEqual(self.maze.maze[2][2], MazeCellStates.OPEN_SOUTH_WEST)

    def test_set_cell_state_validations(self):
        self.assertRaises(CantTearWallException, self.maze.set_cell_state, 0, 1,
          MazeCellStates.OPEN_NORTH)
        self.assertRaises(CantTearWallException, self.maze.set_cell_state, 1, 3,
          MazeCellStates.OPEN_EAST)
        self.assertRaises(CantTearWallException, self.maze.set_cell_state, 3, 1,
          MazeCellStates.OPEN_SOUTH)
        self.assertRaises(CantTearWallException, self.maze.set_cell_state, 1, 0,
          MazeCellStates.OPEN_WEST)


if __name__ == "__main__":
    unittest.main()
