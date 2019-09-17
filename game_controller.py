# Othello game controller. Maintains the state of the
# game, including each player's final score.

# Counting & math
START_AT_ZERO = 0
HALVE_IT = 2

# Colors & styling
BLACK_RGB = 0
SEE_THROUGH = 220
WHITE_RGB = 255
OPAQUE = 255
SMALL_TEXT = 20
BIG_TEXT = 40

# Positioning
LEFT_X = 0
TOP_Y = 0

# Player status settings
PLAYERSTATUS_HEIGHT = 50


class GameController:
    """The class representing the GameController object. Maintains
    the state of the game, including each player's final score."""
    def __init__(self, WIDTH, HEIGHT):
        """Passed a width and height of the game window, creates
        the GameController object and associated attributes."""
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.human_score = START_AT_ZERO
        self.computer_score = START_AT_ZERO
        self.game_over = False
        self.human_wins = False
        self.computer_wins = False
        self.tied_game = False

    def update(self):
        """Called from draw(). Runs appropriate methods if the
        game is over."""
        if self.game_over:
            self.determineWinner()
            self.printResult()

    def determineWinner(self):
        """Called from self.update() if self.game_over = True.
        Sets the winner attribute based on scores at the time
        the method is run."""

        # Human won.
        if self.human_score > self.computer_score:
            self.human_wins = True
            # (Reset these to False, just in case.)
            self.computer_wins = self.tied_game = False

        # Computer won.
        elif self.computer_score > self.human_score:
            self.computer_wins = True
            self.human_wins = self.tied_game = False

        # Neither, so it must be tied.
        else:
            self.tied_game = True
            self.computer_wins = self.human_wins = False

    def printResult(self):
        """Called from self.update() if self.game_over = True.
        Displays game winner and final scores to the board."""

        # Cover board with overlay.
        fill(BLACK_RGB, SEE_THROUGH)
        rect(LEFT_X, TOP_Y, self.WIDTH, self.HEIGHT + PLAYERSTATUS_HEIGHT)
        fill(WHITE_RGB, OPAQUE)
        textAlign(CENTER)

        # Set text variables based on winner and scores
        if self.human_wins:
            winner_text = "YOU WON!!!!!"
        elif self.computer_wins:
            winner_text = "Aw, you lost."
        else:
            winner_text = "It's a tie."
        scores_text = '------------' \
                      '\nFinal Scores:' + \
                      '\nYou: ' + str(self.human_score) + \
                      '\nComputer: ' + str(self.computer_score)

        # Print the text.
        textSize(BIG_TEXT)
        text(winner_text, self.WIDTH/HALVE_IT, self.HEIGHT/HALVE_IT)
        textSize(SMALL_TEXT)
        text(scores_text, self.WIDTH/HALVE_IT, self.HEIGHT/HALVE_IT + 50)

    def inputScores(self, player_name):
        """Given a string input as a player name, writes the name and
        player's score to the scores.txt file. If it's a new top score,
        add it to the top of the file. Else, add it to the bottom."""

        scores_file_text = player_name + ' ' + str(self.human_score) + '\n'

        f = open('scores.txt', 'r')
        top_place = f.readline()

        # Does the file have existing entries?
        if top_place != '':
            current_high_score = int(top_place.split(' ')[-1])

            # Is this score the new high score?
            if self.human_score > current_high_score:
                scores_file_text += top_place
                existing_entries = f.readlines()
                for entry in existing_entries:
                    scores_file_text += entry
                    f.close()
                f = open("scores.txt", "w")
            # Not a high score, so just append it.
            else:
                f = open("scores.txt", "a")
        # No existing scores, so just append it.
        else:
            f = open("scores.txt", "a")

        f.write(scores_file_text)
        f.close
