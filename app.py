from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4
from flask_debugtoolbar import DebugToolbarExtension

from boggle import BoggleGame

GAME_ID_KEY = "gameId"
WORD_KEY = "word"

app = Flask(__name__)
app.config['SECRET_KEY'] = "something secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify(gameId=game_id, board=game.board)

@app.post("/api/score-word")
def score_word():
    """Check if the word is valid and score it"""
    game = games[request.json[GAME_ID_KEY]]
    word = request.json[WORD_KEY].upper()

    if not game.is_word_in_word_list(word):
        return jsonify({ "result": "not-word" })
    elif not game.check_word_on_board(word):
        return jsonify({ "result": "not-on-board" })
    else:
        score = game.play_and_score_word(word)
        return jsonify({ "result": "ok" })