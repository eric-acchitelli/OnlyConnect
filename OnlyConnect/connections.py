import signal
from typing import List, Dict
from cs50 import get_string
from OnlyConnect import RoundBase

class Connection(RoundBase):
    def play(self, teams: List[Dict[str, int]], currentTeam: int):

        # Initialize variables.
        puzzleRequest = ""
        puzzleComplete = 0
        questionChoices = []

        # Collect available hieroglyph choices in one list for players to select from.
        for key in self.puzzles.keys():
            questionChoices.append(str(key))

        # While there are still puzzles to be played, ask the player which puzzle they would like to play. Once selected, all
        # data for that puzzle is initialized
        while puzzleComplete != 6:
            while puzzleRequest not in questionChoices:
                print(f"{teams[currentTeam]['name']}, it is your turn.")
                puzzleRequest = get_string(f"Which puzzle would you like? {questionChoices}: ")
            # qType = self.puzzles[puzzleRequest].type       <-- Can be used in future implementations for picture/music clues
            clue1 = self.puzzles[puzzleRequest].clues[0]
            clue2 = self.puzzles[puzzleRequest].clues[1]
            clue3 = self.puzzles[puzzleRequest].clues[2]
            clue4 = self.puzzles[puzzleRequest].clues[3]
            connection = self.puzzles[puzzleRequest].connection

            # Initialize variables.
            response = ""
            points = 5
            incorrect = False
            solved = False

            # Print the first clue; once shown, the host can progress the round based on player decisions. If the players
            # ask for the next clue, the host types "NEXT" to reduce the available points and print the next clue (if another
            # clue is available). If the team rings in and provides a correct response, the host types "SOLVED" and the team
            # is awarded points based on how many clues they've seen. If the team rings in but cannot provide a correct
            # response, the host types "INCORRECT" and reveals the rest of the clues for the opposing team to get a chance
            # to steal. If successful, the opposing team has 1 point added to their score. A 45-second countdown is started
            # simultaneously with the first clue being revealed; if the timer runs out, a message prints that the team has
            # run out of time and the other team will have a chance to steal as if they were incorrect.
            print(f"Clue 1: {clue1}")
            signal.signal(signal.SIGALRM, countdownTimer)
            signal.alarm(45)
            global TIMEOUT
            TIMEOUT = False
            while response not in ["NEXT", "SOLVED", "INCORRECT"]:
                response = get_string("NEXT clue, SOLVED puzzle, INCORRECT guess? ").upper()
                if TIMEOUT == True:
                    incorrect = True
                    points = 1
                    break
                if response == "NEXT":
                    points = 3
                    response = ""
                    break
                elif response == "SOLVED":
                    teams[currentTeam]["score"] += points
                    response = ""
                    solved = True
                    signal.alarm(0)
                    break
                elif response == "INCORRECT":
                    points = 1
                    incorrect = True
                    response = ""
                    signal.alarm(0)
                    break
            print(f"Clue 2: {clue2}")
            while (response not in ["NEXT", "SOLVED", "INCORRECT"]) and (solved != True) and (incorrect != True):
                response = get_string("NEXT clue, SOLVED puzzle, INCORRECT guess? ").upper()
                if TIMEOUT == True:
                    incorrect = True
                    points = 1
                    break
                if response == "NEXT":
                    points = 2
                    response = ""
                    break
                elif response == "SOLVED":
                    teams[currentTeam]["score"] += points
                    response = ""
                    solved = True
                    signal.alarm(0)
                    break
                elif response == "INCORRECT":
                    points = 1
                    incorrect = True
                    response = ""
                    signal.alarm(0)
                    break
            print(f"Clue 3: {clue3}")
            while (response not in ["NEXT", "SOLVED", "INCORRECT"]) and (solved != True) and (incorrect != True):
                response = get_string("NEXT clue, SOLVED puzzle, INCORRECT guess? ").upper()
                if TIMEOUT == True:
                    incorrect = True
                    points = 1
                    break
                if response == "NEXT":
                    points = 1
                    response = ""
                    break
                elif response == "SOLVED":
                    teams[currentTeam]["score"] += points
                    response = ""
                    solved = True
                    signal.alarm(0)
                    break
                elif response == "INCORRECT":
                    points = 1
                    incorrect = True
                    response = ""
                    signal.alarm(0)
                    break
            print(f"Clue 4: {clue4}")
            while (response not in ["SOLVED", "INCORRECT"]) and (solved != True) and (incorrect != True):
                response = get_string("SOLVED puzzle, INCORRECT guess? ").upper()
                if TIMEOUT == True:
                    incorrect = True
                    points = 1
                    break
                if response == "SOLVED":
                    teams[currentTeam]["score"] += points
                    response = ""
                    solved = True
                    signal.alarm(0)
                    break
                elif response == "INCORRECT":
                    points = 1
                    incorrect = True
                    response = ""
                    signal.alarm(0)
                    break
            if solved == True:
                print(f"Connection: {connection}")
            elif incorrect == True:
                while response not in ["REVEAL", "SOLVED"]:
                    response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                    if response == "REVEAL":
                        points = 0
                        print(f"Connection: {connection}")
                        response = ""
                        break
                    elif response == "SOLVED":
                        print(f"Connection: {connection}")
                        if currentTeam == 1:
                            teams[currentTeam - 1]["score"] += points
                        else:
                            teams[currentTeam + 1]["score"] += points
                        response = ""
                        break
            puzzleComplete += 1
            questionChoices.remove(puzzleRequest)
            puzzleRequest = ""
            if currentTeam == 1:
                currentTeam -= 1
            else:
                currentTeam += 1

        print("At the end of the first round:")
        print(f"The {teams[0]['name']} have {teams[0]['score']} points")
        print(f"The {teams[1]['name']} have {teams[1]['score']} points")



def countdownTimer(signum, frame):
    print("Time's up! The opposing team now has a chance to earn a bonus point.")
    global TIMEOUT
    TIMEOUT = True
    return