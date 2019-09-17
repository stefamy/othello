from game_controller import GameController
from board import Board

# Tests the (non-display) functionality in the Board cell module.

COMPUTER = -1
HUMAN = 1

GRID_COL_ROW_COUNT = 8
CELL_W_H = 100
STROKE_WEIGHT = 2
STROKE_OFFSET = 1
WIDTH = HEIGHT = int((GRID_COL_ROW_COUNT * CELL_W_H) -
                     (STROKE_WEIGHT * STROKE_WEIGHT))


def test_constructor():
    """Test the Board __init__ function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)

    assert board.GRID_COL_ROW_COUNT == GRID_COL_ROW_COUNT
    assert board.CELL_W_H == CELL_W_H
    assert board.WIDTH == WIDTH
    assert board.HEIGHT == HEIGHT
    assert board.WIDTH == board.HEIGHT
    assert board.gc is gc
    assert board.grid is not None
    assert type(board.grid) == dict
    assert board.grid[(1, 1)].piece is None
    assert board.grid[(4, 4)].piece is not None


def test_buildGrid():
    """Test the Board buildGrid() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    assert len(board.grid) == GRID_COL_ROW_COUNT * GRID_COL_ROW_COUNT
    assert board.grid[(1, 1)].location == (1, 1)
    assert board.grid[(1, 1)].piece is None
    assert board.grid[(1, 1)].width == CELL_W_H
    assert board.grid[(1, 1)].x == -2
    assert board.grid[(1, 1)].y == -2
    assert board.grid[(4, 4)].location == (4, 4)
    assert board.grid[(4, 4)].piece is not None
    assert board.grid[(4, 4)].width == CELL_W_H
    assert board.grid[(4, 4)].x == 298
    assert board.grid[(4, 4)].y == 298
    assert (8, 8) in board.grid
    assert (7, 7) in board.grid
    assert (6, 6) in board.grid
    assert (8, 9) not in board.grid
    assert (0, 0) not in board.grid
    assert (-1, 0) not in board.grid


def test_setStarterPieces():
    """Test the Board setStarterPieces() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)
    assert board.grid[(3, 3)].piece is None
    assert board.grid[(4, 4)].piece is not None
    assert board.grid[(4, 5)].piece is not None
    assert board.grid[(4, 4)].piece.player == COMPUTER
    assert board.grid[(4, 5)].piece.player == HUMAN
    assert board.grid[(5, 4)].piece.player == HUMAN
    assert board.grid[(5, 5)].piece.player == COMPUTER
    assert board.grid[(6, 4)].piece is None


def test_addPiece():
    """Test the Board addPiece() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)

    assert board.grid[(4, 4)].piece.player == COMPUTER
    assert board.grid[(4, 3)].piece is None

    board.addPiece(4, 3, HUMAN)
    assert board.grid[(4, 3)].piece is not None
    assert board.grid[(4, 3)].piece.player == HUMAN
    assert board.grid[(4, 4)].piece.player == HUMAN
    assert board.grid[(5, 5)].piece.player == COMPUTER


def test_legalMoves():
    """Test the Board legalMoves() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)

    assert len(board.legalMoves(HUMAN)) == 4
    assert (3, 4) in board.legalMoves(HUMAN)
    assert (5, 6) in board.legalMoves(HUMAN)
    assert (4, 4) not in board.legalMoves(HUMAN)
    assert (6, 6) not in board.legalMoves(HUMAN)
    assert (-1, -1) not in board.legalMoves(HUMAN)


def test_checkNeighborLine():
    """Test the Board checkNeighborLine() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)

    neighbors = board.checkNeighborLine(board.grid[(4, 3)], (-1, 0), HUMAN)
    assert neighbors is None
    neighbors_2 = board.checkNeighborLine(board.grid[(4, 3)], (0, 1), HUMAN)
    assert neighbors_2 is not None
    assert board.grid[(4, 4)] in neighbors_2
    assert board.grid[(4, 3)] not in neighbors_2
    assert board.grid[(4, 2)] not in neighbors_2
    assert board.grid[(4, 5)] not in neighbors_2
    assert board.grid[(3, 4)] not in neighbors_2
    neighbors_3 = board.checkNeighborLine(board.grid[(5, 6)], (0, 1), COMPUTER)
    neighbors_4 = board.checkNeighborLine(board.grid[(5, 6)], (1, 1), COMPUTER)
    neighbors_5 = board.checkNeighborLine(board.grid[(5, 6)], (-1, 1),
                                          COMPUTER)
    assert neighbors_3 is None
    assert neighbors_4 is None
    assert neighbors_5 is None


def test_calcCurrentScores():
    """Test the Board calcCurrentScores() function"""
    gc = GameController(WIDTH, HEIGHT)
    board = Board(GRID_COL_ROW_COUNT, CELL_W_H,
                  WIDTH, HEIGHT, gc)

    gc.human_score == 0
    gc.computer_score == 0

    board.calcCurrentScores()

    gc.human_score == 2
    gc.computer_score == 2

    board.addPiece(4, 3, HUMAN)

    gc.human_score == 4
    gc.computer_score == 1
