import json
from typing import Dict
from OnlyConnectDir import Puzzle
from OnlyConnectDir import Connection, Sequences, MissingVowels, ConnectingWall, Tiebreaker


class OnlyConnect:

    def __init__(self, file: str):
        with open(file) as gameFile:
            temp: Dict = json.load(gameFile)
        self.game: Dict[str, Dict[str, Puzzle]] = {}

        # Iterate through the question file for each found and create objects with the class matching the round.
        for roundIndex, round_ in enumerate(temp):
            if roundIndex == 0:
                self.round1 = Connection(temp[round_])
            elif roundIndex == 1:
                self.round2 = Sequences(temp[round_])
            elif roundIndex == 2:
                self.round3 = ConnectingWall(temp[round_])
            elif roundIndex == 3:
                self.round4 = MissingVowels(temp[round_])
            elif roundIndex == 4:
                self.tiebreaker = Tiebreaker(temp[round_])


