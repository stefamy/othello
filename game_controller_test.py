from game_controller import GameController

# Tests the (non-display) functionality in the GameController class module.

WIDTH = 400
HEIGHT = 400


def test_constructor():
    """Test the GameController _init__ function"""
    gc = GameController(WIDTH, HEIGHT)

    assert gc.WIDTH == 400
    assert gc.HEIGHT == 400
    assert gc.human_score == 0
    assert gc.computer_score == 0
    assert gc.game_over is not True
    assert gc.human_wins is False
    assert gc.computer_wins is False
    assert gc.game_over is False
    assert gc.tied_game is False


def test_determineWinner():
    """Test the GameController determineWinner() function"""
    gc = GameController(400, 400)
    gc.human_score = 50
    gc.computer_score = 20
    gc.determineWinner()

    assert gc.human_wins is True
    assert gc.computer_wins is False
    assert gc.tied_game is False

    gc.computer_score = 50
    gc.determineWinner()
    assert gc.human_wins is False
    assert gc.computer_wins is False
    assert gc.tied_game is True
