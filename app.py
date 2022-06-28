import sys, random, only_connect
from cs50 import get_string


questionChoices = []
BUTTON_CHOICES = ["NEXT","SOLVED","INCORRECT"]


if len(sys.argv) != 2:
    print("Usage: python app.py <puzzle_collection>")

gameSession = only_connect.OnlyConnect(sys.argv[1])

teams = [0] * 2
teamName = ""

# Collect team names.
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

# Initialize variables.
currentTeam = random.choice([0,1])
response = ""
puzzleComplete = 0
puzzleRequest = ""
coinTossChoice = ""

# Ask the winner of the coin toss whether they would like to go first or second.
while coinTossChoice not in ["FIRST","SECOND"]:
    coinTossChoice = get_string(f"{teams[currentTeam]['name']}, you won the toss. Would you like to go FIRST or SECOND? ").upper()
    if coinTossChoice != "FIRST":
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1

# Play the game.
gameSession.round1.play(teams, currentTeam)
gameSession.round2.play(teams, currentTeam)
gameSession.round3.play(teams, currentTeam)
print("The final round, the missing vowels round is upon us. When both teams are ready, we will begin.")
while response != "YES" and response != "NO":
    response = get_string("Ready? [yes/no]").upper()
    if response == "YES":
        gameSession.round4.play(teams)
        response = ""
        break


#Check the final score and print the results. If there is a tie, run the tiebreaker round and check the score again..
if teams[0]['score'] > teams[1]['score']:
    print(f"The winner, with {teams[0]['score']} points, is the {teams[0]['name']}! Coming close behind in second place with {teams[1]['score']} points is the {teams[1]['name']}!")
elif teams[1]['score'] > teams[0]['score']:
    print(f"The winner, with {teams[1]['score']} points, is the {teams[1]['name']}! Coming close behind in second place with {teams[0]['score']} points is the {teams[0]['name']}!")
elif teams[0]['score'] == teams[1]['score']:
    print(f"It's a tie! Both the {teams[0]['name']} and the {teams[1]['name']} have scored {teams[1]['score']} points!")
    print("To break this tie, we will do one more missing vowels puzzle. No special connection for this puzzle, and only team captains may participate.")
    print("If you buzz in and get it right, your team wins! However, if you buzz in and get it wrong, you lose a point and break the tie, letting your opponents win!")
    while (response != "YES") and (response != "NO"):
        response = get_string("Ready? [yes/no]").upper()
        if response == "YES":
            gameSession.tiebreaker.play(teams)
            if teams[0]['score'] > teams[1]['score']:
                print(f"The winner, with {teams[0]['score']} points, is the {teams[0]['name']}! Coming close behind in second place with {teams[1]['score']} points is the {teams[1]['name']}!")
            elif teams[1]['score'] > teams[0]['score']:
                print(f"The winner, with {teams[1]['score']} points, is the {teams[1]['name']}! Coming close behind in second place with {teams[0]['score']} points is the {teams[0]['name']}!")


