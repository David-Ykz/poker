import axios from 'axios';
import { useState } from 'react'

const serverUrl = 'http://localhost:5000';
let id = -1;


function LeducPokerContainer() {

    const [playerCard, setPlayerCard] = useState(0)
    const [botCard, setBotCard] = useState(0)
    const [communityCard, setCommunityCard] = useState(0)
    
    async function startNewGame() {
        const response = await axios.get(`${serverUrl}/new_game`);
        id = parseInt(response.data);
    }
    async function getGameState() {
        const response = await axios.post(`${serverUrl}/state`, {id: id});
        console.log(response.data);
    }

    return (
        <div>
            <button onClick={startNewGame}>Start New Game</button>
            <button onClick={getGameState}>Get Game State</button>
        </div>
    )
}

export default LeducPokerContainer;
