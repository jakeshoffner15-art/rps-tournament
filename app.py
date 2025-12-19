from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# -------------------------------
# GLOBAL DATA STRUCTURES
# -------------------------------

LEADERBOARD = {}  # Central dictionary
CURRENT_GAME = {
    "player1": None,
    "player2": None,
    "round": 0,
    "scores": {}
}
LAST_WINNER = None

CHOICES = ["rock", "paper", "scissors"]

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def determine_winner(p1, p2):
    if p1 == p2:
        return "tie"
    if (
        (p1 == "rock" and p2 == "scissors") or
        (p1 == "paper" and p2 == "rock") or
        (p1 == "scissors" and p2 == "paper")
    ):
        return "player1"
    return "player2"

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# PLAYER REGISTRATION
# -------------------------------

@app.route("/api/player/register", methods=["POST"])
def register_player():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Player name required"}), 400

    if name not in LEADERBOARD:
        LEADERBOARD[name] = {
            "score": 0,
            "games_won": 0
        }

    return jsonify({"message": f"Player {name} registered successfully"})

# -------------------------------
# START GAME
# -------------------------------

@app.route("/api/game/start", methods=["POST"])
def start_game():
    global CURRENT_GAME, LAST_WINNER

    data = request.get_json()
    player1 = data.get("player1")
    player2 = data.get("player2")

    if not player1 or not player2:
        return jsonify({"error": "Two players required"}), 400

    CURRENT_GAME = {
        "player1": player1,
        "player2": player2,
        "round": 0,
        "scores": {
            player1: 0,
            player2: 0
        }
    }

    return jsonify({"message": "Game started"})

# -------------------------------
# PLAY ROUND
# -------------------------------

@app.route("/api/game/play_round", methods=["POST"])
def play_round():
    global CURRENT_GAME, LAST_WINNER

    if CURRENT_GAME["round"] >= 10:
        return jsonify({"error": "Game already finished"}), 400

    data = request.get_json()
    player1_choice = data.get("player1_choice")
    player2_choice = random.choice(CHOICES)

    result = determine_winner(player1_choice, player2_choice)

    CURRENT_GAME["round"] += 1

    if result == "player1":
        CURRENT_GAME["scores"][CURRENT_GAME["player1"]] += 1
        LEADERBOARD[CURRENT_GAME["player1"]]["score"] += 1
    elif result == "player2":
        CURRENT_GAME["scores"][CURRENT_GAME["player2"]] += 1
        LEADERBOARD[CURRENT_GAME["player2"]]["score"] += 1

    game_over = CURRENT_GAME["round"] == 10

    if game_over:
        p1 = CURRENT_GAME["player1"]
        p2 = CURRENT_GAME["player2"]
        p1_score = CURRENT_GAME["scores"][p1]
        p2_score = CURRENT_GAME["scores"][p2]

        if p1_score > p2_score:
            LEADERBOARD[p1]["games_won"] += 1
            LAST_WINNER = p1
        elif p2_score > p1_score:
            LEADERBOARD[p2]["games_won"] += 1
            LAST_WINNER = p2
        else:
            LAST_WINNER = None

    return jsonify({
        "round": CURRENT_GAME["round"],
        "player1_choice": player1_choice,
        "player2_choice": player2_choice,
        "scores": CURRENT_GAME["scores"],
        "game_over": game_over,
        "winner": LAST_WINNER
    })

# -------------------------------
# LEADERBOARD
# -------------------------------

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    players = []

    for name, stats in LEADERBOARD.items():
        players.append({
            "name": name,
            "score": stats["score"],
            "games_won": stats["games_won"]
        })

    by_name = sorted(players, key=lambda x: x["name"])
    by_score = sorted(players, key=lambda x: x["score"], reverse=True)

    return jsonify({
        "by_name": by_name,
        "by_score": by_score
    })

# -------------------------------
# RUN SERVER
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)