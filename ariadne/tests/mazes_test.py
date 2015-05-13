from ..errors import CantTearWallException
from ..mazes import Maze, MazeCellStates

import unittest

class MazeTest(unittest.TestCase):
    
    def setUp(self):
        self.test_maze4 = Maze(4, 4)
        self.test_maze3 = Maze(3, 3)

    def test_tear_down_wall(self):
        self.test_maze4.tear_down_wall(2, 2, MazeCellStates.OPEN_WEST)
        self.assertEqual(self.test_maze4.maze[2][2], MazeCellStates.OPEN_WEST)

        self.test_maze4.tear_down_wall(2, 2, MazeCellStates.OPEN_SOUTH)
        self.assertEqual(self.test_maze4.maze[3][2], MazeCellStates.OPEN_NORTH)
        self.assertEqual(self.test_maze4.maze[2][2], MazeCellStates.OPEN_SOUTH_WEST)
        
        self.test_maze4.tear_down_wall(2, 2, MazeCellStates.NO_OPEN)
        self.assertEqual(self.test_maze4.maze[2][2], MazeCellStates.OPEN_SOUTH_WEST)

    def test_tear_down_wall_validations(self):
        self.assertRaises(CantTearWallException, self.test_maze4.tear_down_wall, 0, 1,
          MazeCellStates.OPEN_NORTH)
        self.assertRaises(CantTearWallException, self.test_maze4.tear_down_wall, 1, 3,
          MazeCellStates.OPEN_EAST)
        self.assertRaises(CantTearWallException, self.test_maze4.tear_down_wall, 3, 1,
          MazeCellStates.OPEN_SOUTH)
        self.assertRaises(CantTearWallException, self.test_maze4.tear_down_wall, 1, 0,
          MazeCellStates.OPEN_WEST)

    def test_str(self):
        target = """
 _ _ _ 
| |_  |
| | | |
|_ _ _|"""

        target = target.strip()
        self.test_maze3.tear_down_wall(0, 0, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(1, 0, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(0, 1, MazeCellStates.OPEN_EAST)
        self.test_maze3.tear_down_wall(1, 1, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(1, 2, MazeCellStates.OPEN_SOUTH)


if __name__ == "__main__":
    unittest.main()
