from cell import Cell
from math import ceil
from random import sample

# A class representing the PlayerManager object, which controls
# each player's moves and handles switching of the current player.

NONE = 0
COLUMN_INDEX = 0
ROW_INDEX = 1
PICK_ONE = 1
FIRST_INDEX = 0
INCREMENT_ONE = 1
TIME_DELAY = 1

COMPUTER = -1
HUMAN = 1


class PlayerManager:
    """Initializes the PlayerManager object, which controls each player's
    (human and computer) moves and switching of the current player"""
    def __init__(self, board, game_controller, more_difficult):
        """Given a board object, game controller object, and boolean designating
        it as difficult or not, initializes the PlayerManager object."""
        self.board = board
        self.gc = game_controller
        self.more_difficult = more_difficult
        self.player_turn = HUMAN
        self.legal_moves = self.board.legalMoves(self.player_turn)

    def update(self, start_time):
        """Passed the a time_stamp in seconds and called from draw(). Refreshes
        the board playerStatus, checks if computer should take its turn (with a
        delay), and ends game if no moves are left."""
        self.board.playerStatus(self.player_turn)
        if len(self.legal_moves) > NONE:
            if self.player_turn == COMPUTER:
                if abs(start_time - second()) > TIME_DELAY:
                    self.computerMove()
        else:
            self.gc.game_over = True

    def humanMove(self, mouseX, mouseY):
        """Given mouse x and y location, check if the cell there is empty, and
        if so, add a piece for the current player. Then call switchPlayer()."""

        column = int(ceil(mouseX/self.board.CELL_W_H) + INCREMENT_ONE)
        row = int(ceil(mouseY/self.board.CELL_W_H) + INCREMENT_ONE)

        # Check if it's a valid move, and make it if so.
        if (column, row) in self.legal_moves.keys():
            self.board.addPiece(column, row, self.player_turn)
            self.switchPlayer()

    def computerMove(self):
        """Runs from self.update() if the player_turn is set as the computer.
        Checks list of legal moves and makes one at random. If difficulty
        level is set, selects the move will result in the most flips."""

        # Pick a random move from the valid moves.
        computer_move = sample(self.legal_moves.keys(), PICK_ONE)[FIRST_INDEX]

        if self.more_difficult is True:
            # Pick the move which results in the most flips:
            for move, flips in self.legal_moves.items():
                if len(flips) > len(self.legal_moves[computer_move]):
                    computer_move = move

        column = computer_move[COLUMN_INDEX]
        row = computer_move[ROW_INDEX]

        # Make the move.
        self.board.addPiece(column, row, self.player_turn)
        self.switchPlayer()

    def switchPlayer(self):
        """Called after humanMove() or computerMove() complete. Checks that
        there are indeed moves left for the next player and switches the
        player. Else, keep player as-is."""

        # Switch the player.
        self.player_turn = -self.player_turn
        self.legal_moves = self.board.legalMoves(self.player_turn)

        # Are there any moves for the new player?
        if len(self.legal_moves) == NONE:
            # No, so switch it back to original player and reset legal moves.
            self.player_turn = -self.player_turn
            self.legal_moves = self.board.legalMoves(self.player_turn)
