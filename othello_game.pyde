from board import Board
from game_controller import GameController
from player_manager import PlayerManager

# The main file for Othello game application.
# ------------------------------------------
# HW 12, CS 5001
# Othello Part 2.1
# Amy Stefani
# ------------------------------------------

#  ------------- Game Settings -------------
#   Board size and appearance can be determined by
#   changing these values before running the game.
GRID_COL_ROW_COUNT = 8
CELL_W_H = 80
BOARD_BG = 0x00cc66  # Green
MORE_DIFFICULT = True
#  ----------- END Game Settings -----------

# Constants - Do not change.
STROKE_WEIGHT = 2
STROKE_OFFSET = 1
INCREMENT_ONE = 1
WIDTH = HEIGHT = int((GRID_COL_ROW_COUNT * CELL_W_H) -
                     (STROKE_WEIGHT * STROKE_OFFSET))
COMPUTER = -1
HUMAN = 1
SCOREBOARD_HEIGHT = 50

# Initialize
start_time = 0


# Instantiate game controller and board using game settings.
gc = GameController(WIDTH, HEIGHT)
board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
              WIDTH, HEIGHT, gc)
pm = PlayerManager(board, gc, MORE_DIFFICULT)


def setup():
    """Set up the canvas with width and height
    as determined by game settings."""
    size(WIDTH, HEIGHT + SCOREBOARD_HEIGHT)


def draw():
    """Frame by frame refresh of board and game controller."""
    background(BOARD_BG)
    board.display()

    if gc.game_over is False:
        pm.update(start_time)
        gc.update()
    else:
        saveScore()


def mouseClicked():
    """Run the Board's makeMove method upon user mouse click."""
    if pm.player_turn == HUMAN:
        pm.humanMove(mouseX, mouseY)

        # Reset timer.
        global start_time
        start_time = second()


def input(message=''):
    """A helper function to mimic python's built in input() function.
    Accepts a string input from the user. Returns the input."""
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)


def saveScore():
    """Request the name for scores file and pass it to the game
    controller to add the score. Then end the draw() loop."""

    player_name = input('Enter your name for the scoreboard.')

    if player_name:
        gc.inputScores(player_name)
    else:
        gc.inputScores('Anonymous player')

    noLoop()
