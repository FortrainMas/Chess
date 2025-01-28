from random import randint
import uuid
import json

from fastapi import APIRouter, status, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


from db import games


router = APIRouter()


class CreateGameRequest(BaseModel):
    user_id: str

@router.post("/game/create", status_code=status.HTTP_200_OK)
def create_game(payload: CreateGameRequest):
    game_id = games.create_game(payload.user_id)
    print(f"Create game with id = {game_id}")
    games.log_game(game_id)
    return {
        "status": "success",
        "game_id": game_id
    }





class JoinGameRequest(BaseModel):
    game_id: str
    user_id: str

@router.post("/game/join", status_code=status.HTTP_200_OK)
async def join_game(payload: JoinGameRequest):
    game_id = payload.game_id
    user_id = payload.user_id

    game = games.get_game(game_id)
    games.log_game(game_id)
    if not (game is None) and len(game["players"]) < 2 and game["players"][0] != user_id:
        if randint(0, 1) == 0:
            game["players"].insert(0, user_id)
        else:
            game["players"].append(user_id)

        games.log_game(game_id)

        return {"status":"success", "status_code": 200}
    else:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")



@router.websocket("/ws/game")
async def game_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = websocket.query_params.get("user_id")
    game_id = websocket.query_params.get("game_id")
    print(f"Openned connection for {user_id} in game: {game_id}")

    game = games.get_game(game_id)
    if game is None:
        print("Game ", game_id, "not found")
        print("ERROR ERROR ERROR")
        av_games = " ".join(games.available_games())
        await websocket.send_json({"status": "not found the game " + game_id +" " + av_games})
        await websocket.close()
        return
    

    if len(game["players"]) == 1:
        games.add_connection(game_id, user_id, websocket)
        await websocket.send_json({"status": "wait"})

    if len(game["players"]) == 2:
        games.add_connection(game_id, user_id, websocket)
        for player in game["players"]:
            await game["connections"][player].send_json(games.game_status(game_id, player))

        for conn in game["connections"]["others"]:
           await  conn.send_json(games.game_status(game_id, game["player"][0]))


    try:
        while 1:
            data = await websocket.receive_text()
            data = json.loads(data)
            games.make_move(game_id, user_id, [data["from"], data["to"]])
            print(data)
            print(game)
            for player in game["players"]:
                await game["connections"][player].send_json(games.game_status(game_id, player))

            for conn in game["connections"]["others"]:
               await  conn.send_json(games.game_status(game_id, game["player"][0]))

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected.")
        game["connections"].remove(websocket)  
        await websocket.close()
        await websocket.send_json({"status": "disconnected"})



class GetGameRequest(BaseModel):
    game_id: str
    user_id: str

@router.get("/game/{game_id}")
def get_game(payload: GetGameRequest):
    game_id = payload.game_id
    user_id = payload.user_id

    game = games.get_game(game_id)
    
    if game is None:
        status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail="Game not found")
    
    if len(game["players"]) == 2:
        result = {
            "status":"success",
            "game_field": game["game_field"],
            "game_turn": game["game_turn"],
            "side": "white" if game["players"].index(user_id) == 0 else "black" if game["players"].index(user_id) == 1 else "none"
        }
        return result
    
    status_code = status.STATUS_204_NO_CONTENT
    raise HTTPException(status_code=status_code, detail="Waiting for opponent")
    

