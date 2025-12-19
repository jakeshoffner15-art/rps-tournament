from flask import Flask, render_template

app = Flask(__name__)

LEADERBOARD = {}

CURRENT_GAME = {
    "player1": None,
    "player2": None,
    "round": 0,
    "scores": {}
}

LAST_WINNER = None


@app.route("/")
def home():
    return render_template("index.html")

from flask import jsonify

@app.route("/api/leaderboard")
def leaderboard():
    
    players = []
    for name, stats in LEADERBOARD.items():
        players.append({
            "name": name,
            "score": stats["score"],
            "games_won": stats["games_won"]
        })

    by_name = sorted(players, key=lambda x: x["name"].lower())

    by_score = sorted(players, key=lambda x: x["score"], reverse=True)

    return jsonify({
        "by_name": by_name,
        "by_score": by_score
    })

from flask import request

@app.route("/api/player/register", methods=["POST"])
def register_player():
    data = request.get_json()
    player_name = data.get("name")

    if not player_name:
        return jsonify({"error:" "Player name is required"}), 400

    if player_name not in LEADERBOARD:
        LEADERBOARD[player_name] = {"score": 0, "games_won": 0}

    return jsonify({"message": f"Player '{player_name}' registered successfully", "leaderboard": LEADERBOARD})

import random

def determine_winner(p1_choice, p2_choice):
    if p1_choice == p2_choice:
        return None
    if (
        (p1_choice == "rock" and p2_choice == "scissors") or
        (p1_choice == "scissors" and p2_choice == "paper") or
        (p1_choice == "paper" and p2_choice == "rock")
    ):
        return "player1"
    return "player2"

@app.route("/api/game/start", methods=["POST"])
def start_game():
    data = request.get_json()

    global LAST_WINNER

    player1 = LAST_WINNER if LAST_WINNER else data.get("player1")
    player2 = data.get("player2")

    if not player1 or not player2:
        return jsonify({"error": "Both player names are required"}), 400

    for player in [player1, player2]:
        if player not in LEADERBOARD:
            LEADERBOARD[player] = {"score": 0, "games_won": 0}

    CURRENT_GAME["player1"] = player1
    CURRENT_GAME["player2"] = player2
    CURRENT_GAME["round"] = 0
    CURRENT_GAME["scores"] = {
        player1: 0,
        player2: 0
    } 

    return jsonify({
        "message": "New 10-round game started",
        "player1": player1,
        "player2": player2,
        "retained_winner": LAST_WINNER is not None
    })

@app.route("/api/game/play_round", methods=["POST"])
def play_round():
    global LAST_WINNER

    if CURRENT_GAME["round"] >= 10:
        return jsonify({"error": "Game over. Start a new game"})
    
    data = request.json
    p1_choice = data["player1_choice"]
    p2_choice = random.choice(["rock", "paper", "scissors"])

    if p1_choice == p2_choice:
        winner = "tie"
    elif (
        (p1_choice == "rock" and p2_choice == "scissors") or
        (p1_choice == "paper" and p2_choice == "rock") or
        (p1_choice == "scissors" and p2_choice == "paper")
    ):
        winner = CURRENT_GAME["player1"]
        CURRENT_GAME["scores"][winner] += 1
    else:
        winner = CURRENT_GAME["player2"]
        CURRENT_GAME["scores"][winner] += 1

    CURRENT_GAME["round"] += 1

    if CURRENT_GAME["round"] == 10:
        p1 = CURRENT_GAME["player1"]
        p2 = CURRENT_GAME["player2"]

        if CURRENT_GAME["scores"][p1] > CURRENT_GAME["scores"][p2]:
            LAST_WINNER = p1
            LEADERBOARD[p1]["games_won"] += 1
        elif CURRENT_GAME["scores"][p2] > CURRENT_GAME["scores"][p1]:
            LAST_WINNER = p2
            LEADERBOARD[p2]["games_won"] += 1
        else:
            LAST_WINNER = None

        return jsonify({
            "round": CURRENT_GAME["round"],
            "player1_choice": p1_choice,
            "player2_choice": p2_choice,
            "scores": CURRENT_GAME["scores"],
            "game_over": True,
            "winner": LAST_WINNER
        })

   return jsonify({
       "round": CURRENT_GAME["round"],
       "player1_choice": p1_choice,
       "player2_choice": p2_choice,
       "scores": CURRENT_GAME["scores"],
       "game_over": False
   })


    
if __name__ == "__main__":
    app.run(debug=True)
