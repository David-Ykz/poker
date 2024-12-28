import json
import pyspiel
import pickle
import numpy as np
from random import randint
import redis
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

r = redis.Redis(
    host=os.getenv('HOST'),
    port=os.getenv('PORT'),
    decode_responses=True,
    username=os.getenv('REDIS_USERNAME'),
    password=os.getenv('PASSWORD'),
)
game = pyspiel.load_game('leduc_poker', {'players': 2})
with open('cfr_policy.pkl', "rb") as f:
    average_policy = pickle.load(f)

def applyRandomAction(state):
    outcomes = state.chance_outcomes()
    action_list, probs = zip(*outcomes)
    action = np.random.choice(action_list, p=probs)
    state.apply_action(action)

def newGame():
    state = game.new_initial_state()
    playerTurn = randint(0, 1)
    id = str(uuid.uuid4())
    saveGame(id, state, playerTurn, -10000)
    return id, playerTurn

def getGame(id):
    data = json.loads(r.get(id))
    state = game.deserialize_state(data['state'])
    print(state)
    playGame(state, data['playerTurn'], 1 - data['playerTurn'])
    return state, data['playerTurn'], data['winner']

def saveGame(id, state, playerTurn, winner):
    data = {'state': state.serialize(), 'playerTurn': playerTurn, 'winner': winner}
    r.set(id, json.dumps(data))

def playGame(state, playerTurn, aiTurn):
    while not (state.current_player() == playerTurn or state.is_terminal()):
        if state.is_chance_node():
            applyRandomAction(state)
        if state.current_player() == aiTurn:
            aiDecision(state, aiTurn)

def aiDecision(state, aiTurn):
    if state.current_player() == aiTurn and not state.is_chance_node():
        legal_actions = state.legal_actions()
        action_probs = [
            average_policy.action_probabilities(state, player_id=aiTurn)[a]
            for a in legal_actions
        ]
        action = np.random.choice(legal_actions, p=action_probs)
        state.apply_action(action)

def playerDecision(state, playerTurn, decision):
    print(state)
    print(playerTurn)
    print(decision)
    if state.current_player() == playerTurn and not state.is_chance_node():
        state.apply_action(decision)


def processState(state):
    result = {}
    result["terminal"] = state.is_terminal()
    if state.is_terminal():
        returns = state.returns()
        if returns[0] == returns[1]:
            result["winner"] = -1
        else:
            result["winner"] = state.returns().index(max(state.returns()))
    else:
        result["winner"] = -10000
    state = str(state)
    for line in state.strip().split("\n"):
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        
        if key.startswith("Money"):
            result["Money"] = list(map(int, value.split()))
        elif key.startswith("Cards"):
            result["Cards"] = list(map(int, value.split()))
        elif "sequence" in key:
            result[key] = [v.strip() for v in value.split(",")] if value else []
        else:
            try:
                result[key] = int(value)
            except ValueError:
                result[key] = value
    return result
