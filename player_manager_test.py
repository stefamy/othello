from player_manager import PlayerManager
from game_controller import GameController
from board import Board

# Tests the (non-display) functionality in the PlayerManager class module.

COMPUTER = -1
HUMAN = 1

MORE_DIFFICULT = True
GRID_COL_ROW_COUNT = 8
CELL_W_H = 100
STROKE_WEIGHT = 2
STROKE_OFFSET = 1
WIDTH = HEIGHT = int((GRID_COL_ROW_COUNT * CELL_W_H) -
                     (STROKE_WEIGHT * STROKE_WEIGHT))


def test_constructor():
    """Test the PlayerManager __init__ function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    pm = PlayerManager(board, gc, MORE_DIFFICULT)

    assert pm.board is board
    assert pm.gc is gc
    assert pm.more_difficult is True
    assert pm.player_turn == HUMAN
    assert pm.player_turn != COMPUTER
    assert len(pm.legal_moves) == 4


def test_humanMove():
    """Test the PlayerManager humanMove() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    pm = PlayerManager(board, gc, MORE_DIFFICULT)

    pm.humanMove(15, 15)
    assert board.grid[(1, 1)].piece is None
    pm.humanMove(200, 300)
    assert board.grid[(3, 3)].piece is None
    assert board.grid[(2, 3)].piece is None
    assert board.grid[(3, 4)].piece is not None
    assert board.grid[(3, 4)].piece.player == HUMAN


def test_computerMove():
    """Test the PlayerManager computerMove() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    pm = PlayerManager(board, gc, MORE_DIFFICULT)

    assert gc.computer_score == 0

    pm.humanMove(200, 300)

    assert gc.computer_score == 1
    assert gc.human_score == 4

    pm.computerMove()

    assert gc.computer_score == 3
    assert gc.human_score == 3


def test_switchPlayer():
    """Test the PlayerManager switchPlayer() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    pm = PlayerManager(board, gc, MORE_DIFFICULT)

    assert pm.player_turn == HUMAN
    assert pm.player_turn != COMPUTER

    pm.switchPlayer()

    assert pm.player_turn == COMPUTER
    assert pm.player_turn != HUMAN

    pm.switchPlayer()

    assert pm.player_turn != COMPUTER
    assert pm.player_turn == HUMAN
