import os
import sys

from flask import Flask, jsonify, render_template, url_for

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.minesweeper import Minesweeper


app = Flask(__name__)

game = Minesweeper(5, 5, 3)

def get_game_state() -> dict:
    if game.game_over:
        board = game.get_full_board()
        message = "🥲 Game Over! 🥲"
    elif game.is_winner():
        board = game.get_board()
        message = "🔥 You Win! 🔥"
    else:
        board = game.get_board()
        message = ""

    return {
        "board": board,
        "message": message,
        "game_over": game.game_over,
        "is_winner": game.is_winner(),
        "rows": game.rows,
        "cols": game.cols,
    }

@app.route("/")
def index():
    return render_template("index.html", initial_state=get_game_state())

@app.route("/api/state")
def api_state():
    return jsonify(get_game_state())

@app.route("/api/reveal/<int:row>/<int:col>", methods=["POST"])
def api_reveal(row: int, col: int):
    game.reveal(row, col)
    return jsonify(get_game_state())

@app.route("/api/flag/<int:row>/<int:col>", methods=["POST"])
def api_flag(row: int, col: int):
    game.toggle_flag(row, col)
    return jsonify(get_game_state())

@app.route("/api/restart", methods=["POST"])
def api_restart():
    game.restart()
    return jsonify(get_game_state())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)