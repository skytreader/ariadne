from ..errors import CantTearWallException
from ..mazes import Maze, MazeCellStates

import unittest

class MazeTest(unittest.TestCase):
    
    def setUp(self):
        self.test_maze4 = Maze(4, 4)
        self.test_maze3 = Maze(3, 3)
        self.rect_maze = Maze(4, 3)

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
        raw_target = """ _ _ _
|_|_|_|
|_|_|_|
|_|_|_|""".rstrip()
        self.assertEqual(raw_target, str(self.test_maze3))
        target = """ _ _ _
| |_  |
| | | |
|_ _ _|""".rstrip()

        self.test_maze3.tear_down_wall(0, 0, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(0, 2, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(1, 0, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(0, 1, MazeCellStates.OPEN_EAST)
        self.test_maze3.tear_down_wall(1, 1, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(1, 2, MazeCellStates.OPEN_SOUTH)
        self.test_maze3.tear_down_wall(2, 1, MazeCellStates.OPEN_EAST_WEST)

        self.test_maze3.tear_down_wall(1, 2, MazeCellStates.OPEN_SOUTH)
        self.assertEqual(target, str(self.test_maze3))

    def test_move_to_opening(self):
        move_north_11 = self.rect_maze.move_to_opening(1, 1, MazeCellStates.OPEN_NORTH)
        self.assertEqual(set([(0, 1)]), move_north_11)

        move_northwest_11 = self.rect_maze.move_to_opening(1, 1, MazeCellStates.OPEN_NORTH_WEST)
        self.assertEqual(set([(0, 1), (1, 0)]), move_northwest_11)

        self.assertRaises(CantTearWallException, self.rect_maze.move_to_opening, 0,
          1, MazeCellStates.OPEN_NORTH)

    def test_eq(self):
        three = Maze(3, 3)
        self.assertEqual(three, self.test_maze3)
        self.assertNotEqual(three, self.test_maze4)
        three.tear_down_wall(0, 0, MazeCellStates.OPEN_EAST)
        self.assertNotEqual(three, self.test_maze3)

if __name__ == "__main__":
    unittest.main()
