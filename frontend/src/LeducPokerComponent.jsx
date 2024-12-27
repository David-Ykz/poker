import axios from 'axios';
import { useState } from 'react'
import j1 from './Assets/jack_of_hearts2.png'
import j2 from './Assets/jack_of_spades2.png'
import q1 from './Assets/queen_of_hearts2.png'
import q2 from './Assets/queen_of_spades2.png'
import k1 from './Assets/king_of_hearts2.png'
import k2 from './Assets/king_of_spades2.png'
import cardBack from './Assets/back_card.png'
import pokerTable from './Assets/poker_table.jpg'
import './LeducPokerComponent.css'

const serverUrl = 'http://localhost:5000';
let id = -1;
let playerTurn = -1;


function LeducPokerContainer() {
    const backgroundStyle = {
        backgroundImage: `url(${pokerTable})`,
        backgroundSize: 'cover', // Ensures the image covers the entire viewport
        backgroundRepeat: 'no-repeat', // Prevents the image from repeating
        backgroundPosition: 'center', // Centers the image
        width: '100vw', // Full viewport width
        height: '100vh', // Full viewport height
    };


    const [playerCard, setPlayerCard] = useState(-10000);
    const [botCard, setBotCard] = useState(-10000);
    const [communityCard, setCommunityCard] = useState(-10000);
    const [playerPot, setPlayerPot] = useState(0);
    const [botPot, setBotPot] = useState(0);
    const [pot, setPot] = useState(0);
    const [winner, setWinner] = useState(-10000);
    const [numPlayerWins, setNumPlayerWins] = useState(0);
    const [numBotWins, setNumBotWins] = useState(0);
    const [isTerminal, setIsTerminal] = useState(false);
//    let isTerminal = false;
//    const cardMappings = ['J', 'J', 'Q', 'Q', 'K', 'K']
    const cardMappings = [j1, j2, q1, q2, k1, k2]
    const [actionList, setActionList] = useState([])


    async function startNewGame() {
        const response = await axios.get(`${serverUrl}/new_game`);
        id = response.data.id;
        playerTurn = response.data.turn;
        await getGameState();
    }
    async function getGameState() {
        const response = await axios.post(`${serverUrl}/state`, {id: id});
        const data = response.data;
        console.log(data);
        setPlayerCard(data.Cards[playerTurn + 1])
        setBotCard(data.Cards[2 - playerTurn])
        setCommunityCard(data.Cards[0])
        setPlayerPot(data.Money[playerTurn])
        setBotPot(data.Money[1 - playerTurn])
        setPot(data.Pot)
        console.log(playerTurn);
        setActionList(data['Round 1 sequence'].concat(data['Round 2 sequence']))
        setIsTerminal(data.terminal);
        setWinner(data.winner);

        if (data.winner === playerTurn) {
            setNumPlayerWins(numPlayerWins + 1);
        } else if (data.winner === 1 - playerTurn) {
            setNumBotWins(numBotWins + 1);
        }
    }
    async function playerDecision(decision) {
        const decisionMap = ['Fold', 'Call', 'Raise']
        let copyActionList = actionList;
        copyActionList.push(decisionMap[decision])
        setActionList(copyActionList);
        await axios.put(`${serverUrl}/decision`, {id: id, decision: decision});
        await getGameState();
    }

    async function foldAction() {
        await playerDecision(0);
    }
    async function callAction() {
        await playerDecision(1);
    }
    async function raiseAction() {
        await playerDecision(2)
    }

    function getBotCard() {
        if (botCard === -10000) {
            return ''
        }
        if (isTerminal && actionList[actionList.length - 1] !== 'Fold') {
            return <img src={cardMappings[botCard]} className="botCard" />
        } else {
            return <img src={cardBack} className="botCard" />
        }
    }

    function isGameOver() {
        if (winner === playerTurn) {
            return <p>You won!</p>;
        } else if (winner === 1 - playerTurn) {
            return <p>The bot has won</p>
        } else if (winner === -1) {
            return <p>Draw</p>
        }
    }

    return (
        <div style={backgroundStyle}>
        
            <img src={cardMappings[playerCard]} className="playerCard" />
            {getBotCard()}
            <img src={cardMappings[communityCard]} className="communityCard" />
            <button onClick={startNewGame} className="newGameButton">Start New Game</button>
            {isTerminal || id === -1 ? <></> : (
            <div className="playerActions">
                <button onClick={foldAction}>Fold</button>
                <button onClick={callAction}>Call</button>
                <button onClick={raiseAction}>Raise</button>
            </div>
            )}

            {
                pot === 0 ? <></> : (
                    <div className="pot">
                        Pot: {pot === 0 ? '' : pot}
                    </div>
                )
            }
            <div className="pot">
                {isGameOver()}
            </div>
            <div className="botPanel">
                <p className="panelTitle">Bot:</p>
                Chips: {botPot}
                <br />
                # Wins: {numBotWins}
            </div>
            <div className="playerPanel">
                <p className="panelTitle">Player:</p>
                Chips: {playerPot}
                <br />
                # Wins: {numPlayerWins}
            </div>

        </div>
    )
}

export default LeducPokerContainer;
