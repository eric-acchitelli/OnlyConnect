from flask import Flask, render_template, redirect, request, send_file
import sys, random, only_connect, html, json
from OnlyConnect import vowelsPuzzle

app = Flask(__name__)

# Initialize global variables.
teams = [0] * 2
currentTeam = random.choice([0, 1])
questionsPlayed = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load_game", methods=["GET","POST"])
def load():
    if request.method == "POST":
        file = request.form.get("filename")
        if file.endswith('.json'):
            global gameSession
            gameSession = only_connect.OnlyConnect(file)
            return render_template("select_teams.html")
        else:
            return render_template("invalid_file.html")
    else:
        return redirect("/")


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
        #teams = gameSession.round1.play(teams, currentTeam)
        return render_template("round1.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)
    else:
        return redirect("/")


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

@app.route("/round2", methods=["GET"])
def beginRound2():
    global teams
    global questionsPlayed
    questionsPlayed = []
    global currentTeam
    #teams = gameSession.round1.play(teams, currentTeam)
    return render_template("round2.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)


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
    #teams = gameSession.round1.play(teams, currentTeam)
    return render_template("round3.html", currentTeam=currentTeam, teams=teams, questionsPlayed=questionsPlayed)


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


@app.route("/round1tworeeds", methods=["GET"])
def r1TwoReeds():
    #global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('TwoReeds')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Two Reeds"], hieroglyph=html.unescape("&#78284;"))


@app.route("/round1lion", methods=["GET"])
def r1Lion():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('Lion')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Lion"], hieroglyph=html.unescape("&#78061;"))


@app.route("/round1twistedflax", methods=["GET"])
def r1TwistedFlax():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('TwistedFlax')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Twisted Flax"], hieroglyph=html.unescape("&#78747;"))


@app.route("/round1hornedviper", methods=["GET"])
def r1HornedViper():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('HornedViper')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Horned Viper"], hieroglyph=html.unescape("&#78225;"))


@app.route("/round1water", methods=["GET"])
def r1Water():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('Water')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Water"], hieroglyph=html.unescape("&#78359;"))


@app.route("/round1eyeofhorus", methods=["GET"])
def r1EyeOfHorus():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('EyeOfHorus')
    return render_template("round1puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round1.puzzles["Eye of Horus"], hieroglyph=html.unescape("&#77952;"))


@app.route("/round2tworeeds", methods=["GET"])
def r2TwoReeds():
    #global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('TwoReeds')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Two Reeds"], hieroglyph=html.unescape("&#78284;"))


@app.route("/round2lion", methods=["GET"])
def r2Lion():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('Lion')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Lion"], hieroglyph=html.unescape("&#78061;"))


@app.route("/round2twistedflax", methods=["GET"])
def r2TwistedFlax():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('TwistedFlax')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Twisted Flax"], hieroglyph=html.unescape("&#78747;"))


@app.route("/round2hornedviper", methods=["GET"])
def r2HornedViper():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('HornedViper')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Horned Viper"], hieroglyph=html.unescape("&#78225;"))


@app.route("/round2water", methods=["GET"])
def r2Water():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('Water')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Water"], hieroglyph=html.unescape("&#78359;"))


@app.route("/round2eyeofhorus", methods=["GET"])
def r2EyeOfHorus():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
    global questionsPlayed
    questionsPlayed.append('EyeOfHorus')
    return render_template("round2puzzle.html", currentTeam=currentTeam, teams=teams,
                            puzzle=gameSession.round2.puzzles["Eye of Horus"], hieroglyph=html.unescape("&#77952;"))

@app.route("/round3lion", methods=["GET"])
def r3Lion():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
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

@app.route("/round3water", methods=["GET"])
def r3Water():
    global teams
    #teams = gameSession.round1.play(teams, currentTeam)
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

@app.route("/template", methods=["GET"])
def download():
    path = 'static/questions_template.json'
    return send_file(path, as_attachment=True)