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
        extra_turn = False
        try:
            while True:
                if self.stop_iteration:
                    break
                result = next(f)
                if len(result) == 5:
                    self.state, start, end, num, extra_turn = result
                else:
                    self.state, start, end, num = result
                if start is None:
                    break
                self.UI.paintMove(start, end, num)
                last_pit = end
        except StopIteration:
            pass

        time.sleep(1)

        if extra_turn:
            print("Player gets another turn")
            return ""  # Pemain mendapatkan giliran tambahan

        self.pointer = 0 if self.state[-1] else 1

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
