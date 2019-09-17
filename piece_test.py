from piece import Piece

# Tests the (non-display) functionality in the Piece class module.

CELL_PIECE_SIZE_DIFF = 20
HALVE_IT = 2
COMPUTER = 1
HUMAN = -1


def test_constructor():
    """Test the Piece __init__ function"""
    # Test #1
    p1 = Piece(-2, -2, 100, 1)
    assert p1.x == 48
    assert p1.y == 48
    assert p1.size == 90
    assert p1.player == COMPUTER

    # Test #2
    p2 = Piece(397, 197, 200, -1)
    assert p2.x == 497
    assert p2.y == 297
    assert p2.size == 190
    assert p2.player == HUMAN
