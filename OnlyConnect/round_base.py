from OnlyConnect import Puzzle

class RoundBase:
    def __init__(self, questions):
        self.puzzles = {}
        for hieroglyph, puzzle in questions.items():
            self.puzzles[hieroglyph] = Puzzle(puzzle)

    def play():
        pass