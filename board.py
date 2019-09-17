from piece import Piece
from cell import Cell

# The board for Othello, consisting of individual cells (and their pieces).

# Players
COMPUTER = -1
HUMAN = 1

# Counting & math
INCREMENT_ONE = 1
START_AT_ZERO = 0
START_AT_ONE = 1
HALVE_IT = 2
COL_INDEX = 0
ROW_INDEX = 1

# Colors & styling
GREEN_TEXT = 0xFF00cc66
RED_TEXT = 0xFFf7182e
BLACK_RGB = 0
SEE_THROUGH = 220
WHITE_RGB = 255
OPAQUE = 255
STROKE_WEIGHT = 2

# Player status settings
PLAYERSTATUS_TEXT_SIZE = 20
PLAYERSTATUS_HEIGHT = 50
PLAYERSTATUS_TEXT_OFFSET = 30

# All cardinal directions from a single cell
ALL_DIRECTIONS = [(-1, 1), (0, 1), (1, 1),  # Lowers
                  (-1, 0), (1, 0),  # Adjacents
                  (-1, -1), (0, -1), (1, -1)]  # Uppers


class Board:
    """The Othello game board. Generates a grid of cells and starter pieces
    based on game settings. After each valid move, updates state of board and
    alternates current player. Updates game controller when board is full."""
    def __init__(self, GRID_COL_ROW_COUNT, CELL_W_H,
                 WIDTH, HEIGHT, game_controller):
        """Given the total column and row counts, cell width and heights,
        width and height of the window, and game_controller object, creates
        an instance of the Board class with associated attributes."""
        self.GRID_COL_ROW_COUNT = GRID_COL_ROW_COUNT
        self.CELL_W_H = CELL_W_H
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.gc = game_controller
        self.grid = self.buildGrid()
        # Once the board is created, set it with starter pieces.
        self.setStarterPieces()

    def buildGrid(self):
        """Given the column/row count, returns a dict of (column, row)
        keys with Cell objects as their values."""
        # Generate a list of (column, row) tuples based on the game settings.
        rows = columns = [i for i in range(START_AT_ONE,
                                           self.GRID_COL_ROW_COUNT +
                                           INCREMENT_ONE)]
        grid = {}
        for column in columns:
            for row in rows:
                # Create a cell at every (column, row) location
                grid[(column, row)] = (Cell(column, row, self.CELL_W_H))

        return grid

    def setStarterPieces(self):
        """Add 4 starter pieces to center of the board (or close to it for
        odd-sized grids), while alternating the assigned player."""

        # Calculate the piece's positioning based on grid attributes.
        half_grid_size = self.GRID_COL_ROW_COUNT / int(HALVE_IT)
        start = half_grid_size
        end = start + INCREMENT_ONE
        temp_player_turn = HUMAN

        # Add all piece locations to a list for iteration.
        starter_pieces = [(start, end), (start, start),
                          (end, start), (end, end)]

        for coordinates in starter_pieces:
            cell = self.grid[(coordinates[COL_INDEX], coordinates[ROW_INDEX])]
            cell.piece = Piece(cell.x, cell.y, self.CELL_W_H, temp_player_turn)
            # Change player manually rather than through the method,
            # since we don't need to check if there are moves left.
            temp_player_turn = -temp_player_turn

    def addPiece(self, column, row, player_turn):
        """Called from PlayerManager after a valid move is selected. Given a
        column and row location and the current player, add a piece for that
        player to the appropriate cell and flip any pieces as necessary."""

        new_cell = self.grid[(column, row)]

        # Flip any pieces that need flipping.
        for flipper_cell in self.legalMoves(player_turn)[new_cell.location]:
            flipper_cell.piece.player = player_turn

        # Add the piece to the board at the cell location.
        new_cell.piece = Piece(new_cell.x, new_cell.y,
                               new_cell.width, player_turn)

        # Update the scores.
        self.calcCurrentScores()

    def legalMoves(self, player_turn):
        """Given a current player, generate all the legal moves available for
        that player (and the resulting flips) and return them in a dict."""

        moves_and_flips = {}
        # Checking every open cell in the grid:
        for location, cell in self.grid.items():
            if cell.piece is None:
                # For each empty cell, check cells in all directions from it.
                for direction in ALL_DIRECTIONS:
                    next_in_line = cell.neighbor(direction)
                    # Ensure we're still on the board
                    if next_in_line in self.grid:
                        next_in_line = self.grid[next_in_line]
                        # Check if the empty cell neighbor has a piece.
                        if next_in_line.piece is not None:
                            # Check if it belongs to the other player.
                            if next_in_line.piece.player != player_turn:
                                # It is the opposite, so check all
                                # neighbors in that same direction.
                                pieces_to_flip = \
                                    self.checkNeighborLine(next_in_line,
                                                           direction,
                                                           player_turn)
                                # It returned cells, so this is a valid move!
                                if pieces_to_flip is not None:
                                    pieces_to_flip.add(next_in_line)
                                    # Add a new cell to the valid moves.
                                    if cell.location in moves_and_flips.keys():
                                        moves_and_flips[cell.location] \
                                            .update(pieces_to_flip)
                                    # Or, update an existing cell location.
                                    else:
                                        moves_and_flips[cell.location] \
                                            = pieces_to_flip
        return moves_and_flips

    def checkNeighborLine(self, start_cell, direction, player_turn):
        """Given a cell location, a direction (as a tuple of col/row coordinates)
        and a player_turn, return the set of cells to have pieces flipped if a
        piece was added there. If not a valid move, return None."""
        checking = True
        cells_to_flip = set()

        while checking:
            # Check the next cell out from the current location:
            next_in_line = start_cell.neighbor(direction)
            if next_in_line in self.grid:
                next_in_line = self.grid[next_in_line]
                # Check #1, does it have a piece to flip?
                if next_in_line.piece is not None:
                    # Check #2, does it belong to the opposite player?
                    if next_in_line.piece.player != player_turn:
                        # It does, so keep checking down the line.
                        cells_to_flip.add(next_in_line)
                        start_cell = next_in_line
                    else:
                        # It doesn't, so it must be our "end" piece.
                        return cells_to_flip
                else:
                    checking = False
            else:
                checking = False
        else:
            # Loop ended without a valid line of flips.
            return None

    def calcCurrentScores(self):
        """Called from self.addPiece() after pieces have been flipped according
        to the latest move. Recalculates the scores for both players."""

        # Reset both scores to zero.
        self.gc.human_score = START_AT_ZERO
        self.gc.computer_score = START_AT_ZERO

        # Tally scores based on current game pieces.
        for location, cell in self.grid.items():
            if cell.piece is not None:
                if cell.piece.player == HUMAN:
                    self.gc.human_score += INCREMENT_ONE
                else:
                    self.gc.computer_score += INCREMENT_ONE

    def playerStatus(self, player_turn):
        """Called from update() in the PlayerManager. Given the current
        player, display whose turn it is in the bottom of the window."""
        textSize(PLAYERSTATUS_TEXT_SIZE)
        textAlign(CENTER)
        if player_turn == COMPUTER:
            fill(RED_TEXT)
            textSize(PLAYERSTATUS_TEXT_SIZE)
            text("Computer's move...", self.WIDTH/HALVE_IT,
                 self.HEIGHT+PLAYERSTATUS_TEXT_OFFSET)
        else:
            fill(GREEN_TEXT)
            text("Your move.", self.WIDTH/HALVE_IT,
                 self.HEIGHT+PLAYERSTATUS_TEXT_OFFSET)

    def display(self):
        """Called from draw(), makes the necessary per-frame updates to board
        (displays the cells and draws the background for the player status)."""
        for cell in self.grid.keys():
            self.grid[cell].display()

        # Background for current player area
        fill(BLACK_RGB)
        rect(START_AT_ZERO, self.HEIGHT, self.WIDTH, PLAYERSTATUS_HEIGHT)
