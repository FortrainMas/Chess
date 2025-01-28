import { configureStore, createSlice } from '@reduxjs/toolkit';


const createUserId = () => {
    const storedId = sessionStorage.getItem("user_id");
    if(storedId){
        return storedId;
    }

    const user_id = Math.floor(Math.random() * 100000).toString();
    sessionStorage.setItem("user_id", user_id);

    return user_id;
}

const counterSlice = createSlice({
    name: 'counter',
    initialState: { 
        user_id: createUserId(),
        game_id: null,
        color: "white",
        field: [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
    },
    reducers: {
        setGameId: (state, action) => { state.game_id = action.payload; },
        setColor: (state, action) => { state.color = action.payload; },
        setField: (state, action) => { state.field = action.payload; }
    },
});

export const { setGameId, setColor, setField } = counterSlice.actions;

const store = configureStore({ reducer: counterSlice.reducer });

export default store;
