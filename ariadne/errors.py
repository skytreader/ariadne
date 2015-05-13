class CantTearWallException(Exception):
    
    def __init__(self, row, col, cell_state):
        self.row = row
        self.col = col
        self.cell_state = cell_state

    def __str__(self):
        from .mazes import MazeCellState
        return "Can't %s for cell at (%s, %s)" % (MazeCellState.LABELS[self.cell_state],
          self.row, self.col)
