import json, sys
from cs50 import get_string
import random

questionChoices = []
BUTTON_CHOICES = ["NEXT","SOLVED","INCORRECT"]


if len(sys.argv) != 2:
    print("Usage: python app.py <puzzle_collection>")

with open(sys.argv[1]) as file:
    puzzles = json.load(file)

teams = [0] * 2
teamName = ""

for i in range(2):
    while teamName == "":
        teamName = get_string(f"Team {(i+1)}'s Name: ")
        teams[i] = {
            "name": teamName,
            "score": 0
        }

    if i != 1:
        print(f"{teams[i]}")
        teamName = ""

currentTeam = random.choice([0,1])
roundNumber = 1
puzzleComplete = 0
puzzleRequest = ""


while roundNumber < 3:
    roundString = "Round " + str(roundNumber)
    for key in puzzles[roundString].keys():
        questionChoices.append(str(key))
    while puzzleComplete != 6:
        while puzzleRequest not in questionChoices:
            print(f"{teams[currentTeam]['name']}, it is your turn.")
            puzzleRequest = get_string(f"Which puzzle would you like? {questionChoices}: ")
        qType = puzzles[roundString][puzzleRequest]["type"]
        clue1 = puzzles[roundString][puzzleRequest]["clue1"]
        clue2 = puzzles[roundString][puzzleRequest]["clue2"]
        clue3 = puzzles[roundString][puzzleRequest]["clue3"]
        clue4 = puzzles[roundString][puzzleRequest]["clue4"]
        connection = puzzles[roundString][puzzleRequest]["connection"]
        response = ""
        points = 5
        print(f"Question Type: {qType}")
        print(f"Clue 1: {clue1}")
        while response not in BUTTON_CHOICES:
            response = get_string("NEXT clue, SOLVED puzzle, INCORRECT guess?")
            if response == "NEXT":
                points = 3
                break
            elif response == "SOLVED":
                teams[currentTeam]["score"] += points
            elif response == "INCORRECT":
                points = 1
        print(f"Clue 2: {clue2}")
        print(f"Clue 3: {clue3}")
        print(f"Clue 4: {clue4}")
        print(f"Connection: {connection}")
        puzzleComplete += 1
        questionChoices.remove(puzzleRequest)
        puzzleRequest = ""
        if not (roundNumber == 2 and puzzleComplete == 6):
            if currentTeam == 1:
                currentTeam -= 1
            else:
                currentTeam += 1
    roundNumber += 1
    puzzleComplete = 0
print(f"{teams[currentTeam]['name']}, you get to choose which connecting wall you want.")

while roundNumber < 4:
    roundString = "Round " + str(roundNumber)
    for key in puzzles[roundString].keys():
        questionChoices.append(str(key))
    while puzzleComplete != 2:
        connectingWall = []
        setNumber = []
        wallComplete = 0
        setTracker = 1
        set1 = [0] * 4
        set2 = [0] * 4
        set3 = [0] * 4
        set4 = [0] * 4
        setTemp = [0] * 4
        initialSet = 0
        match = True
        lives = 3
        while puzzleRequest not in questionChoices:
            print(f"{teams[currentTeam]['name']}, it is your turn.")
            puzzleRequest = get_string(f"Which puzzle would you like? {questionChoices}: ")
        if len(setNumber) == 0:
            for key in puzzles[roundString][puzzleRequest].keys():
                setNumber.append(str(key))
        for key in setNumber:
            setValues = puzzles[roundString][puzzleRequest][key].values()
            for item in setValues:
                if item != puzzles[roundString][puzzleRequest][key]["connection"]:
                    connectingWall.append(str(item))
            random.shuffle(connectingWall)
        while setTracker < 5:
            guess1 = ""
            guess2 = ""
            guess3 = ""
            guess4 = ""
            match = True
            print(f"{connectingWall}")
            while guess1 not in connectingWall:
                guess1 = get_string(f"Select 4 entries from the connecting wall. ")
                if guess1 not in connectingWall:
                    print("Not in Connecting Wall.")
            for i in range(1,5):
                if guess1 in puzzles[roundString][puzzleRequest][f"Set {i}"].values():
                    initialSet = i
            while (guess2 not in connectingWall):
                guess2 = get_string(f"Select 3 more entries from the connecting wall. ")
                if guess2 not in connectingWall:
                    print("Not in Connecting Wall.")
                elif (guess2 == guess1):
                    print("Already guessed in this set.")
                    guess2 = ""
            if ((guess2 in puzzles[roundString][puzzleRequest][f"Set {initialSet}"].values()) and (match == True)) == False:
                match = False
            while (guess3 not in connectingWall):
                guess3 = get_string(f"Select 2 more entries from the connecting wall. ")
                if guess3 not in connectingWall:
                    print("Not in Connecting Wall.")
                elif (guess3 == guess1) or (guess3 == guess2):
                    print("Already guessed in this set.")
                    guess3 = ""
            if ((guess3 in puzzles[roundString][puzzleRequest][f"Set {initialSet}"].values()) and (match == True)) == False:
                match = False
            while (guess4 not in connectingWall):
                guess4 = get_string(f"Select 1 more entry from the connecting wall. ")
                if guess4 not in connectingWall:
                    print("Not in Connecting Wall.")
                elif (guess4 == guess1) or (guess4 == guess2) or (guess4 == guess3):
                    print("Already guessed in this set.")
                    guess4 = ""
            if ((guess4 in puzzles[roundString][puzzleRequest][f"Set {initialSet}"].values()) and (match == True)) == False:
                match = False
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
                setTracker += 1
            elif (match == False) and (setTracker == 3):
                lives -= 1
                print(f"You have {lives} lives remaining.")
                if lives == 0:
                    print("You are out of lives.")
                    break
        if setTracker > 1:
            print(f"{set1}")
            for i in range (1,5):
                if set1[0] in puzzles[roundString][puzzleRequest][f"Set {i}"].values():
                    print(f"{puzzles[roundString][puzzleRequest][f'Set {i}']['connection']}")
        if setTracker > 2:
            print(f"{set2}")
            for i in range (1,5):
                if set2[0] in puzzles[roundString][puzzleRequest][f"Set {i}"].values():
                    print(f"{puzzles[roundString][puzzleRequest][f'Set {i}']['connection']}")
        if setTracker > 3:
            print(f"{set3}")
            for i in range (1,5):
                if set3[0] in puzzles[roundString][puzzleRequest][f"Set {i}"].values():
                    print(f"{puzzles[roundString][puzzleRequest][f'Set {i}']['connection']}")
            print(f"{set4}")
            for i in range (1,5):
                if set4[0] in puzzles[roundString][puzzleRequest][f"Set {i}"].values():
                    print(f"{puzzles[roundString][puzzleRequest][f'Set {i}']['connection']}")

        puzzleComplete += 1
        questionChoices.remove(puzzleRequest)
        puzzleRequest = ""
        connectingWall = []
    roundNumber += 1

roundString = "Round " + str(roundNumber)
for set in puzzles[roundString]:
    print(f"{puzzles[roundString][set]['connection']}")
    for i in range(1,5):
        nospacesinput = ''.join(ch.upper() for ch in puzzles[roundString][set][str(i)] if ch.isalpha())
        vowels = ['A','E','I','O','U']
        novowelsinput = ''.join(ch for ch in nospacesinput if ch not in vowels)
        finalOutput = ''
        spaceProb = 0.00
        for ch in novowelsinput:
            finalOutput += ch
            spaceProb += 0.15
            if random.random() < spaceProb:
                finalOutput += ' '
                spaceProb = 0

        print(f"{finalOutput}")
        print(f"{puzzles[roundString][set][str(i)]}")


if "Soprano" in puzzles["Round 3"]["Water"]["Set 2"].values():
    print("yes")




