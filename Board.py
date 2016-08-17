# THIS IS A NOTE OF THINGS THAT I NEED TO FIX:
# -> moves that cause castling rights to change DONE
# -> capturing promoted pieces DONE
# -> check that the game has ended DONE
# -> can't castle through a check DONE
# -> better support for illegal moves from human DONE

from Constants import *
from itertools import product
from PieceUtils import *
from Move import Move
from copy import deepcopy, copy
from random import shuffle

class Board:
    def __init__(self, white="White", black="Black", position=None):
        self.position = self.get_starting_position()
        self.turn = 'w'
        # [bool, bool] -> [K side, Q side]
        self.castling = {
            'w': [True, True],
            'b': [True, True]
        }
        self.castled = {
            'w': False,
            'b': False
        }
        # [True, True, True, True]
        self.ep = None
        # in_check has the coordinates of the piece that is checking
        # the king
        self.in_check = None
        self.halfmove_since_capt_pawn = 0
        self.moves = 1
        self.in_hand = {
            'w': {piece:0 for piece in chess_pieces['w'] if piece != 'K'},
            'b': {piece:0 for piece in chess_pieces['b'] if piece != 'k'}
        }
        self.result = None # possible values: 'w', 'b', 'd'

    def __str__(self):
        s = "\n"
        board = self.position
        for row in board:
            for piece in row:
                if piece == None:
                    s +=  " .  "
                else:
                    s +=  " " + piece + "  "
            s +=  '\n\n'

        s +=  "Pieces available to each player: \n"
        s +=  "White: " + str(self.in_hand['w']) + "\n"
        s +=  "Black: " + str(self.in_hand['b']) + "\n"
        return s

    def print_board(self):
        print self
        # print "\n"
        # board = self.position
        # for row in board:
        #     for piece in row:
        #         if piece == None:
        #             print " . ",
        #         else:
        #             print unicode_pieces[piece] + " ",
        #     print '\n'



    def get_piece(self, row, col):
        return self.position[row][col]

    def set_piece(self, row, col, piece):
        self.position[row][col] = piece

    def can_castle(self, player, side):
        # player_ind = 0 if player == 'w' else 1
        side_ind = 0 if side == 'k' else 1
        # return self.castling[2*player_ind + side_ind]
        return self.castling[player][side_ind]

    def set_can_castle(self, player, side, allowance):
        # player_ind = 0 if player == 'w' else 1
        side_ind = 0 if side == 'k' else 1
        # return self.castling[2*player_ind + side_ind]
        self.castling[player][side_ind] = allowance

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

    # gets all moves that are legal if we ignore any checks
    # the exclude_king parameter
    def get_legal_moves_help(self):
        position = self.position
        moves = []
        for (row, col) in product(xrange(len(position)), xrange(len(position))):
            if position[row][col] == None:
                for piece, num in self.in_hand[self.turn].iteritems():
                    if num > 0:
                        if (piece != 'p' and piece != 'P') or (row != 0 and row != 7):
                            moves.append(Move(None, (row, col), placing_piece=piece))
            elif is_mine(self, position[row][col]):
                moves += get_legal_moves_for_piece(self, (row, col))
        return moves

    def get_king_pos(self, player):
        position = self.position
        king = 'K' if player == 'w' else 'k'
        for (row, col) in product(xrange(len(position)), xrange(len(position))):
            if position[row][col] == king:
                return (row, col)
        return None

    # better version of under attack
    # iterates trough some under_attack_by_X()
    def under_attack(self, pos, perspective):
        check_fns = [under_attack_by_pawn, under_attack_by_king,
                    under_attack_by_knight, under_attack_by_bishop,
                    under_attack_by_rook, under_attack_by_queen]
        old_turn = self.turn
        self.turn = perspective
        for check_fn in check_fns:
            attacking_piece = check_fn(self, pos)
            if attacking_piece != None:
                self.turn = old_turn
                return attacking_piece
        self.turn = old_turn
        return None


    # checks if a square is "under attack" from the perspective of some player
    # def under_attack(self, pos, perspective):
    #     board_cpy = deepcopy(self)
    #     # pretend it's the opponent's turn
    #     board_cpy.turn = opponent[perspective]
    #     # we can pretend that castling isn't allowed because it's irrelvant to
    #     # checking if a square is under attack
    #     board_cpy.castling = {
    #         'w': [False, False],
    #         'b': [False, False]
    #     }
    #     moves = board_cpy.get_legal_moves_help()
    #     for move in moves:
    #         if (move.end == pos) and (move.placing_piece == None):
    #             return True
    #     return False


    # checks if the player is in check
    def is_in_check(self, player):
        return self.under_attack(self.get_king_pos(player), player)


    def get_legal_moves(self):
        attack_fns = {
                    'p': under_attack_by_pawn,
                    'k': under_attack_by_king,
                    'n': under_attack_by_knight,
                    'b': under_attack_by_bishop,
                    'r': under_attack_by_rook,
                    'q': under_attack_by_queen
                    }

        checking_pos = self.in_check
        moves = self.get_legal_moves_help()
        moves_to_return = copy(moves)
        # print [move.move_to_str() for move in moves]
        for move in moves:
            # Reasons why a move could result in check:
            #   -> (1) we were already in check, and didn't fix it
            #       "fixing it" constitutes blocking the attack, ,
            #       taking the piece, or moving out of the way
            #   -> (2) moving a pinnned piece

            # casework for (1)
            # first check: we are in check, and we didn't move the
            # king out of the way, and we didn't capture the checking
            # piece
            if checking_pos != None and \
            not (move.start != None and \
            self.get_piece(move.start[0], move.start[1]) == ('K' if self.turn == 'w' else 'k')) and \
            move.end != checking_pos:
                # check if we blocked, by putting a pawn there and seeing if still under attack
                end_piece = self.get_piece(move.end[0], move.end[1])
                self.set_piece(move.end[0], move.end[1], ('P' if self.turn == 'w' else 'p'))
                checking_piece = self.get_piece(checking_pos[0], checking_pos[1])[0]
                attack_fn = attack_fns[checking_piece.lower()]
                if attack_fn(self, self.get_king_pos(self.turn)) != None:
                    moves_to_return.remove(move)
                # undo changes
                self.set_piece(move.end[0], move.end[1], end_piece)

            # casework for (2)
            elif checking_pos == None and move.start != None:
                end_piece = self.get_piece(move.end[0], move.end[1])
                moving_piece = self.get_piece(move.start[0], move.start[1])
                self.set_piece(move.end[0], move.end[1], moving_piece)
                self.set_piece(move.start[0], move.start[1], None)
                if self.is_in_check(self.turn) != None:
                    moves_to_return.remove(move)
                # undo changes
                self.set_piece(move.start[0], move.start[1], moving_piece)
                self.set_piece(move.end[0], move.end[1], end_piece)

            # # simulate a move
            # board = self.make_move_from_move(move, True)
            # # check if that causes the player to be in check
            # if board.is_in_check(self.turn):
            #     moves_to_return.remove(move)
        shuffle(moves_to_return)
        return moves_to_return

    def print_legal_moves(self):
        print [move.move_to_str() for move in self.get_legal_moves()]

    # takes a string "e2e4" and returns the move
    # Move((2, 4), (4, 4))
    # figures out if it's a promotion, a castle, or some madness like that
    # possible types of moves:
    #   -> normal translation, capture, or castle. encoded "e2e4"
    #       for this sort of encoding, this function figures out which of
    #       the above types is correct
    #   -> promotion: encoded "e7e8, Q" for white, or "e2e1, q" for black
    #   -> placement encoded "Q@e2" for white, or "q@e2" for black
    # assumes that move strings are correctly formatted
    def get_move(self, move_str):

        def str_to_square(str):
            return (int(str[1]) - 1, 7 - ord(str[0]) + ord('a'))

        if '@' in move_str: # placement case
            end_str = move_str[2:]
            end = str_to_square(end_str)

            return Move(None, end, placing_piece=move_str[0])

        elif ',' in move_str: # promotion case
            start_str = move_str[:2]
            end_str = move_str[2:4]
            start = str_to_square(start_str)
            end = str_to_square(end_str)

            return Move(start, end, move_str[len(move_str) - 1])

        else:
            start_str = move_str[:2]
            end_str = move_str[2:]
            start = str_to_square(start_str)
            end = str_to_square(end_str)

            # check if castle
            piece = self.get_piece(start[0], start[1])
            # king moves two spaces
            if (piece == 'K' or piece == 'k') and (abs(end[1] - start[1]) == 2):
                # kingside or queenside
                castle = 'Q' if (end[1] - start[1]) > 0 else 'K'
                # white or black
                if self.turn == 'b':
                    castle = castle.lower()
                return Move(start, end, castle=castle)

        return Move(start, end)

    def result_checks(self):
        if len(self.get_legal_moves()) == 0:
            if self.in_check != None: # Checkmate!!
                return opponent[self.turn]
            else: # Stalemate!!
                return 'd'
        if self.halfmove_since_capt_pawn >= 50:
            return 'd'
        return None

    # note: castling rights for these catagories might already be False
    # this can probably be done with cleaner code (less hardcoding)
    def rook_castle_change(self, pos):
        if pos == (0, 0):
            self.castling['w'][0] = False
        elif pos == (0, 7):
            self.castling['w'][1] = False
        elif pos == (7, 0):
            self.castling['b'][0] = False
        elif pos == (7, 7):
            self.castling['b'][1] = False

    def update_in_hand(self, taken_piece):
        if len(taken_piece) == 1:
            board_cpy.in_hand[board_cpy.turn][switch_sides(taken_piece, board_cpy.turn)] += 1
        else: # capturing a piece that was promoted
            board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1
        # update castling rights
        if taken_piece.lower() == 'r':
            board_cpy.rook_castle_change(move.end)

    # makes move given an instance of Move (rather than a string)
    def make_move_from_move(self, move):

        def switch_sides(piece, player):
            return piece.upper() if player == 'w' else piece.lower()


        # need to adjust the parameters of the board
        board_cpy = deepcopy(self)

        # list of possible moves and what parameters need to be changed for each
        # ***** REMEMBER: we need to see if any given move results in a check ******
        # the possible moves are as follows:
        # 1. moving a piece from one spot to an empty spot that's not the ep target
        #   -> essentially constitutes changing the position of a piece
        #   -> note: castling rights can change here
        # 2. taking a piece
        #   -> change position of taking piece
        #   -> add taken piece to board.turn's in_hand
        #   -> note: castling rights can change here
        # 3. en passant
        #   -> change position of taking pawn
        #   -> remove pawn
        #   -> add pawn to board.turn's in_hand
        # 4. castle
        #   -> move rook and king
        #   -> note: castling rights change here
        # 5. placing piece
        #   -> put piece on square
        #   -> remove piece from in_hand
        # 6. promoting piece
        #   -> putting piece on square
        #

        if move.start != None: moving_piece = board_cpy.get_piece(move.start[0], move.start[1])
        taken_piece = board_cpy.get_piece(move.end[0], move.end[1])

        # conditions for (1) or (2): move or take
        if (move.end != board_cpy.ep) and move.castle == None \
        and move.promoting_piece == None and move.placing_piece == None:
            # change board
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], moving_piece)

            # update castle rights
            if moving_piece.lower() == 'k': # if king is moved, castling can't be done
                board_cpy.castling[board_cpy.turn] = [False, False]
            if moving_piece.lower() == 'r':
                board_cpy.rook_castle_change(move.start)

            # update in_hand (for (2))
            if taken_piece != None:
                if len(taken_piece) == 1:
                    board_cpy.in_hand[board_cpy.turn][switch_sides(taken_piece, board_cpy.turn)] += 1
                else: # capturing a piece that was promoted
                    board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1
                # update castling rights
                if taken_piece.lower() == 'r':
                    board_cpy.rook_castle_change(move.end)

            # if a piece is taken or pawn is advanced, we need to restart halfmove count
            if taken_piece != None or moving_piece == 'p' or moving_piece == 'P':
                board_cpy.halfmove_since_capt_pawn = 0


        #  condition (3): ep
        elif (move.end == board_cpy.ep) and (moving_piece == 'p' or moving_piece == 'P'):
            # change board
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], moving_piece)
            board_cpy.set_piece(move.end[0] - (1 if board_cpy.turn == 'w' else -1), move.end[1], None)
            board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1

        # condition (4): castle
        elif move.castle != None:
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], moving_piece)

            if (move.castle).lower() == 'k':
                rook = board_cpy.get_piece(move.end[0], move.end[1] - 1)
                board_cpy.set_piece(move.end[0], move.end[1] - 1, None)
                board_cpy.set_piece(move.end[0], move.end[1] + 1, rook)
            else:
                rook = board_cpy.get_piece(move.end[0], move.end[1] + 2)
                board_cpy.set_piece(move.end[0], move.end[1] + 2, None)
                board_cpy.set_piece(move.end[0], move.end[1] - 1, rook)
            board_cpy.castled[board_cpy.turn] = True
            board_cpy.castling[board_cpy.turn] = [False, False]

        # condition (5): placement
        elif move.placing_piece != None:
            board_cpy.set_piece(move.end[0], move.end[1], move.placing_piece)
            board_cpy.in_hand[board_cpy.turn][move.placing_piece] -= 1

        # condition (6): promotion
        elif move.promoting_piece != None:
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], move.promoting_piece + '*')
            if taken_piece != None:
                if len(taken_piece) == 1:
                    board_cpy.in_hand[board_cpy.turn][switch_sides(taken_piece, board_cpy.turn)] += 1
                else: # capturing a piece that was promoted
                    board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1
                # update castling rights
                if taken_piece.lower() == 'r':
                    board_cpy.rook_castle_change(move.end)

            board_cpy.halfmove_since_capt_pawn = 0


        # final adjustments
        board_cpy.turn = opponent[board_cpy.turn]
        if board_cpy.turn == 'w': board_cpy.moves += 1
        board_cpy.in_check = board_cpy.is_in_check(board_cpy.turn)

        if board_cpy.halfmove_since_capt_pawn !=  0: # means no capture or pawn advance
            board_cpy.halfmove_since_capt_pawn += 1

        board_cpy.result = board_cpy.result_checks()


        return board_cpy


    # moves are made like: e2e4, e2e3
    # returns "ILLEGAL_MOVE" if illegal
    def make_move(self, move_str):
        move = self.get_move(move_str)
        if not (move.params in [poss.params for poss in self.get_legal_moves()]):
            return "ILLEGAL_MOVE"
        return self.make_move_from_move(move)


    def get_result(self):
        return self.result
