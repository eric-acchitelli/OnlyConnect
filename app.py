from flask import Flask, render_template, redirect, request, send_file, session
import random, only_connect, html, json
from OnlyConnect import vowelsPuzzle
from flask_session import Session

ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
app.secret_key = "VictoriaCoren-Mitchell"


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize global variables.
teams = [0] * 2
currentTeam = random.choice([0, 1])
questionsPlayed = []

# Code adapted from Flask documentation (https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/)
# Determines if the file uploaded by the user matches the .json extension.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

# Code adapted from Flask documentation (https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/)
# Confirms that the file uploaded by the user is valid and, if so, creates the gameSession object.
@app.route("/load_game", methods=["GET","POST"])
def load():
    if request.method == "POST":
        if 'filename' not in request.files:
            return render_template("invalid_file.html", message="File not found.")
        file = request.files['filename']
        if file.filename == '':
            return render_template("invalid_file.html", message="Filename empty.")
        if file and allowed_file(file.filename):
            session['gameFileName'] = file.filename
            global gameSession
            gameSession = only_connect.OnlyConnect(file)
            return render_template("select_teams.html")
        else:
            return render_template("invalid_file.html", message="Invalid file type.")
    else:
        return redirect("/")

# Initializes the team information.
@app.route("/coin_toss", methods=["GET","POST"])
def chooseTeamNames():
    if request.method == "POST":
        global teams
        teams[0] = {
            "name": request.form.get("team1"),
            "score": 0
            }
        teams[1] = {
            "name": request.form.get("team2"),
            "score": 0
            }
        return render_template("coin_toss.html", coinTossWinner=teams[currentTeam])
    else:
        return redirect("/")

# Alters the currentTeam variable based on the choice of the team who won the coin toss.
@app.route("/round1", methods=["GET","POST"])
def beginRound1():
    if request.method == "POST":
        if request.form.get("choice") == "second":
            global currentTeam
            if currentTeam == 1:
                currentTeam -= 1
            else:
                currentTeam += 1
        global teams
        global questionsPlayed
        questionsPlayed = []
        return render_template("round1.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)
    else:
        return redirect("/")

# Adds the score earned in the previously played puzzle to the team who scored the points (either the team whose turn it was if
# correct or the opposing team if they solved it after the currentTeam got it incorrect) and switches currentTeam to the opposing
# team.
@app.route("/round1inprogress", methods=["GET","POST"])
def continueRound1():
    if request.method == "POST":
        global teams
        scoringTeam = int(request.form.get("scoringTeam"))
        points = int(request.form.get("points"))
        teams[scoringTeam]["score"] += points
        global currentTeam
        global questionsPlayed
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1
        return render_template("round1.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)

# Resets the questionsPlayed list and begins round 2.
@app.route("/round2", methods=["GET"])
def beginRound2():
    global teams
    global questionsPlayed
    questionsPlayed = []
    global currentTeam
    return render_template("round2.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)

# Adds the score earned in the previously played puzzle to the team who scored the points (either the team whose turn it was if
# correct or the opposing team if they solved it after the currentTeam got it incorrect) and switches currentTeam to the opposing
# team.
@app.route("/round2inprogress", methods=["GET","POST"])
def continueRound2():
    if request.method == "POST":
        global teams
        scoringTeam = int(request.form.get("scoringTeam"))
        points = int(request.form.get("points"))
        teams[scoringTeam]["score"] += points
        global currentTeam
        global questionsPlayed
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1
        return render_template("round2.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)

# Resets the questionsPlayed list and begins round 3.
@app.route("/round3", methods=["GET"])
def beginRound3():
    global teams
    global questionsPlayed
    questionsPlayed = []
    global currentTeam
    if currentTeam == 1:
        currentTeam -= 1
    else:
        currentTeam += 1
    return render_template("round3.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)

# Adds the score earned in the previously played puzzle to the currentTeam and switches the currentTeam variable to the opposing
# team.
@app.route("/round3inprogress", methods=["GET","POST"])
def continueRound3():
    if request.method == "POST":
        global teams
        scoringTeam = int(request.form.get("scoringTeam"))
        points = int(request.form.get("points"))
        teams[scoringTeam]["score"] += points
        global currentTeam
        global questionsPlayed
        if currentTeam == 1:
            currentTeam -= 1
        else:
            currentTeam += 1
        return render_template("round3.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)

# Creates lists fo the encoded answers, decoded answers, and connections in the missing vowels round and sends them to round4.html
# for parsing in the final round.
@app.route("/round4", methods=["GET"])
def beginRound4():
    global teams
    encodedAnswers = []
    decodedAnswers = []
    connections = [0] * 4
    for i in range(4):
        encodedAnswers.append([0] * 4)
        decodedAnswers.append([0] * 4)
    i = 0
    for set_ in gameSession.round4.puzzles.keys():
        j = 0
        for clue in gameSession.round4.puzzles[set_].clues:
            encodedAnswers[i][j] = vowelsPuzzle(str(clue))
            decodedAnswers[i][j] = str(clue).upper()
            j += 1
        connections[i] = gameSession.round4.puzzles[set_].connection
        i += 1
    return render_template("round4.html", teams=teams,clues=encodedAnswers,answers=decodedAnswers,connections=connections)

# Adds the points earned during the missing vowels round to the overall team scores and determines if a tie has occurred. If
# so, run the tiebreaker round; if not, display the game over screen announcing the winner.
@app.route("/endgame", methods=["GET","POST"])
def endgame():
    if request.method == "POST":
        global teams

        teams[0]["score"] += int(request.form.get("team0points"))
        teams[1]["score"] += int(request.form.get("team1points"))
        if teams[0]["score"] == teams[1]["score"]:
            encodedTiebreaker = []
            decodedTiebreaker = []
            connections = [0]

            encodedTiebreaker.append([])
            decodedTiebreaker.append([])
            for set_ in gameSession.tiebreaker.puzzles.keys():
                for clue in gameSession.tiebreaker.puzzles[set_].clues:
                    encodedTiebreaker[0] = [vowelsPuzzle(str(clue))]
                    decodedTiebreaker[0] = [str(clue).upper()]
                connections.append(gameSession.tiebreaker.puzzles[set_].connection)
            return render_template("round4.html", teams=teams,clues=encodedTiebreaker,answers=decodedTiebreaker,connections=[["Tiebreaker"]])
        elif teams[0]["score"] > teams[1]["score"]:
            winningTeam = 0
            losingTeam = 1
        else:
            winningTeam = 1
            losingTeam = 0
        return render_template("game_over.html", teams=teams, winningTeam=winningTeam, losingTeam=losingTeam)
    else:
        return redirect("/")

# Runs the round 1 Two Reeds puzzle.
@app.route("/round1tworeeds", methods=["GET"])
def r1TwoReeds():
    global teams
    global questionsPlayed
    questionsPlayed.append('TwoReeds')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Two Reeds"], hieroglyph=html.unescape("&#78284;"))

# Runs the round 1 Lion puzzle.
@app.route("/round1lion", methods=["GET"])
def r1Lion():
    global teams
    global questionsPlayed
    questionsPlayed.append('Lion')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Lion"], hieroglyph=html.unescape("&#78061;"))

# Runs the round 1 Twisted Flax puzzle.
@app.route("/round1twistedflax", methods=["GET"])
def r1TwistedFlax():
    global teams
    global questionsPlayed
    questionsPlayed.append('TwistedFlax')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Twisted Flax"], hieroglyph=html.unescape("&#78747;"))

# Runs the round 1 Horned Viper puzzle.
@app.route("/round1hornedviper", methods=["GET"])
def r1HornedViper():
    global teams
    global questionsPlayed
    questionsPlayed.append('HornedViper')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Horned Viper"], hieroglyph=html.unescape("&#78225;"))

# Runs the round 1 Water puzzle.
@app.route("/round1water", methods=["GET"])
def r1Water():
    global teams
    global questionsPlayed
    questionsPlayed.append('Water')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Water"], hieroglyph=html.unescape("&#78359;"))

# Runs the round 1 Eye of Horus puzzle.
@app.route("/round1eyeofhorus", methods=["GET"])
def r1EyeOfHorus():
    global teams
    global questionsPlayed
    questionsPlayed.append('EyeOfHorus')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Eye of Horus"], hieroglyph=html.unescape("&#77952;"))

# Runs the round 2 Two Reeds puzzle.
@app.route("/round2tworeeds", methods=["GET"])
def r2TwoReeds():
    global teams
    global questionsPlayed
    questionsPlayed.append('TwoReeds')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Two Reeds"], hieroglyph=html.unescape("&#78284;"))

# Runs the round 2 Lion puzzle.
@app.route("/round2lion", methods=["GET"])
def r2Lion():
    global teams
    global questionsPlayed
    questionsPlayed.append('Lion')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Lion"], hieroglyph=html.unescape("&#78061;"))

# Runs the round 2 Twisted Flax puzzle.
@app.route("/round2twistedflax", methods=["GET"])
def r2TwistedFlax():
    global teams
    global questionsPlayed
    questionsPlayed.append('TwistedFlax')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Twisted Flax"], hieroglyph=html.unescape("&#78747;"))

# Runs the round 2 Horned Viper puzzle.
@app.route("/round2hornedviper", methods=["GET"])
def r2HornedViper():
    global teams
    global questionsPlayed
    questionsPlayed.append('HornedViper')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Horned Viper"], hieroglyph=html.unescape("&#78225;"))

# Runs the round 2 Water puzzle.
@app.route("/round2water", methods=["GET"])
def r2Water():
    global teams
    global questionsPlayed
    questionsPlayed.append('Water')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Water"], hieroglyph=html.unescape("&#78359;"))

# Runs the round 2 Eye of Horus puzzle.
@app.route("/round2eyeofhorus", methods=["GET"])
def r2EyeOfHorus():
    global teams
    global questionsPlayed
    questionsPlayed.append('EyeOfHorus')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Eye of Horus"], hieroglyph=html.unescape("&#77952;"))

# Runs the round 3 Lion puzzle.
@app.route("/round3lion", methods=["GET"])
def r3Lion():
    global teams
    global questionsPlayed
    questionsPlayed.append('Lion')
    connectingWall = []
    for set_ in gameSession.round3.puzzles["Lion"]:
        for clue in gameSession.round3.puzzles["Lion"][set_].clues:
            connectingWall.append(str(clue))
    random.shuffle(connectingWall)
    puzzle = "Lion"
    return render_template("round3puzzle.html", currentTeam=currentTeam, teams=teams, connectingWall=connectingWall,
                            set1=gameSession.round3.puzzles["Lion"]["Set 1"].__dict__,
                            set2=gameSession.round3.puzzles["Lion"]["Set 2"].__dict__,
                            set3=gameSession.round3.puzzles["Lion"]["Set 3"].__dict__,
                            set4=gameSession.round3.puzzles["Lion"]["Set 4"].__dict__,
                            hieroglyph=html.unescape("&#78061;"), puzzle=puzzle)

# Runs the round 3 Water puzzle.
@app.route("/round3water", methods=["GET"])
def r3Water():
    global teams
    global questionsPlayed
    questionsPlayed.append('Water')
    connectingWall = []
    for set_ in gameSession.round3.puzzles["Water"]:
        for clue in gameSession.round3.puzzles["Water"][set_].clues:
            connectingWall.append(str(clue))
    random.shuffle(connectingWall)
    puzzle = "Water"
    return render_template("round3puzzle.html", currentTeam=currentTeam, teams=teams, connectingWall=connectingWall,
                            set1=gameSession.round3.puzzles["Water"]["Set 1"].__dict__,
                            set2=gameSession.round3.puzzles["Water"]["Set 2"].__dict__,
                            set3=gameSession.round3.puzzles["Water"]["Set 3"].__dict__,
                            set4=gameSession.round3.puzzles["Water"]["Set 4"].__dict__,
                            hieroglyph=html.unescape("&#78359;"), puzzle=puzzle)

# After the round 3 connecting wall, collects the order that the sets were solved and runs round3connections.html to allow
# players to provide the connections in order of the finding of the groups. If not all groups were found, the remaining sets
# are added in order.
@app.route("/round3connections", methods=["GET","POST"])
def r3connections():
    setOrder=json.loads(request.form.get("correctSets"))
    puzzle=str(request.form.get("puzzle"))
    if puzzle == "Water":
        hieroglyph = html.unescape("&#78359;")
    elif puzzle == "Lion":
        hieroglyph = html.unescape("&#78061;")
    if len(setOrder) < 4:
        for set_ in ["Set 1", "Set 2", "Set 3", "Set 4"]:
            if set_ not in setOrder:
                setOrder.append(set_)
    return render_template("round3connections.html", currentTeam=currentTeam, teams=teams,
                            set1=gameSession.round3.puzzles[puzzle]["Set 1"].__dict__,
                            set2=gameSession.round3.puzzles[puzzle]["Set 2"].__dict__,
                            set3=gameSession.round3.puzzles[puzzle]["Set 3"].__dict__,
                            set4=gameSession.round3.puzzles[puzzle]["Set 4"].__dict__,
                            setOrder=setOrder, wallPoints=request.form.get("points"),
                            hieroglyph=hieroglyph)

# Route designed to allow the user to download questions_template.json to their device
@app.route("/template", methods=["GET"])
def download():
    path = 'static/questions_template.json'
    return send_file(path, as_attachment=True)