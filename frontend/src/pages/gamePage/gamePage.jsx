import { useEffect, useRef, useState } from 'react'
import { useParams } from "react-router";
import { API_ADR } from '../../api/api';

import { useDispatch, useSelector } from 'react-redux';
import GameField from '../../components/gameField';
import { setField, setGameId, setColor } from '../../redux/store';

function GamePage() {
  const dispatch = useDispatch();

  const [turn, setTurn] = useState(false);

  const user_id = useSelector((state) => state.user_id);
  const game_id = sessionStorage.getItem("game_id");
  const color = useSelector((state) => state.color);
  dispatch(setGameId(game_id))

  const socketRef = useRef(null); 

  useEffect(() => {
    const socket = new WebSocket(`ws://${API_ADR}/api/v1/ws/game?game_id=${game_id}&user_id=${user_id}`);
    socketRef.current = socket;

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);
      console.log(data["game_field"]);

      if(data["color"] == "black") {
        const rotateMatrix = (matrix) => {
            for (let i = 0; i < matrix.length; i++) {
              matrix[i].reverse();
          }
          matrix.reverse();
          return matrix;
        }

        rotateMatrix(data["game_field"]);
      }
      console.log("Must move");
      console.log(data["game_field"], data["color"])
      setTurn(data["user_turn"])
      dispatch(setField(data["game_field"]));
      dispatch(setColor(data["color"]))
    };

    // Cleanup on component unmount
    return () => {
      if (socket) {
        //socket.close();
        console.log("WebSocket closed");
      }
    };
  }, [API_ADR, game_id, user_id]); 
  const makeMove = (move) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      //If we play for black than moves have to be rotated
      if(color == "black"){
        move[0][0] = 7 - move[0][0]
        move[0][1] = 7 - move[0][1]
        move[1][0] = 7 - move[1][0]
        move[1][1] = 7 - move[1][1]
      }

      socketRef.current.send(
        JSON.stringify({
          from: move[0],
          to: move[1],
        })
      );
      console.log("Move sent:", move);
    } else {
      console.error("WebSocket is not open");
    }
  };


  return (
    <div style={{display: 'flex', flexDirection: 'row'}}>
        <GameField makeMove={makeMove}/>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'start', marginLeft: '70px'}}>
            <h1>
                Играем
            </h1>
            {
              turn ?
              (<h2 style={{color: '#646cff'}}>
                Your turn
              </h2>) :
              (<h2>
                Opp's turn
              </h2>)
            }
            <h2>
                Session id: {game_id}
            </h2>
            <h2>
                Your id: {user_id}
            </h2>
        </div>
    </div>
  )
}

export default GamePage
