import numpy as np
import time

startState = (4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, True)


def transition(state, action):
    newstate = list(state)
    player_turn = state[-1]
    last_pit = None

    if player_turn:
        point = action + 1
        times = state[action]
        newstate[action] = 0
        for _ in range(times):
            if point == 13:
                point = 0
            newstate[point] += 1
            last_pit = point
            point += 1
            if point == 14:
                point = 0
        extra_turn = last_pit == 6
    else:
        point = action + 8
        times = state[action + 7]
        newstate[action + 7] = 0
        for _ in range(times):
            if point == 6:
                point += 1
            if point == 14:
                point = 0
            newstate[point] += 1
            last_pit = point
            point += 1
            if point == 14:
                point = 0
        extra_turn = last_pit == 13

    if not extra_turn:
        newstate[-1] = not newstate[-1]

    return tuple(newstate)


def transitionIterating(state, action):
    newstate = list(state)
    player_turn = state[-1]
    last_pit = None

    if player_turn:
        point = action + 1
        times = state[action]
        newstate[action] = 0
        for _ in range(times):
            if point == 13:
                point = 0
            newstate[point] += 1
            last_pit = point
            time.sleep(0.5)
            yield tuple(newstate), action, point, 1
            point += 1
            if point == 14:
                point = 0
        extra_turn = last_pit == 6
    else:
        point = action + 8
        times = state[action + 7]
        newstate[action + 7] = 0
        for _ in range(times):
            if point == 6:
                point += 1
            if point == 14:
                point = 0
            newstate[point] += 1
            last_pit = point
            time.sleep(0.5)
            yield tuple(newstate), action + 7, point, 1
            point += 1
            if point == 14:
                point = 0
        extra_turn = last_pit == 13

    if not extra_turn:
        newstate[-1] = not newstate[-1]

    yield tuple(newstate), None, None, None


def getLegalActions(state):
    actions = []
    if state[-1] == True:
        for i in range(0, 6):
            if state[i] > 0:
                actions.append(i)
    else:
        for i in range(7, 13):
            if state[i] > 0:
                actions.append(i - 7)
    return actions


def isTerminal(state):
    if (np.sum(state[:6]) == 0) or (np.sum(state[7:13]) == 0):
        return True
    return False


def getSum(state):
    return np.sum(state[:7]), np.sum(state[7:-1])
