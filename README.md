# Rock-Paper-Scissors Tournament Leaderboard

## Project Description
This project is a Flask-based web application that manages a persistent, multi-player Rock-Paper-Scissors tournament. It demonstrates the use of Python data structures (dictionaries and lists) and algorithms (searching and sorting) to track player statistics and display leaderboards.

A central dictionary (LEADERBOARD) stores all player data, while sorted list views are generated dynamically for the leaderboard. 

---

## Features
- Player registration
- 10-round Rock-Paper-Scissors games
- Winner retention between games
- Persistent leaderboard during runtime
- Leaderboard sorted alphabetically by player name
- Leaderboard sorted by cumulative score (descending)
- RESTFUL API design using Flask

---

## Technologies Used
- Python 3
- Flask
- HTML
- JavaScript (Fetch API)

---

## Project Structure

rps_tournament/
|--app.py
|--requirements.txt
|--templates/
 |   |--index.html
|-- README.md

---

## How to run the Project

### Prerequisites
- Python 3 installed
- Flask installed

### Setup Instructions

1. Clone the respository:
```bash 
git clone https://github.com/jakeshoffner15-art/rps-tournament.git

2. Navigate into the project folder:
bash

cd rps_tournament

3. Install dependencies:
bash 

pip install -r requirements.txt

4. Run the Flask application:
bash

python3 app.py

5. Open your browser and go to http://127.0.0.1:5000


API Endpoints

Register Player 

POST /api/player/register

Request Body:
{
    "name": "PlayerName"
}

Start Game 

POST /api/game/start

Request Body:
{
    "player1": "Alice",
    "player2": "Bob",
}

Play Round

POST /api/game/play_round

Request Body:
{
    "player1_choice": "rock"
}

Get Leaderboard

GET /api/leaderboard

Returns:

* Leaderboard sorted alphabetically by player name

* Leaderboard sorted by cumulative score (descending)

Notes

* Each game consists og 10 rounds

* The winner of each game is retained as Player 1 for the next match

* Leaderboard data persists while the server is running

Author 

Jake Shoffner 