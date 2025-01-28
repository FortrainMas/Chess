import axios from "axios";

export const API_ADR = "127.0.0.1:8000";
export const API_PATH = `http://${API_ADR}/api/v1/`;


export const createGameAPI = async (userID) => {
  const response = await axios.post(`${API_PATH}game/create`, { user_id: userID });
  return response.data.game_id;
};

export const joinGameAPI = async (gameID, userID) => {
  try {
    await axios.post(`${API_PATH}game/join`, { game_id: gameID, user_id: userID });
    return { status: "success" };
  } catch (e) {
    console.error(e.response?.data || e.message); // Log the error details
    return { status: "error" };
  }
};
