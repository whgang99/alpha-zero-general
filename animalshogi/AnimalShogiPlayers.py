import numpy as np
from random import choice


piece2int = {'C': 1, 'E': 2, 'G': 3, 'L': 4}
int2piece = {1: 'C', 2: 'E', 3: 'G', 4: 'L'}

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanAnimalShogiPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print("[", int2piece[int(i/12) + 1], int(i/4) % 3, int(i%4), end="] ")
        while True:
            input_move = input()
            input_a = input_move.strip(" ")
            if len(input_a) == 3:
                try:
                    piece, x, y = input_a
                    piece = piece.upper()
                    x, y = int(x), int(y)
                    if piece in piece2int and (0 <= x < 3) and (0 <= y < 4):
                        a = 12 * (piece2int[piece] - 1) + 4 * x + y
                        if valid[a]:
                            break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return a


class GreedyAnimalShogiPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        max_score = -10
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            print(score, a // 12 + 1, (a // 4) % 3, a % 4)
            if score > max_score:
                max_score = score
                candidates = [a]
            elif score == max_score:
                candidates.append(a)
        return choice(candidates)
