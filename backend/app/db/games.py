import uuid
from fastapi import WebSocket
from utils import chess_utils

games = {}

def create_game(user_id):
    game_id = str(uuid.uuid4())[:8]
    game_field = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

    game = {
        "game_id": game_id,
        "game_field": game_field,
        "game_turn": "white",
        "players": [user_id],
        "connections": {}
    }

    game["connections"]["others"] = []
    games[game_id] = game
    return game_id

def add_connection(game_id, user_id, webSocket):
    if not game_id in games:
        print(f"Attempt to add connection by {user_id} in game {game_id} which does not exist")
        return False
    game = games[game_id]
    if user_id in game["players"]:
        game["connections"][user_id] = webSocket
        print(f"Set connection from {user_id} in game {game_id}")
    else:
        game["connections"]["others"].append(webSocket)
        print(f"Added connection from {user_id} in game {game_id} as others")
    return True

def remove_connection(game_id, user_id, webSocket):
    pass

def game_status(game_id, user_id):
    game = games[game_id]

    game_field = game["game_field"]
    turn = game["game_turn"]
    user_color = "white" if game["players"].index(user_id) == 0 else "black"

    return {
        "status": "play", 
        "game_field": game_field, 
        "turn": turn, 
        "color": user_color,
        "user_turn": user_color == turn
    }
    
def make_move(game_id, user_id, move):
    if not game_id in games:
        print(f"Attempt to send move to wrong game id {game_id}")
        return False
    game = games[game_id]
    
    if not user_id in game["players"]:
        print(f"Attempt to send move from wrong user_id {user_id}. Allowed: {game["players"]}")
        return False
    
    user_color = "white" if game["players"].index(user_id) == 0 else "black"
    if user_color != game["game_turn"]:
        print(f"User color is wrong {user_color} and current turn is {game["game_turn"]}")
        return False
    
    if chess_utils.allowed_move(game["game_field"], game["game_turn"], move) == False:
        return False

    field = game["game_field"]
    piece = field[move[0][0]][move[0][1]]
    field[move[1][0]][move[1][1]] = piece
    field[move[0][0]][move[0][1]] = ""

    game["game_turn"] = "black" if game["game_turn"] == "white" else "white"



def get_game(game_id):
    if game_id not in games:
        return None
    return games[game_id]

def available_games():
    return list(games.keys())


def log_game(game_id):
    if game_id in games:
        game = games[game_id]
        print(f"Log for game {game_id}")
        print(f"{len(game["players"])} players: {game['players']}")
    elif game_id not in games:
        print(f"Game {game_id} not found")



