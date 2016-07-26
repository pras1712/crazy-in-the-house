from Constants import *
from itertools import product
from PieceUtils import *
from Move import Move
class Board:
    def __init__(self, white="White", black="Black", position=None):
        self.position = self.get_starting_position()
        self.turn = 'w'
        # [bool, bool] -> [K side, Q side]
        self.castling = {
            'w': [True, True],
            'b': [True, True]
        }
        # [True, True, True, True]
        self.ep = None
        self.in_check = False
        self.halfmove_since_capt_pawn = 0
        self.moves = 0
        self.pieces = {
            'w': {piece:0 for piece in chess_pieces['w'] if piece != 'K'},
            'b': {piece:0 for piece in chess_pieces['b'] if piece != 'k'}
        }
        self.result = None # possible values: 'w', 'b', 'd'

    def print_board(self):
        print "\n"
        board = self.position
        for row in board:
            for piece in row:
                if piece == None:
                    print "   ",
                else:
                    print " " + piece + " ",
            print '\n'


    def get_piece(self, row, col):
        return self.position[row][col]

    def can_castle(self, player, side):
        # player_ind = 0 if player == 'w' else 1
        side_ind = 0 if side == 'k' else 1
        # return self.castling[2*player_ind + side_ind]
        return self.castling[player][side_ind]

    def get_starting_position(self):
        return [
            ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
            ['P']*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            ['p']*8,
            ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
        ]

    def pieces(self, player):
        return chess_pieces[player]

    def get_legal_moves(self):
        position = self.position
        moves = []
        for (row, col) in product(xrange(len(position)), xrange(len(position))):
            if position[row][col] == None:
                for piece, num in self.pieces[self.turn].iteritems():
                    if num > 0:
                        if (piece != 'p' and piece != 'P') or (row != 0 and row != 7):
                            moves.append(Move(None, (row, col), placing_piece=piece))
            elif is_mine(self, position[row][col]):
                moves += get_legal_moves_for_piece(self, (row, col))
        return moves

    # moves are made like: e2e4, e2e3
    # returns 'ILLEGAL_MOVE' if illegal
    def make_move(self, move):
        pass

    def get_result(self):
        return self.result
