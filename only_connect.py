import json
import random
import signal
from typing import Any, Dict, List
from cs50 import get_string

questionChoices = []


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


class Puzzle:
    def __init__(self, parameters: Dict[str, Any]):
        self.connection: str = parameters["connection"]
        self.clues: List[str] = [values for keys, values in parameters.items() if "clue" in keys]
        self.type = [values for keys, values in parameters.items() if "type" in keys]


# Abstract base class for actual round types.
class Round:
    def __init__(self, questions):
        self.puzzles = {}
        for hieroglyph, puzzle in questions.items():
            self.puzzles[hieroglyph] = Puzzle(puzzle)

    def play():
        pass


class Connection(Round):
    def play(self, teams: List[Dict[str, int]], currentTeam: int):

        # Initialize variables.
        puzzleRequest = ""
        puzzleComplete = 0

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


class Sequences(Round):
    def play(self, teams, currentTeam):

        # Initialize variables.
        puzzleRequest = ""
        puzzleComplete = 0

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

            # This puzzle works almost identically with the first round; the only difference between the two is that the
            # teams can only see a maximum of three clues instead of all four; this is because the teams are trying to
            # provide as their answer not the connection, but what would come fourth in the sequence of clues being revealed.
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
                elif response == "NEXT":
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
                print(f"Clue 4: {clue4}")
                print(f"Connection: {connection}")
            elif incorrect == True:
                while response not in ["REVEAL", "SOLVED"]:
                    response = get_string("REVEAL solution, SOLVED puzzle ?").upper()
                    if response == "REVEAL":
                        points = 0
                        print(f"Clue 4: {clue4}")
                        print(f"Connection: {connection}")
                        response = ""
                        break
                    elif response == "SOLVED":
                        print(f"Clue 4: {clue4}")
                        print(f"Connection: {connection}")
                        if currentTeam == 1:
                            teams[currentTeam - 1]["score"] += points
                        else:
                            teams[currentTeam + 1]["score"] += points
                        response = ""
                        break

            # Note that the puzzle has been completed and remove the hieroglyph from the list of options for the next player.
            # If this was not the last puzzle of this round, alter the currentTeam variable to reflect whose turn is next.
            puzzleComplete += 1
            questionChoices.remove(puzzleRequest)
            puzzleRequest = ""
            TIMEOUT = False
            if puzzleComplete != 6:
                if currentTeam == 1:
                    currentTeam -= 1
                else:
                    currentTeam += 1
        print("At the end of the second round:")
        print(f"The {teams[0]['name']} have {teams[0]['score']} points")
        print(f"The {teams[1]['name']} have {teams[1]['score']} points")


class ConnectingWall(Round):
    def __init__(self, questions):
        self.puzzles = {}
        for hieroglyph in questions:
            if not hieroglyph in self.puzzles:
                self.puzzles[hieroglyph] = {}
            for set_, puzzle in questions[hieroglyph].items():
                self.puzzles[hieroglyph][set_] = Puzzle(puzzle)

    def play(self, teams, currentTeam):
        puzzleRequest = ""
        puzzleComplete = 0
        for key in self.puzzles.keys():
            questionChoices.append(str(key))
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1

        # Setup for the connecting wall round plays out here.
        while puzzleComplete != 2:

            # Initialize variables.
            connectingWall = []
            setTracker = 1
            set1 = [0] * 4
            set2 = [0] * 4
            set3 = [0] * 4
            set4 = [0] * 4
            setTemp = [0] * 4
            initialSet = 0
            match = True
            lives = 3
            wallPoints = 0

            # Ask the player which connecting wall they would like to play. Once selected, add all of the clues from each
            # set to the connecting wall list and then shuffle the list.
            while puzzleRequest not in questionChoices:
                print(f"{teams[currentTeam]['name']}, it is your turn.")
                puzzleRequest = get_string(f"Which puzzle would you like? {questionChoices}: ")
            for set in self.puzzles[puzzleRequest]:
                for clue in self.puzzles[puzzleRequest][set].clues:
                    connectingWall.append(str(clue))
                random.shuffle(connectingWall)

            # The round begins here. setTracker notes which set the player is looking for.
            while setTracker < 5:
                guess1 = ""
                guess2 = ""
                guess3 = ""
                guess4 = ""
                match = True
                global TIMEOUT
                TIMEOUT = False
                # Print the connecting wall for the player and begin the 3-minute countdown for the round. Once the timer
                # runs out, a message will print stating that the round is over and will not accept any further input from
                # the user.
                print(f"Connecting Wall: {connectingWall}")
                signal.signal(signal.SIGALRM, wallCountdownTimer)
                signal.alarm(180)
                # Ask the user for four entries from the connecting wall, checking that each one is actually on the wall
                # and is unique (no duplicates). Check the first entry and note which set of answers it belongs to, then
                # check every other guess to see if they are all in that set. If any of them do not fall in that set, set
                # match to False.
                while guess1 not in connectingWall:
                    guess1 = get_string(f"Select 4 entries from the connecting wall. ")
                    if TIMEOUT == True:
                        match = False
                        break
                    if guess1 not in connectingWall:
                        print("Not in Connecting Wall.")
                for set in self.puzzles[puzzleRequest]:
                    if guess1 in self.puzzles[puzzleRequest][set].clues:
                        initialSet = set
                while (guess2 not in connectingWall):
                    guess2 = get_string(f"Select 3 more entries from the connecting wall. ")
                    if TIMEOUT == True:
                        match = False
                        break
                    if guess2 not in connectingWall:
                        print("Not in Connecting Wall.")
                    elif (guess2 == guess1):
                        print("Already guessed in this set.")
                        guess2 = ""
                if ((guess2 in self.puzzles[puzzleRequest][initialSet].clues) and (match == True)) == False:
                    match = False
                while (guess3 not in connectingWall):
                    guess3 = get_string(f"Select 2 more entries from the connecting wall. ")
                    if TIMEOUT == True:
                        match = False
                        break
                    if guess3 not in connectingWall:
                        print("Not in Connecting Wall.")
                    elif (guess3 == guess1) or (guess3 == guess2):
                        print("Already guessed in this set.")
                        guess3 = ""
                if ((guess3 in self.puzzles[puzzleRequest][initialSet].clues) and (match == True)) == False:
                    match = False
                while (guess4 not in connectingWall):
                    guess4 = get_string(f"Select 1 more entry from the connecting wall. ")
                    if TIMEOUT == True:
                        match = False
                        break
                    if guess4 not in connectingWall:
                        print("Not in Connecting Wall.")
                    elif (guess4 == guess1) or (guess4 == guess2) or (guess4 == guess3):
                        print("Already guessed in this set.")
                        guess4 = ""
                if ((guess4 in self.puzzles[puzzleRequest][initialSet].clues) and (match == True)) == False:
                    match = False

                # If a complete set is found, remove the phrases from the wall and place them into a dedicated variable. When
                # two sets are found, remind the user that they only have three tries to find the remaining two groups; in
                # this case, each failure removes a life. Once all three "lives" are used, the user is informed that they are
                # out of lives and is taken immediately to the connections part of the round. If a third set is found, the
                # fourth set is automatically found (since there are only four entries left in the connecting wall) and an
                # extra point is added to account for the fourth group. If a match is not found but the player has not yet
                # found two other sets, an error message is printed to ask the player to try again. The timer started at the
                # beginning of the round will be disabled when either of the game end conditions are reached.
                if match == True:
                    setTemp = [guess1, guess2, guess3, guess4]
                    for item in setTemp:
                        connectingWall.remove(item)
                    if setTracker == 1:
                        set1 = setTemp
                    elif setTracker == 2:
                        set2 = setTemp
                        print(f"You have {lives} lives now. Any incorrect set causes you to lose a life.")
                    elif setTracker == 3:
                        set3 = setTemp
                        set4 = connectingWall
                        setTracker += 1
                        wallPoints += 1
                        signal.alarm(0)
                    setTracker += 1
                    wallPoints += 1
                elif (match == False) and (setTracker == 3):
                    lives -= 1
                    print(f"Incorrect. You have {lives} lives remaining.")
                    if lives == 0:
                        print("You are out of lives.")
                        signal.alarm(0)
                        break
                else:
                    print("Incorrect. Try again.")

            # The host now must go through each found set, one at a time, and confirm that the player knows what the connection
            # is between all four items in the set. Since the sets can be found in any order, the for loop looks for the answer
            # set that holds the first value of the player's set. If they do, the host types "SOLVED," which gives the team a
            # point; if not, the host types "REVEAL" to reveal the connection and move to the next one. After the found sets
            # are examined, the remaining sets that were not found are revealed and the player has the opportunity to give
            # the connections for those sets, earning points for each correct connection.
            response = ""
            if setTracker > 1:
                print(f"{set1}")
                for set in self.puzzles[puzzleRequest]:
                    if set1[0] in self.puzzles[puzzleRequest][set].clues:
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                break
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                wallPoints += 1
                                break
            elif setTracker == 1:
                for set in self.puzzles[puzzleRequest]:
                    print(f"{self.puzzles[puzzleRequest][set].clues}")
                    while response not in ["REVEAL", "SOLVED"]:
                        response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                        if response == "REVEAL":
                            print(f"{self.puzzles[puzzleRequest][set].connection}")
                            break
                        elif response == "SOLVED":
                            print(f"{self.puzzles[puzzleRequest][set].connection}")
                            wallPoints += 1
                            break

            response = ""
            if setTracker > 2:
                print(f"{set2}")
                for set in self.puzzles[puzzleRequest]:
                    if set2[0] in self.puzzles[puzzleRequest][set].clues:
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                wallPoints += 1
            elif setTracker == 2:
                for set in self.puzzles[puzzleRequest]:
                    if set1[0] not in self.puzzles[puzzleRequest][set].clues:
                        print(f"{self.puzzles[puzzleRequest][set].clues}")
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                break
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                wallPoints += 1
                                break
            response = ""
            if setTracker > 3:
                print(f"{set3}")
                for set in self.puzzles[puzzleRequest]:
                    if set3[0] in self.puzzles[puzzleRequest][set].clues:
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                wallPoints += 1
                response = ""
                print(f"{set4}")
                for set in self.puzzles[puzzleRequest]:
                    if set4[0] in self.puzzles[puzzleRequest][set].clues:
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                wallPoints += 1
            elif setTracker == 3:
                for set in self.puzzles[puzzleRequest]:
                    if (set1[0] not in self.puzzles[puzzleRequest][set].clues) and (set2[0] not in self.puzzles[puzzleRequest][set].clues):
                        print(f"{self.puzzles[puzzleRequest][set].clues}")
                        while response not in ["REVEAL", "SOLVED"]:
                            response = get_string("REVEAL solution, SOLVED puzzle? ").upper()
                            if response == "REVEAL":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                response = ""
                                break
                            elif response == "SOLVED":
                                print(f"{self.puzzles[puzzleRequest][set].connection}")
                                response = ""
                                wallPoints += 1
                                break

            # If the team found all four groups and gave all four correct connections, they receive a two point bonus to their
            # wall score. The final total will be added to their total score. A confirmation message prints their current score.
            if wallPoints == 8:
                wallPoints += 2
            teams[currentTeam]["score"] += wallPoints
            print(
                f"You have scored a total of {wallPoints} at the Connecting Wall, for a new total score of {teams[currentTeam]['score']}")

            # Document the completion of the wall, remove that option from the choices for the next player, and change the
            # currentTeam variable to reflect that it is the next player's turn.
            puzzleComplete += 1
            questionChoices.remove(puzzleRequest)
            puzzleRequest = ""
            connectingWall = []
            if currentTeam == 1:
                currentTeam -= 1
            else:
                currentTeam += 1
        print("After the Connecting Wall:")
        print(f"The {teams[0]['name']} have {teams[0]['score']} points")
        print(f"The {teams[1]['name']} have {teams[1]['score']} points")


class MissingVowels(Round):
    def play(self, teams):
        puzzleComplete = 0
        response = ""
        BUTTON_OPTIONS = [(f"{teams[0]['name']} correct").upper(), (f"{teams[1]['name']} correct").upper(),
                          (f"{teams[0]['name']} incorrect").upper(), (f"{teams[1]['name']} incorrect").upper(), "SKIP"]
        TEAM_0_BUTTON_OPTIONS = [(f"{teams[0]['name']} correct").upper(), (f"{teams[0]['name']} incorrect").upper()]
        TEAM_1_BUTTON_OPTIONS = [(f"{teams[1]['name']} correct").upper(), (f"{teams[1]['name']} incorrect").upper()]
        for set in self.puzzles.keys():
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
                        while response not in TEAM_1_BUTTON_OPTIONS:
                            response = get_string(f"{TEAM_1_BUTTON_OPTIONS} ").upper()
                            if response == f"{teams[1]['name']} correct".upper():
                                teams[1]['score'] += 1
                                response = ""
                                break
                            else:
                                response = ""
                                break
                        break
                    elif response == f"{teams[1]['name']} incorrect".upper():
                        if teams[1]['score'] > 0:
                            teams[1]['score'] -= 1
                        response = ""
                        while response not in TEAM_0_BUTTON_OPTIONS:
                            response = get_string(f"{TEAM_0_BUTTON_OPTIONS} ").upper()
                            if response == f"{teams[0]['name']} correct".upper():
                                teams[0]['score'] += 1
                                response = ""
                                break
                            else:
                                response = ""
                                break
                    elif response == "SKIP":
                        response = ""
                        break
                print(f"----------{clue}")
            print(f"{teams[0]['name']} have {teams[0]['score']} points")
            print(f"{teams[1]['name']} have {teams[1]['score']} points")


class Tiebreaker(Round):
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


# A function to remove vowels from and randomly add spaces to a string.
def vowelsPuzzle(clue: str):
    nospaces = ''.join(ch.upper() for ch in clue if ch.isalpha())
    vowels = ['A', 'E', 'I', 'O', 'U']
    novowels = ''.join(ch for ch in nospaces if ch not in vowels)
    finalOutput = ''
    spaceProb = 0.00
    for ch in novowels:
        finalOutput += ch
        spaceProb += 0.15
        if random.random() < spaceProb:
            finalOutput += ' '
            spaceProb = 0.00
    return finalOutput


def countdownTimer(signum, frame):
    print("Time's up! The opposing team now has a chance to earn a bonus point.")
    global TIMEOUT
    TIMEOUT = True
    return


def wallCountdownTimer(signum, frame):
    print("Time's up! Time to see if you can spot the connections between these groups. We'll start with the groups you found and then see if you can figure out the connection of any that you didn't find.")
    global TIMEOUT
    TIMEOUT = True
    return

