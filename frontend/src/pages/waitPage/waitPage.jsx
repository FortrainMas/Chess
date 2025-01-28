import { useEffect, useState } from 'react'
import { useNavigate, useParams } from "react-router";
import { API_ADR } from '../../api/api';

import { useDispatch, useSelector } from 'react-redux';

function WaitPages() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const user_id = useSelector((state) => state.user_id);

  let socket;

  useEffect(() => {
    socket = new WebSocket(`ws://${API_ADR}/api/v1/ws/game?game_id=${id}&user_id=${user_id}`);
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      if (data.status != "wait") {
        navigate("/game");
      }
    };
  });



  return (
    <>
        <h1>
            Your game id is {id}
        </h1>
        <h2>
            Waiting for opponent
        </h2>
    </>
  )
}

export default WaitPages
