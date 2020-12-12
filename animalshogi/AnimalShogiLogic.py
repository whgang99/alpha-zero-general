'''
Animal Shogi implementation by Gang, Woohyun
based on Eric P. Nichols' othello logic.

Differences from official rules:
    The player who made 1000-days-moves(threefold repetition) loses.
    Moves limit (defaults to 100)
================================================================
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row. (equivalent to files and ranks in chess - Gang, Woohyun)
'''
import numpy as np

class Board():

    # Movements of each pieces.
    # Chicks and Hens' movements are asymmetrical.
    __directions = [None,
        [(0, 1)],  # 1: White chick
        [(1,1),(1,-1),(-1,-1),(-1,1)],  # 2: (White) Elephant
        [(1,0),(0,-1),(-1,0),(0,1)],  # 3: (White) Giraffe
        [(1,1),(1,0),(0,-1),(-1,0),(-1,1),(0,1)],  # 4: White Hen
        [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)],  # 5 = -5: Lion
        [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(0,1)],  # -4: Black Hen
        [(1,0),(0,-1),(-1,0),(0,1)],  # -3: (Black) Giraffe
        [(1,1),(1,-1),(-1,-1),(-1,1)],  # -2: (Black) Elephant
        [(0, -1)]]  # -1: Black chick

    def __init__(self, turn_limit=100):
        "Set up initial board configuration."
        
        # Create the empty board array.
        self.pieces = [None] * 3
        for i in range(3):
            self.pieces[i] = [0] * 4

        # Set up the pieces at init.
        self.pieces[0][0] = 2
        self.pieces[1][0] = 5
        self.pieces[2][0] = 3
        self.pieces[1][1] = 1
        self.pieces[1][2] = -1
        self.pieces[0][3] = -3
        self.pieces[1][3] = -5
        self.pieces[2][3] = -2
        
        # Lions and hens cannot become a motigoma, so there can only be motigomas in 1st~3rd index.
        # I needlessly included 0th index for simpler implementation.
        self.moti = [[0, 0, 0, 0], [0, 0, 0, 0]]

        # Correctly re-implemented 1000 days move.
        # (Equivalent to threefold repetition of chess.)
        self.draw_counter = {}
        # dirty implementation using self.draw_counter[0]
        # as threefold repetition flag
        self.draw_counter[0] = 0

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]
    
    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        
        for i in range(1, 4):
            count += i * (self.moti[0][i] - self.moti[1][i])
        
        for y in range(4):
            for x in range(3):
                count += self[x][y]
        return count * color
    
    def get_legal_moves(self, color):
        """(src_x, src_y, dst_x, dst_y) format
        Uchi moves are denoted by src_x = 3, src_y = (piece - 1).
        """
        moves = set()  # stores the legal moves.
        
        # Unlike shogi, 2-chicks, strike-chick-mate, back-rank-chick-strike, and not evading checks are accepted.
        
        for i in range(1, 4):
            if self.moti[color // 2][i]:
                newmoves = self._get_moves_for_motigoma(i, color)
                moves.update(newmoves)
                
        # Get all the squares with pieces of the given color.
        for y in range(4):
            for x in range(3):
                if np.sign(self[x][y]) == color:
                    newmoves = self._get_moves_for_square((x,y))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for i in range(1, 4):
            if self.moti[color // 2][i]:
                newmoves = self._get_moves_for_motigoma(i, color)
                if len(newmoves)>0:
                    return True
                
        for y in range(4):
            for x in range(3):
                if np.sign(self[x][y]) == color:
                    newmoves = self._get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    def _get_moves_for_motigoma(self, piece, color):
        """Returns all the legal moves using the piece on the square.
        Move are notated in tuple (piece, x, y)
        e.g. White lion to C-file, 2nd rank is (4, 2, 1)
        """
        if not self.moti[color // 2][piece]:
            return None
        
        moves = []
        
        for y in range(4):
            for x in range(3):
                if self[x][y] == 0:
                    moves.append((3, piece - 1, x, y))

        # return the generated move list
        return moves

    def _get_moves_for_square(self, square):
        """Returns all the legal moves using the piece on the square.
        Move are notated in tuple (piece, x, y)
        e.g. White lion to C-file, 2nd rank is (4, 2, 1)
        """
        (x,y) = square
        piece = self[x][y]

        # skip empty source squares.
        if piece==0:
            return None

        # search all possible directions.
        moves = []
        for direction in self.__directions[piece]:
            move = self._discover_move(square, direction)
            if move:
                # print(square,move,direction)
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board.
        """
        # print(move)
        self.draw_counter[0] += 1

        src_x, src_y, dst_x, dst_y = move
        
        if src_x == 3:
            piece = src_y + 1
            self.moti[color // 2][piece] -= 1
            self[dst_x][dst_y] = piece * color
            return
        else:
            piece = self[src_x][src_y]
            capture = abs(self[dst_x][dst_y])
        
            self[src_x][src_y] = 0
        
            if capture % 5:
                if capture == 4:
                    capture = 1
                self.moti[color // 2][capture] += 1
        
            if piece == 1 and dst_y == 3:
                self[dst_x][3] = 4
            elif piece == -1 and dst_y == 0:
                self[dst_x][0] = -4
            else:
                self[dst_x][dst_y] = piece
            
        current_hash = self._hash(color)
        if current_hash in self.draw_counter:
            self.draw_counter[current_hash] += 1
            #print("Repeated %d times (%d)" % (self.draw_counter[current_hash], current_hash))
            if self.draw_counter[current_hash] == 3:
                self.draw_counter[0] = -1
        else:
            #print("New situation (%d)" % current_hash)
            self.draw_counter[current_hash] = 1

        return

    def _hash(self, color):
        hashValue = hash(tuple(np.vstack((self.pieces, self.moti)).flatten()))

        return hashValue

    def _discover_move(self, origin, direction):
        """ If moving the piece on origin in direction is a valid move, returns the move. If not, returns None.
        """
        x, y = origin
        dst_x, dst_y = [a + b for a, b in zip(origin, direction)]
        piece = self[x][y]

        if 0 <= dst_x < 3 and 0 <= dst_y < 4 and np.sign(self[dst_x][dst_y]) != np.sign(piece):
            return (x, y, dst_x, dst_y)
        else:
            return None

