from world import *
from gameController import *
import numpy as np
import torch


class minimaxAgent:
    HUMAN = 0
    MINIMAX = 1
    ABPRUNE = 2
    MEANVALUE = 3

    def __init__(self, playerType=MEANVALUE, ply=2):
        self.type = playerType
        self.ply = ply

    def minimaxMove(self, state, ply):
        best_score = float("-inf")
        best_move = None
        turn = self
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if isTerminal(next_state):
                score = self.evaluateTerminal(next_state)
            else:
                if next_state[-1] == state[-1]:  # Player gets another turn
                    score = self.maxValue(next_state, ply - 1, turn)
                else:
                    score = self.minValue(next_state, ply - 1, turn)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def maxValue(self, state, ply, turn):
        if isTerminal(state):
            return self.evaluateTerminal(state)
        if ply == 0:
            return turn.score(state)
        score_max = float("-inf")
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if next_state[-1] == state[-1]:  # Player gets another turn
                s = self.maxValue(next_state, ply - 1, turn)
            else:
                s = self.minValue(next_state, ply - 1, turn)
            if s > score_max:
                score_max = s
        return score_max

    def minValue(self, state, ply, turn):
        if isTerminal(state):
            return self.evaluateTerminal(state)
        if ply == 0:
            return turn.score(state)
        score_min = float("inf")
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if next_state[-1] == state[-1]:  # Opponent gets another turn
                s = self.minValue(next_state, ply - 1, turn)
            else:
                s = self.maxValue(next_state, ply - 1, turn)
            if s < score_min:
                score_min = s
        return score_min

    def evaluateTerminal(self, state):
        p1_sum, p2_sum = getSum(state)
        if p1_sum > p2_sum:
            return 999 if state[-1] else -999
        elif p1_sum < p2_sum:
            return -999 if state[-1] else 999
        else:
            return 0

    def alphabetamove(self, state, ply):
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        turn = self
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if isTerminal(next_state):
                score = self.evaluateTerminal(next_state)
            else:
                if next_state[-1] == state[-1]:
                    score = self.maxABValue(next_state, ply - 1, turn, alpha, beta)
                else:
                    score = self.minABValue(next_state, ply - 1, turn, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = move
            if alpha >= beta:
                break
        return best_move

    def maxABValue(self, state, ply, turn, alpha, beta):
        if isTerminal(state):
            return self.evaluateTerminal(state)
        if ply == 0:
            return turn.score(state)
        score = float("-inf")
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if next_state[-1] == state[-1]:
                s = self.maxABValue(next_state, ply - 1, turn, alpha, beta)
            else:
                s = self.minABValue(next_state, ply - 1, turn, alpha, beta)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score

    def minABValue(self, state, ply, turn, alpha, beta):
        if isTerminal(state):
            return self.evaluateTerminal(state)
        if ply == 0:
            return turn.score(state)
        score = float("inf")
        for move in getLegalActions(state):
            next_state = transition(state, move)
            if next_state[-1] == state[-1]:
                s = self.minABValue(next_state, ply - 1, turn, alpha, beta)
            else:
                s = self.maxABValue(next_state, ply - 1, turn, alpha, beta)
            if s < score:
                score = s
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def score(self, state):
        p1_store = state[6]
        p2_store = state[13]
        if state[-1]:
            return p1_store - p2_store + (np.sum(state[:6]) - np.sum(state[7:13]))
        else:
            return p2_store - p1_store + (np.sum(state[7:13]) - np.sum(state[:6]))

    def play(self, state):
        if self.type == self.MINIMAX:
            return self.minimaxMove(state, self.ply)
        elif self.type == self.ABPRUNE:
            return self.alphabetamove(state, self.ply)
        elif self.type == self.MEANVALUE:
            return self.randomMove(state, self.ply)
        else:
            return self.randomMove(state, self.ply)

    def randomMove(self, state, ply):
        legal_moves = getLegalActions(state)
        return np.random.choice(legal_moves)


class minimaxAgentML(minimaxAgent):
    HUMAN = 0
    MINIMAX = 1
    ABPRUNE = 2
    MEANVALUE = 3

    def __init__(self, playerType=MEANVALUE, ply=2):
        super().__init__(playerType, ply)
        self.model = torch.load("model")

    def normalization(self, state):
        state = np.array([state])
        means = np.array(
            [
                [
                    1.6831783766488317,
                    1.920861792019031,
                    2.0142274382885192,
                    2.099035853596613,
                    2.223753461124363,
                    2.3957063177909617,
                    11.785342967427546,
                    1.6735022578976735,
                    1.916759244860047,
                    2.0219108486903,
                    2.095517344002846,
                    2.2175399572616663,
                    2.4000639932270524,
                    11.760987284327173,
                ]
            ]
        )
        stds = np.array(
            [
                [
                    2.2965555781311355,
                    2.5959722979902446,
                    2.6847805719174693,
                    2.745832204831912,
                    2.8541587526372196,
                    2.979194156904659,
                    6.298355040135411,
                    2.3016301665931884,
                    2.5987004084829355,
                    2.6955533493313037,
                    2.738373835337156,
                    2.8395994049082107,
                    2.9842425056695507,
                    6.301167592999449,
                ]
            ]
        )
        state = (state - means) / stds
        return state.tolist()

    def score(self, state):
        state_features = list(state[:-1])
        normalized_state = self.normalization(state_features)
        with torch.no_grad():
            out = self.model(torch.tensor(normalized_state, dtype=torch.float32))
        if state[-1]:
            return out.item()
        else:
            return -out.item()
