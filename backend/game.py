import pyspiel
import pickle
import numpy as np
from random import randint

existingGames = []
with open('cfr_policy.pkl', "rb") as f:
    average_policy = pickle.load(f)

def applyRandomAction(state):
    outcomes = state.chance_outcomes()
    action_list, probs = zip(*outcomes)
    action = np.random.choice(action_list, p=probs)
    state.apply_action(action)

def initializeNewGame():
    game = pyspiel.load_game('leduc_poker', {'players': 2})
    state = game.new_initial_state()
    playerTurn = randint(0, 1)
    applyRandomAction(state)
    applyRandomAction(state)
    for i in range(len(existingGames)):
        if existingGames[i] == None:
            existingGames[i] = {'state': state, 'playerTurn': playerTurn}
            return i, playerTurn
    existingGames.append({'state': state, 'playerTurn': playerTurn})
    return len(existingGames) - 1, playerTurn

def getGameState(id):
    print(existingGames[id])
    aiTurn = 1 - existingGames[id]['playerTurn']
    state = existingGames[id]['state']

    if state.is_terminal():
        print("terminal state")
        return processState(state)

    playGame(id)

    if state.is_chance_node():
        applyRandomAction(state)

    return processState(state)

def playGame(id):
    state = existingGames[id]['state']
    playerTurn = existingGames[id]['playerTurn']
    aiTurn = 1 - playerTurn
    while not (state.current_player() == playerTurn or state.is_terminal()):
        if state.is_chance_node():
            applyRandomAction(state)
        if state.current_player() == aiTurn:
            print("ai made move")
            applyDecision(id, -1)


def applyDecision(id, decision):
    state = existingGames[id]['state']
    playerTurn = existingGames[id]['playerTurn']
    aiTurn = 1 - playerTurn
    if decision == -1:
        legal_actions = state.legal_actions()
        action_probs = [
            average_policy.action_probabilities(state, player_id=aiTurn)[a]
            for a in legal_actions
        ]
        action = np.random.choice(legal_actions, p=action_probs)
        state.apply_action(action)

        print("ai made move", action)
        return action
    elif state.current_player() == playerTurn and not state.is_chance_node():
        state.apply_action(decision)
        print("player made move", decision)
        return -1

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
