from .errors import CantTearWallException

class MazeCellStates(object):
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

    """
    Maps the cell states above to a textual description
    """
    LABELS = {
        NO_OPEN: "NO_OPEN",
        OPEN_WEST: "OPEN_WEST",
        OPEN_SOUTH: "OPEN_SOUTH",
        OPEN_SOUTH_WEST: "OPEN_SOUTH_WEST",
        OPEN_EAST: "OPEN_EAST",
        OPEN_EAST_WEST: "OPEN_EAST_WEST",
        OPEN_EAST_SOUTH_WEST: "OPEN_EAST_SOUTH_WEST",
        OPEN_NORTH: "OPEN_NORTH",
        OPEN_NORTH_WEST: "OPEN_NORTH_WEST",
        OPEN_NORTH_SOUTH: "OPEN_NORTH_SOUTH",
        OPEN_NORTH_SOUTH_WEST: "OPEN_NORTH_SOUTH_WEST",
        OPEN_NORTH_EAST: "OPEN_NORTH_EAST",
        OPEN_NORTH_EAST_WEST: "OPEN_NORTH_EAST_WEST",
        OPEN_NORTH_EAST_SOUTH: "OPEN_NORTH_EAST_SOUTH",
        OPEN_NORTH_EAST_SOUTH_WEST: "OPEN_NORTH_EAST_SOUTH_WEST"
    }
    
    """
    A mapping that tells you what to tear down in adjacent cells when you tear
    down walls for a given cell.
    """
    INVERSES = {
        OPEN_WEST: OPEN_EAST,
        OPEN_EAST: OPEN_WEST,
        OPEN_NORTH: OPEN_SOUTH,
        OPEN_SOUTH: OPEN_NORTH,
    }


class Maze(object):
    
    def __init__(self, width, height, initial_state=MazeCellStates.NO_OPEN):
        self.maze = [[initial_state for _ in range(width)] for __ in range(height)]
    
    def __set_cell_state(self, row, col, cell_state):
        will_open_north = (cell_state & MazeCellStates.OPEN_NORTH) == MazeCellStates.OPEN_NORTH
        will_open_east = (cell_state & MazeCellStates.OPEN_EAST) == MazeCellStates.OPEN_EAST
        will_open_south = (cell_state & MazeCellStates.OPEN_SOUTH) == MazeCellStates.OPEN_SOUTH
        will_open_west = (cell_state & MazeCellStates.OPEN_WEST) == MazeCellStates.OPEN_WEST
        cant_tear = CantTearWallException(row, col, cell_state)

        if row == 0 and will_open_north:
            raise cant_tear
        elif col == 0 and will_open_west:
            raise cant_tear
        elif row == len(self.maze) - 1 and will_open_south:
            raise cant_tear
        elif col == len(self.maze[0]) - 1 and will_open_east:
            raise cant_tear
        
        self.maze[row][col] = self.maze[row][col] | cell_state

    def tear_down_wall(self, row, col, cell_state):
        """
        Remove a wall in the given cell so that it, at least, "resembles" the
        specified cell_state (do read next paragraph).

        The effects of this method is cumulative. That is, if in one call you
        OPEN_WEST for a given cell, then in another call you OPEN_SOUTH in the
        same cell, the effect is as if you made one call to OPEN_SOUTH_WEST. It
        also affects adjacent cells to ensure that the openings are bidirectional.

        Note that this cannot be used to undo removed walls.

        row - integer index
        col - integer index
        cell state - preferrably as enumerated in MazeCellStates
        """
        
        self.__set_cell_state(row, col, cell_state)
        will_open_north = (cell_state & MazeCellStates.OPEN_NORTH) == MazeCellStates.OPEN_NORTH
        will_open_east = (cell_state & MazeCellStates.OPEN_EAST) == MazeCellStates.OPEN_EAST
        will_open_south = (cell_state & MazeCellStates.OPEN_SOUTH) == MazeCellStates.OPEN_SOUTH
        will_open_west = (cell_state & MazeCellStates.OPEN_WEST) == MazeCellStates.OPEN_WEST

        if will_open_north:
            self.__set_cell_state(row - 1, col, MazeCellStates.OPEN_SOUTH)

        if will_open_east:
            self.__set_cell_state(row, col + 1, MazeCellStates.OPEN_WEST)

        if will_open_south:
            self.__set_cell_state(row + 1, col, MazeCellStates.OPEN_NORTH)

        if will_open_west:
            self.__set_cell_state(row, col - 1, MazeCellStates.OPEN_EAST)

    def __str__(self):
        build_string = ["".join([" _" for _ in range(len(self.maze) - 1)].push(" "))]
        
        for row in self.maze:
            row_str = []
            for cell in row:
                open_east = (cell & MazeCellStates.OPEN_EAST) == MazeCellStates.OPEN_EAST
                open_south = (cell & MazeCellStates.OPEN_SOUTH) == MazeCellStates.OPEN_SOUTH
                open_west = (cell & MazeCellStates.OPEN_WEST) == MazeCellStates.OPEN_WEST
                
                cell_str = []

                if open_east:
                    cell_str.push(" ")
                else:
                    cell_str.push("|")

                if open_south:
                    cell_str.push(" ")
                else:
                    cell_str.push("_")

                if open_west:
                    cell_str.push(" ")
                else:
                    cell_str.push("|")

                row_str.push("".join(cell_str))

            build_string.push("".join(row_str))
        
        return "\\n".join(build_string)
