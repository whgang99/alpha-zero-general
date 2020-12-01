import numpy as np
from random import choice


piece2int = {'C': 1, 'E': 2, 'G': 3, 'H': 4, 'L': 5}
int2piece = {1: 'C', 2: 'E', 3: 'G', 4: 'H', 5: 'L'}

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
                src_x, src_y, dst_x, dst_y = i // 48, (i // 12) % 4, (i // 4) % 3, i % 4
                if src_x == 3:
                    print("[", int2piece[src_y + 1], chr(dst_x + 65), dst_y, sep="", end="]")
                else:
                    print("[", chr(src_x + 65), src_y, chr(dst_x + 65), dst_y, sep="", end="]")
        while True:
            input_move = input()
            input_a = input_move
            if input_a[-1].upper() == 'U':
                uti = True
                input_a = input_a[:-1]
            else:
                uti=False
            if len(input_a) == 4:
                try:
                    src_x, src_y, dst_x, dst_y = input_a
                    src_x, dst_x = ord(src_x.upper()) - 65, ord(dst_x.upper()) - 65
                    src_y, dst_y = int(src_y), int(dst_y)
                    print(src_x, src_y, dst_x, dst_y )
                    
                    if (0 <= src_x < 3) and (0 <= src_y < 4) and (0 <= dst_x < 3) and (0 <= dst_y < 4):
                        a = 48 * src_x + 12 * src_y + 4 * dst_x + dst_y
                        if valid[a]:
                            break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            elif len(input_a) == 3:
                try:
                    src_x = 3
                    src_y, dst_x, dst_y = input_a
                    src_y = piece2int[src_y.upper()] - 1
                    dst_x = ord(dst_x.upper()) - 65
                    dst_y = int(dst_y)
                    
                    print(src_x, src_y, dst_x, dst_y)
                    
                    if (0 <= src_y < 3) and (0 <= dst_x < 3) and (0 <= dst_y < 4):
                        a = 48 * src_x + 12 * src_y + 4 * dst_x + dst_y
                        print(a)
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
        max_score = -20
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            if score > max_score:
                max_score = score
                candidates = [a]
            elif score == max_score:
                candidates.append(a)
        return choice(candidates)
