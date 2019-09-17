# The class representing a single cell on the game board.
# Each cell may be empty or may possess a game piece.

# Colors & Styling
BLACK_RGB = 0
ACCT_FOR_SELF = 1
STROKE_WEIGHT = 2

# Positioning
COL_INDEX = 0
ROW_INDEX = 1


class Cell:
    """A single cell at a specific x, y location on the game board containing
    either a game piece belonging to a specific player or empty (None)."""
    def __init__(self, column, row, CELL_W_H):
        """Given an integer value representing a column, an integer value
        representing a row, and the cell width/height in pixels, creates
        the Cell object with its associated attributes."""
        self.location = (column, row)
        self.width = self.height = CELL_W_H
        self.x = ((column - ACCT_FOR_SELF) *
                  self.width) - STROKE_WEIGHT
        self.y = ((row - ACCT_FOR_SELF) *
                  self.height) - STROKE_WEIGHT
        self.piece = None

    def display(self):
        """Draws a single cell with a black border at the
        appropriate x, y location on the board."""
        noFill()
        stroke(BLACK_RGB)
        strokeWeight(STROKE_WEIGHT)
        rect(self.x, self.y, self.width, self.height)

        # If the cell contains a game piece, display it as well.
        if self.piece:
            self.piece.display()

    def neighbor(self, direction_coords):
        """Given column, row coordinates as a tuple of two ints (eg, (-1, 0)),
        adds them to this cell's column/row coordinates and returns a tuple."""
        neighbor_col = self.location[COL_INDEX] + direction_coords[COL_INDEX]
        neighbor_row = self.location[ROW_INDEX] + direction_coords[ROW_INDEX]

        return (neighbor_col, neighbor_row)
