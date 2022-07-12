# ONLY CONNECT HOST ASSISTANT
### Video Demo: https://youtu.be/_VhhFh76-Xc
### Description:
The Only Connect Host Assistant is an application designed to serve as a game-master aid for a homemade, in-person version of *Only Connect*, based on the BBC quiz show of the same name. Included in this repository are two different versions of the program: a command-line program run directly in the command-line of the terminal, `commandLineProgram.py`, and a Flask app utilizing HTML and JavaScript programming, which is implemented and called from `app.py`. A number of helper files and templates were created in directories `templates`, `static`, and `OnlyConnect`.

#### Background
What is *Only Connect*? Introduced to the world by the British Broadcasting Corporation in 2008, *Only Connect* is often cited as one of television's hardest quiz shows. Host Victoria Coren-Mitchell pits two teams of three against each other in a tournament-style competition of finding the connection between seemingly unrelated clues, forcing contestants to use lateral thinking and patience to find the answers that will get them the points they need to win the game.

I was introduced to *Only Connect* near the end of the summer of 2021, when I was originally introduced to Victoria Coren Mitchell when watching series 12 of *Taskmaster*, another game show based in the UK (and given a spot on week 8's homepage assignment as one example of my "British Nonsense"). Some of my friends had mentioned that Victoria was the host of a quiz show that seemed right up my alley and expressed surprise that I had never heard of the show. Fortunately for me, there were a number of seasons available on YouTube for me to see if it was for me.

It was. I loved the format of the show immensely and realized that I could absolutely do something similar to that for my own friend group. I've already made four of my own homemade games as a PowerPoint presentation and hosted them for my friends to enjoy, which they did immensely. However, there were some definite drawbacks to my renditions:

1. The PowerPoint was a static file, so I couldn't easily track the team information inside of the PowerPoint; I resorted to keeping track either with paper or my phone.
2. The third round, the Connecting Wall, consists of a 4x4 grid of seemingly unrelated clues that must be combined into four related sets of four clues. The general gameplay would require players to take control of the computer and click four clues at a time in order to find those clues, functionality that PowerPoint definitely did not have. For this portion, I was forced to use a third-party site, [PuzzGrid](https://www.puzzgrid.com/), that my players would be able to use.

While I was able to make these work on their own accord, I knew that I wanted to have a solution that would be able to run all of these things for me. Then, when I began taking CS50, I realized that I could make the very thing that I was looking for, which is the program in this repository. I opted to shoot to build a Flask/HTML application for this project after the struggle that was the development of week 8's homepage assignment: HTML decidedly wasn't my strong suit, so I decided to use this opportunity for my final project to really delve deep and attempt to make another site almost from scratch.

### Brief Overview of Main Files

#### questions.json & questions_template.json
These .json files are the vehicle in which all of the puzzles lie. `questions.json` includes the sample game that appears in the video demo, while `questions_template.json` is a blank template that is available to be downloaded in the Flask version of the app for prospective game masters to develop their own games for use in the program.

#### commandLineProgram.py
This was the proof of concept program for initial logic development of the program. The command line prompt must include the file that houses all of the puzzles as an additional argument in order for the program to initialize properly. Once run, the program creates a user-defined object, invites the user to enter in the names of each team, and then plays through each round using the object created.

#### only_connect.py
This file contains the user-defined class `OnlyConnect`, which loads the file selected by the user into a variable and separates it into subobjects for each round, defined below. The classes for the subobjects are found in the directory `OnlyConnect/` of the program.

#### round_base.py
This file serves as an abstract base class for each round of *Only Connect*, providing the initialization process for most variations and defining up a play function for each.

#### connections.py
The first round of *Only Connect*, called in `commandLineProgram.py` with the `play()` function to start the game. Each team chooses a hieroglyph from the six available and must attempt to solve the puzzle within. Teams have 45 seconds to find the connection between four seemingly random clues. They start with one clue and may ask for more clues (up to a maximum of four) if time allows; however, the fewer clues seen, the more points earned by the team with a correct answer. If the team runs out of time or gives an incorrect answer, the opposing team has a chance to steal a bonus point after seeing all four clues.

#### sequences.py
The second round of *Only Connect*, called in `commandLineProgram.py` with the `play()` function to continue the game. As before, each team chooses a hieroglyph from the six available and must attempt to solve the puzzle within. Teams have 45 seconds to find the sequence between four seemingly random clues; however, instead of providing the sequence alone, the team must respond with what they would expect to see in the fourth clue. They start with one clue and may ask for more clues (up to a maximum of three this time) if time allows; however, the fewer clues seen, the more points earned by the team with a correct answer. Again, if the team runs out of time or gives an incorrect answer, the opposing team has a chance to steal a bonus point after seeing all three available clues.

#### connectingWall.py
The third round of *Only Connect*, called in `commandLineProgram.py` with the `play()` function to continue the game. This time, only two hieroglyphs are available for teams to choose from: once they have chosen their hieroglyph, the team is shown 16 random clues shuffled together which must be separated into four groups of four clues each as described in the background above. Teams have 180 seconds (and once two groups are successfully found, three lives to separate the last two groups) and earn one point for each group found. The team is then asked to provide the connection for each group, earning another point for each correct connection. If all groups are found and all connections are given, the team earns a bonus two points for a total of ten points.

#### missing_vowels.py & tiebreaker.py
The final round of *Only Connect*, called in `commandLineProgram.py` with the `play()` function to (potentially) finish the game. There is no timer for this round; the teams simply face off directly against each other to find the phrase hidden by the missing vowels and jumbled spaces. Each set of four clues is related to each other by a connection provided at the start of the set before revealing the first puzzle of the set. The team that rings in has an opportunity to give the answer, earning a point for their team; if they fail, however, they lose a point and the opposing team gets a free opportunity to make a guess at the puzzle (without losing a point if they're incorrect). After four full sets of four, the game ends and the team with the most points is the winner. If there is a tie, however, the tiebreaker object's `play()` function is called and provides the teams with a single missing vowels puzzle in a sudden death format: if the team rings in and gets it right, they win; if the team rings in and gets it wrong, they lose.

#### app.py
This file serves as the hub for all of the routes of the Flask application. It also keeps track of the primary global variables: the `teams` list, the `gameSession` files, the `questionsPlayed` list that tracks already played puzzles, and the `currentTeam` marker.

#### templates/
This directory houses all of the html files utilized for the program, inside of which is all of the original logic reimplemented and adapted into JavaScript code. The most important of these files are `round1puzzle.html`, `round2puzzle.html`, `round3puzzle.html` & `round3connections.html`, and `round4.html`, which hold the primary logic for each puzzle. Values are passed from app.py using Jinja to these HTML files to ensure a seamless translation.

### Potential Future Development:
As of right now, the Only Connect Host Assistant exists as a Flask application that is run directly from the terminal. I have already begun research into hosting the application online via Heroku and have made an attempt to begin that process already; however, I am running into some processing errors in the port that I am struggling to get past at my current knowledge level. In time, I am sure that I will be able to implement the app much more efficiently and smoothly.

In addition, there are types of puzzles used in rounds 1 and 2 of the official version of *Only Connect* that do not just utilize simple textual clues; additional types include picture clues (where pictures are shown instead of text) and music clues (where snippets of music are played instead of text; they are generally considered to be the hardest type of puzzle). I have already included in the question template a key for each question named "type" that can hold different values depending on the type of puzzle being shown. This key functionally does nothing for this version of the program, but in future iterations, the program could look at the type of each question and either make adjustments to the existing puzzle templates or run a different template altogether in order to implement the puzzles smoothly.