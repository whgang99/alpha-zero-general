from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AnimalShogiLogic import Board
import numpy as np

class AnimalShogiGame(Game):
    square_content = {
        -5: "[L]",
        -4: "[H]",
        -3: "[G]",
        -2: "[E]",
        -1: "[C]",
        +0: "   ",
        +1: "(C)",
        +2: "(E)",
        +3: "(G)",
        +4: "(H)",
        +5: "(L)",
    }

    @staticmethod
    def getSquarePiece(piece):
        return AnimalShogiGame.square_content[piece]

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return np.array(b.pieces), np.array(b.moti), b.draw_counter

    def getBoardSize(self):
        # (a,b) tuple
        return (3, 4)

    def getActionSize(self):
        # return number of actions
        return 180  # (12 source cells + 3 mochigomas) x (12 tiles)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        pieces, moti, draw_counter = board
        b = Board()
        b.pieces = np.copy(pieces)
        b.moti = np.copy(moti)
        b.draw_counter = draw_counter.copy()
        
        if player == 1:
            move = (int(action / 48), int(action / 12) % 4, int(action / 4) % 3, action % 4)
        else:
            if action >= 144:
                move = (int(action / 48), int(action / 12) % 4, 2 - int(action / 4) % 3, 3 - action % 4)
            else:
                move = (2 - int(action / 48), 3 - int(action / 12) % 4, 2 - int(action / 4) % 3, 3 - action % 4)
            
        b.execute_move(move, player)
        return ((b.pieces, b.moti, b.draw_counter), -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        pieces, moti, _ = board
        valids = [0]*self.getActionSize()
        b = Board()
        b.pieces = np.copy(pieces)
        b.moti = np.copy(moti)
        
        legalMoves =  b.get_legal_moves(player)
        legalMoves.sort()
        
        for src_x, src_y, dst_x, dst_y in legalMoves:
            valids[48 * src_x + 12 * src_y + 4 * dst_x + dst_y] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player won, -1 if player lost or drawed
        
        # If a player sends the lion to the back-rank without immediate capture threat, they win.
        # I implemented this as "If the player begins their turn with the lion on the back-rank, they win."
        
        pieces, _, draw_counter = board

        # For training, the player who caused threefold repetition is considered lost.
        if draw_counter[0]:
            return -player

        player_lion = False
        opponent_lion = False
        player_back_rank = False
        for y in range(4):
            for x in range(3):
                if abs(pieces[x][y]) == 5:
                    if np.sign(pieces[x][y]) == player:
                        if player == 1 and y == 3 or player == -1 and y == 0:
                            return 1
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
            pieces, moti, draw_counter = board
            return np.flip(-pieces, (0, 1)), moti[::-1], draw_counter
        else:
            return board

    def getSymmetries(self, board, pi):
        # mirror
        assert(len(pi) == 180)  # 1 for pass

        pieces, moti, draw_counter = board

        pi_board = np.reshape(pi[:144], (3, 4, 3, 4))
        pi_board_uti = np.reshape(pi[144:], (3, 3, 4))
        new_pi = np.hstack((np.flip(pi_board, (1, 3)).ravel(), np.flip(pi_board_uti, (2)).ravel()))

        l = [((pieces, moti, draw_counter), pi), ((np.fliplr(pieces), moti, draw_counter), new_pi)]

        return l

    def stringRepresentation(self, board):  # TODO: print draw counters
        pieces, moti, draw_counter = board
        return pieces.tostring() + moti.tostring()

    def stringRepresentationReadable(self, board):  # TODO: print motigoma, draw counters
        pieces, moti, draw_counter = board
        pieces_s = "".join(self.square_content[square] for row in pieces for square in row)
        return pieces_s

    def getScore(self, board, player):
        pieces, moti, _ = board
        b = Board()
        b.pieces = np.copy(pieces)
        b.moti = np.copy(moti)
        return b.countDiff(player)

    @staticmethod
    def display(board):  # TODO: print motigoma
        pieces, moti, _ = board
        n = pieces.shape[0]
        print("   A   B   C")
        print("----------------")
        for y in range(3, -1, -1):
            print(y, "|", end="")    # print the row #
            for x in range(3):
                piece = pieces[x][y]    # get the piece to print
                print(AnimalShogiGame.square_content[piece], end=" ")
            print("|", end="")
            if y == 3:
                for i in range(1, 4):
                    print(AnimalShogiGame.square_content[-i] * moti[-1][i], end=' ')
            elif y == 0:
                for i in range(1, 4):
                    print(AnimalShogiGame.square_content[i] * moti[0][i], end=' ')
            print()

        print("----------------")
