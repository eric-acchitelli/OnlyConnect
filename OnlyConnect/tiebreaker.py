from OnlyConnect import RoundBase, vowelsPuzzle
from cs50 import get_string


class Tiebreaker(RoundBase):
    def play(self, teams):
        response = ""
        BUTTON_OPTIONS = [(f"{teams[0]['name']} correct").upper(), (f"{teams[1]['name']} correct").upper(),
                          (f"{teams[0]['name']} incorrect").upper(), (f"{teams[1]['name']} incorrect").upper()]
        for set in self.puzzles:
            for clue in self.puzzles[set].clues:
                print(f"{self.puzzles[set].connection}")
                print(f"-----{vowelsPuzzle(str(clue))}")
                while response not in BUTTON_OPTIONS:
                    response = get_string(f"{BUTTON_OPTIONS} ").upper()
                    if response == f"{teams[0]['name']} correct".upper():
                        teams[0]['score'] += 1
                        response = ""
                        break
                    elif response == f"{teams[1]['name']} correct".upper():
                        teams[1]['score'] += 1
                        response = ""
                        break
                    elif response == f"{teams[0]['name']} incorrect".upper():
                        if teams[0]['score'] > 0:
                            teams[0]['score'] -= 1
                        response = ""
                        break
                    elif response == f"{teams[1]['name']} incorrect".upper():
                        if teams[1]['score'] > 0:
                            teams[1]['score'] -= 1
                        response = ""
                        break
                print(f"----------{clue}")