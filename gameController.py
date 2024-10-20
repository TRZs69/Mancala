import numpy as np
from world import *
import time


class game:
    def __init__(self, agent1, agent2):
        self.agents = [agent1, agent2]
        self.state = startState
        self.pointer = 0

    def getState(self):
        return self.state

    def judge(self):
        p1, p2 = getSum(self.state)
        if p1 > p2:
            return "P1 wins!"
        if p1 == p2:
            return "    Draw!"
        if p1 < p2:
            return "P2 wins!"

    def play(self):
        action = self.agents[self.pointer].play(self.state)
        self.state = transition(self.state, action)
        self.pointer = 0 if self.state[-1] else 1
        if isTerminal(self.state):
            return self.judge(), action
        else:
            return "", action


class gameWithGUI(game):
    def __init__(self, agent1, agent2, UI):
        self.UI = UI
        self.stop_iteration = False
        super().__init__(agent1, agent2)

    def move(self, action):
        print("Move")
        f = transitionIterating(self.state, action)
        last_pit = None
        try:
            while True:
                if self.stop_iteration:
                    break
                result = next(f)
                if result[1] is None:
                    break
                self.state, start, end, num = result
                self.UI.paintMove(start, end, num)
                last_pit = end
        except StopIteration:
            pass

        time.sleep(1)

        # Check if the last seed landed in the player's store
        if self.state[-1]:  # Player 1's turn (True)
            if last_pit == 6:  # Last seed landed in Player 1's store
                print("Player 1 gets another turn")
                return ""  # Player 1 gets another turn
        else:  # Player 2's turn (False)
            if last_pit == 13:  # Last seed landed in Player 2's store
                print("Player 2 gets another turn")
                return ""  # Player 2 gets another turn

        # Switch turns if the last seed did not land in the store
        self.pointer = 0 if not self.state[-1] else 1
        self.state = self.state[:-1] + (not self.state[-1],)

        if isTerminal(self.state):
            return self.judge()
        else:
            return ""

    def play(self):
        print("Play")
        judge = ""
        while True:
            if self.stop_iteration:
                break
            if not (self.agents[self.pointer] is None):
                action = self.agents[self.pointer].play(self.state)
                judge = self.move(action)
                if judge != "":
                    self.UI.uiTerminal(self.judge())
                    break
            else:
                self.UI.enableManualAction(self.state[-1])
                break

    def manPlay(self, action):
        if action in getLegalActions(self.state):
            self.UI.disableManualAction(self.state[-1])
            judge = self.move(action)
            if judge != "":
                self.UI.uiTerminal(self.judge())
            else:
                self.play()

    def reset(self):
        self.stop_iteration = True
        time.sleep(0.1)
        self.state = startState
        self.pointer = 0
