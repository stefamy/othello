from cell import Cell
from piece import Piece

# Tests the (non-display) functionality in the Cell class module.


def test_constructor():
    """Test the Cell _init__ function"""
    # Test #1
    c1 = Cell(1, 1, 100)
    assert c1.location == (1, 1)
    assert c1.location[0] == 1
    assert c1.location[1] == 1
    assert c1.width == 100
    assert c1.height == 100
    assert c1.x == -2
    assert c1.y == -2
    assert c1.piece is None

    c1.piece = Piece(c1.x, c1.y, c1.width, 1)
    assert c1.piece is not None
    assert c1.piece.player == 1

    # Test #2
    c2 = Cell(3, 2, 200)
    assert c2.location == (3, 2)
    assert c2.location[0] == 3
    assert c2.location[1] == 2
    assert c2.width == 200
    assert c2.height == 200
    assert c2.x == 398
    assert c2.y == 198
    assert c2.piece is None

    c2.piece = Piece(c2.x, c2.y, c1.width, -1)
    assert c2.piece is not None
    assert c2.piece.player == -1


def test_neighbor():
    """Test the Cell neighbor() function"""
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN_RIGHT = (1, 1)
    HERE = (0, 0)

    c1 = Cell(2, 6, 100)
    c1_up = c1.neighbor(UP)
    c1_left = c1.neighbor(LEFT)
    c1_down_right = c1.neighbor(DOWN_RIGHT)
    c1_here = c1.neighbor(HERE)

    assert c1_up == (2, 5)
    assert c1_up[0] == 2
    assert c1_left == (1, 6)
    assert c1_left[1] == 6
    assert c1_down_right == (3, 7)
    assert c1_here == (2, 6)

    c2 = Cell(4, 2, 200)
    c2_up = c2.neighbor(UP)
    c2_left = c2.neighbor(LEFT)
    c2_down_right = c2.neighbor(DOWN_RIGHT)
    c2_here = c2.neighbor(HERE)

    assert c2_up == (4, 1)
    assert c2_left == (3, 2)
    assert c2_down_right == (5, 3)
    assert c2_here == (4, 2)
