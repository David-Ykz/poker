import pyspiel
import pickle
import numpy as np

existingGames = []
with open('cfr_policy.pkl', "rb") as f:
    average_policy = pickle.load(f)

def applyRandomAction(state):
    outcomes = state.chance_outcomes()
    print(outcomes)
    action_list, probs = zip(*outcomes)
    print(action_list)
    action = np.random.choice(action_list, p=probs)
    print(action)
    state.apply_action(action)

def initializeNewGame():
    game = pyspiel.load_game('leduc_poker', {'players': 2})
    state = game.new_initial_state()
    applyRandomAction(state)
    applyRandomAction(state)
    for i in range(len(existingGames)):
        if existingGames[i] == None:
            existingGames[i] = state
            return i
    existingGames.append(state)
    return len(existingGames) - 1

def getGameState(id):
    return processState(str(existingGames[id]))

def getCommunityCard(id):
    state = existingGames[id]
    applyRandomAction(state)

def applyDecision(id, decision):
    state = existingGames[id]
    if decision == -1:
        legal_actions = state.legal_actions()
        action_probs = [
            average_policy.action_probabilities(state, player_id=0)[a]
            for a in legal_actions
        ]
        action = np.random.choice(legal_actions, p=action_probs)
        state.apply_action(action)
        return action
    else:
        state.apply_action(decision)
        return -1

def processState(state):
    result = {}
    for line in state.strip().split("\n"):
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        
        # Parse specific keys for structured data
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
