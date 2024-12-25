from flask import Flask, jsonify, request
from flask_cors import CORS
from game import initializeNewGame, getGameState, applyDecision

app = Flask(__name__)
CORS(app)

@app.route('/new_game')
def newGame():
    return str(initializeNewGame())

@app.route('/state', methods=["POST"])
def getState():
    id = request.json['id']
    return getGameState(id)

@app.route('/decision', methods=["PUT"])
def processPlayerDecision():
    id = request.json['id']
    decision = request.json['decision']
    applyDecision(id, decision)
    applyDecision(id, -1)

app.run(debug=True)
