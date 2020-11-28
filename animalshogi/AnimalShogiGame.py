from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AnimalShogiLogic import Board
import numpy as np

class AnimalShogiGame(Game):
    square_content = {
        -4: "[L]",
        -3: "[G]",
        -2: "[E]",
        -1: "[C]",
        +0: "   ",
        +1: "(C)",
        +2: "(E)",
        +3: "(G)",
        +4: "(L)",
    }

    @staticmethod
    def getSquarePiece(piece):
        return AnimalShogiGame.square_content[piece]

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return np.array(b.pieces), b.draw_counter

    def getBoardSize(self):
        # (a,b) tuple
        return (3, 4)

    def getActionSize(self):
        # return number of actions
        return 48

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        pieces, draw_counter = board
        b = Board()
        b.pieces = np.copy(pieces)
        b.draw_counter = draw_counter
        if player == 1:
            move = ((int(action/12) + 1), int(action/4) % 3, action%4)
        else:
            move = ((int(action/12) + 1), 2 - int(action/4) % 3, 3 - action%4)
        b.execute_move(move, player)
        return ((b.pieces, b.draw_counter), -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        pieces, _ = board
        valids = [0]*self.getActionSize()
        b = Board()
        b.pieces = np.copy(pieces)
        legalMoves =  b.get_legal_moves(player)
        for piece, x, y in legalMoves:
            valids[12 * (piece - 1) + 4 * x + y] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player won, -1 if player lost or drawed
        # player = 1
        pieces, draw_counter = board

        if draw_counter >= 20:
            return 0.001

        player_lion = False
        opponent_lion = False
        for y in range(4):
            for x in range(3):
                if abs(pieces[x][y]) == 4:
                    if np.sign(pieces[x][y]) == player:
                        player_lion = True
                    else:
                        opponent_lion = True
        
        if player_lion and opponent_lion:
            return 0
        elif player_lion:
            return 1
        elif opponent_lion:
            return -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == -1:
            pieces, draw_counter = board
            return np.flip(-pieces, (0, 1)), draw_counter
        else:
            return board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == 48)  # 1 for pass

        pieces, draw_counter = board

        pi_board = np.reshape(pi, (4, 3, 4))

        l = [((pieces, draw_counter), pi), ((np.fliplr(pieces), draw_counter), list(np.flip(pi_board, 1).ravel()))]

        return l

    def stringRepresentation(self, board):
        pieces, draw_counter = board
        return pieces.tostring() + bytes('%02d' % draw_counter, 'utf-8')

    def stringRepresentationReadable(self, board):
        pieces, draw_counter = board
        pieces_s = "".join(self.square_content[square] for row in pieces for square in row)
        return pieces_s + '\nDraw Counter: %d' % draw_counter

    def getScore(self, board, player):
        pieces, _ = board
        b = Board()
        b.pieces = np.copy(pieces)
        return b.countDiff(player)

    @staticmethod
    def display(board):
        pieces, draw_counter = board
        n = pieces.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end="   ")
        print("")
        print("----------------")
        for y in range(3, -1, -1):
            print(y, "|", end="")    # print the row #
            for x in range(3):
                piece = pieces[x][y]    # get the piece to print
                print(AnimalShogiGame.square_content[piece], end=" ")
            print("|")

        print("---------------- (%d)" % (20 - draw_counter))
