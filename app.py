import sys, random, only_connect
from cs50 import get_string


questionChoices = []
BUTTON_CHOICES = ["NEXT","SOLVED","INCORRECT"]


if len(sys.argv) != 2:
    print("Usage: python app.py <puzzle_collection>")

gameSession = only_connect.OnlyConnect(sys.argv[1])

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
coinTossChoice = ""

while coinTossChoice not in ["FIRST","SECOND"]:
    coinTossChoice = get_string(f"{teams[currentTeam]['name']}, you won the toss. Would you like to go FIRST or SECOND? ").upper()
    if coinTossChoice != "FIRST":
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1

gameSession.round1.play(teams, currentTeam)
gameSession.round2.play(teams, currentTeam)
gameSession.round3.play(teams, currentTeam)
gameSession.round4.play(teams)

if teams[0]['score'] > teams[1]['score']:
    print(f"The winner, with {teams[0]['score']} points, is the {teams[0]['name']}! Coming close behind in second place with {teams[1]['score']} points is the {teams[1]['name']}!")
elif teams[1]['score'] > teams[0]['score']:
    print(f"The winner, with {teams[1]['score']} points, is the {teams[1]['name']}! Coming close behind in second place with {teams[0]['score']} points is the {teams[0]['name']}!")
elif teams[0]['score'] == teams[1]['score']:
    print(f"It's a tie! Both the {teams[0]['name']} and the {teams[1]['name']} have scored {teams[1]['score']} points!")


