import numpy as np
import time

startState = (4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, True)


def transition(state, action):
    newstate = list(state)
    player_turn = state[-1]
    last_pit = None
    extra_turn = False

    if player_turn:
        point = action + 1
        times = state[action]
        newstate[action] = 0
        for i in range(times):
            if point == 13:
                point = 0
            if point == 13:  # Lewati rumah lawan
                point = 0
            pit_was_empty = newstate[point] == 0
            newstate[point] += 1
            last_pit = point
            point += 1
            if point == 14:
                point = 0
        if last_pit == 6:
            extra_turn = True
        else:
            extra_turn = False
            if (
                (last_pit >= 0 and last_pit <= 5)
                and pit_was_empty
                and newstate[last_pit] == 1
                and newstate[12 - last_pit] > 0
            ):
                newstate[6] += newstate[12 - last_pit] + newstate[last_pit]
                newstate[12 - last_pit] = 0
                newstate[last_pit] = 0
    else:
        point = action + 8
        times = state[action + 7]
        newstate[action + 7] = 0
        for i in range(times):
            if point == 6:
                point += 1
            if point == 14:
                point = 0
            pit_was_empty = newstate[point] == 0
            newstate[point] += 1
            last_pit = point
            point += 1
            if point == 14:
                point = 0
        if last_pit == 13:
            extra_turn = True
        else:
            extra_turn = False
            if (
                (last_pit >= 7 and last_pit <= 12)
                and pit_was_empty
                and newstate[last_pit] == 1
                and newstate[12 - last_pit] > 0
            ):
                newstate[13] += newstate[12 - last_pit] + newstate[last_pit]
                newstate[12 - last_pit] = 0
                newstate[last_pit] = 0

    if not extra_turn:
        newstate[-1] = not newstate[-1]

    return tuple(newstate)


def transitionIterating(state, action):
    newstate = list(state)
    player_turn = state[-1]
    last_pit = None
    extra_turn = False

    if player_turn:
        point = action + 1
        times = state[action]
        newstate[action] = 0
        for i in range(times):
            if point == 13:
                point = 0
            if point == 13:
                point = 0
            pit_was_empty = newstate[point] == 0
            newstate[point] += 1
            last_pit = point
            time.sleep(0.5)
            yield tuple(newstate), action, point, 1
            point += 1
            if point == 14:
                point = 0
        if last_pit == 6:
            extra_turn = True
        else:
            extra_turn = False
            if (
                (last_pit >= 0 and last_pit <= 5)
                and pit_was_empty
                and newstate[last_pit] == 1
                and newstate[12 - last_pit] > 0
            ):
                time.sleep(0.5)
                captured_seeds = newstate[12 - last_pit]
                newstate[6] += captured_seeds + newstate[last_pit]
                newstate[last_pit] = 0
                newstate[12 - last_pit] = 0
                yield tuple(newstate), last_pit, 6, 1
                yield tuple(newstate), 12 - last_pit, 6, captured_seeds
    else:
        point = action + 8
        times = state[action + 7]
        newstate[action + 7] = 0
        for i in range(times):
            if point == 6:
                point += 1
            if point == 14:
                point = 0
            pit_was_empty = newstate[point] == 0
            newstate[point] += 1
            last_pit = point
            time.sleep(0.5)
            yield tuple(newstate), action + 7, point, 1
            point += 1
            if point == 14:
                point = 0
        if last_pit == 13:
            extra_turn = True
        else:
            extra_turn = False
            if (
                (last_pit >= 7 and last_pit <= 12)
                and pit_was_empty
                and newstate[last_pit] == 1
                and newstate[12 - last_pit] > 0
            ):
                time.sleep(0.5)
                captured_seeds = newstate[12 - last_pit]
                newstate[13] += captured_seeds + newstate[last_pit]
                newstate[last_pit] = 0
                newstate[12 - last_pit] = 0
                yield tuple(newstate), last_pit, 13, 1
                yield tuple(newstate), 12 - last_pit, 13, captured_seeds

    if not extra_turn:
        newstate[-1] = not newstate[-1]

    yield tuple(newstate), None, None, None, extra_turn


def getLegalActions(state):
    actions = []
    if state[-1]:
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
