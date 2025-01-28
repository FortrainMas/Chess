import { useState } from 'react'
import { useNavigate } from "react-router";
import './App.css'

import { useSelector, useDispatch } from 'react-redux';

import { createGameAPI, joinGameAPI } from './api/api';

import { setGameId } from './redux/store';

function App() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const user_id = useSelector((state) => state.user_id);

  const [gameCode, setGameCode] = useState("");

  const createGame = async () => {
    const game_id = await createGameAPI(user_id);
    sessionStorage.setItem("game_id", game_id);
    dispatch(setGameId(game_id));
    navigate("/wait/" + game_id);
  }

  const joinGame = async () => {
    const response = await joinGameAPI(gameCode, user_id);
    console.log(response);
    if (response.status != "success") {
      alert("Game not found or full");
      return;
    }
    else {
      sessionStorage.setItem("game_id", gameCode);
      dispatch(setGameId(gameCode));
      navigate("/wait/" + gameCode);
    }
  }

  return (
    <>
      <div className='create'>
        <button onClick={createGame}>Create the game</button>
      </div>
      <div className='join'>
        <input type="text" placeholder="Game ID" onChange={(e) => setGameCode(e.target.value)}/>
        <button onClick={joinGame}>Or join one</button>
      </div>
    </>
  )
}

export default App
