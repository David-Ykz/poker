from flask import Flask, jsonify, request
from flask_cors import CORS
from game import getGame, saveGame, newGame, processState, playerDecision

app = Flask(__name__)
CORS(app)

@app.route('/new_game')
def initializeNewGame():
    id, turn = newGame()
    return {'id': id, 'turn': turn}

@app.route('/state', methods=["POST"])
def getState():
    id = request.json['id']
    state, playerTurn, winner = getGame(id)
    processedState = processState(state)
    if processedState['terminal']:
        winner = processedState['winner']
    saveGame(id, state, playerTurn, winner)
    return processedState

@app.route('/decision', methods=["PUT"])
def processPlayerDecision():
    id = request.json['id']
    decision = request.json['decision']
    state, playerTurn, winner = getGame(id)
    playerDecision(state, playerTurn, decision)
    saveGame(id, state, playerTurn, winner)
    return ""

app.run(debug=True)
