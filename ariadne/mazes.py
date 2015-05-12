class MazeCellStates:
    """
    We use a nibble to represent the state of the cell. Each bit in a nibble
    represents the presence or absence of a wall. Specifically, their order
    is (from MSB to LSB) NESW.
    """
    NO_OPEN = 0x0
    OPEN_WEST = 0x1
    OPEN_SOUTH = 0x2
    OPEN_SOUTH_WEST = 0x3
    OPEN_EAST = 0x4
    OPEN_EAST_WEST = 0x5
    OPEN_SOUTH_EAST = 0x6
    OPEN_EAST_SOUTH_WEST = 0x7
    OPEN_NORTH = 0x8
    OPEN_NORTH_WEST = 0x9
    OPEN_NORTH_SOUTH = 0xa
    OPEN_NORTH_SOUTH_WEST = 0xb
    OPEN_NORTH_EAST = 0xc
    OPEN_NORTH_EAST_WEST = 0xd
    OPEN_NORTH_EAST_SOUTH = 0xe
    OPEN_NORTH_EAST_SOUTH_WEST = 0xf

class Maze(object):
    
    def __init__(self, width, height):
        self.maze = [[MazeCellStates.NO_OPEN for _ in range(width)] for __ in range(height)]

    def set_cell_state(self, row, col, cell_state):
        """
        Remove a wall in the given cell so that it, at least, "resembles" the
        specified cell_state (do read next paragraph).

        The effects of this method is cumulative. That is, if in one call you
        OPEN_WEST for a given cell, then in another call you OPEN_SOUTH in the
        same cell, the effect is as if you made one call to OPEN_SOUTH_WEST.

        Note that this cannot be used to undo removed walls.

        row - integer index
        col - integer index
        cell state - preferrably as enumerated in MazeCellStates
        """
        self.maze[row][col] = self.maze[row][col] | cell_state
