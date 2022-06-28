import random
import signal
from OnlyConnectDir import RoundBase, Puzzle
from cs50 import get_string


class ConnectingWall(RoundBase):
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
        questionChoices = []
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


def wallCountdownTimer(signum, frame):
    print("Time's up! Time to see if you can spot the connections between these groups. We'll start with the groups you found and then see if you can figure out the connection of any that you didn't find.")
    global TIMEOUT
    TIMEOUT = True
    return
