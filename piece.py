# The class representing a single game piece at a set location
# on the board. Each cell has an assigned player (that may change
# during gameplay) which determines its dislay color.

# Players
HUMAN = 1
COMPUTER = -1

# Counting & math
CELL_PIECE_SIZE_DIFF = 10
HALVE_IT = 2

# Colors & styling
BLACK_RGB = 0
WHITE_RGB = 255
STROKE_WEIGHT = 2


class Piece:
    """A single game piece belonging to a specific cell on the game board. Each
    game piece belongs to a certain player, which determines its fill color."""
    def __init__(self, cell_x, cell_y, cell_size, player):
        self.x = cell_x + (cell_size // HALVE_IT)
        self.y = cell_y + (cell_size // HALVE_IT)
        self.size = cell_size - CELL_PIECE_SIZE_DIFF
        self.player = player

    def display(self):
        """Draws the game piece at the appropriate x, y location and with
        the appropriate fill color based on its player attribute."""
        stroke(BLACK_RGB)
        strokeWeight(STROKE_WEIGHT)

        if self.player == HUMAN:
            fill(BLACK_RGB)
        elif self.player == COMPUTER:
            fill(WHITE_RGB)

        ellipse(self.x, self.y, self.size, self.size)
