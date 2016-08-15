from Move import Move
from Constants import *
from itertools import product

def get_legal_moves_for_piece(board, pos):
    piece = board.position[pos[0]][pos[1]]
    turn = board.turn
    norm_piece = (piece.lower())[0]
    if norm_piece == 'q':
        return get_legal_moves_for_queen(board, pos)
    elif norm_piece == 'r':
        return get_legal_moves_for_rook(board, pos)
    elif norm_piece == 'b':
        return get_legal_moves_for_bishop(board, pos)
    elif norm_piece == 'n':
        return get_legal_moves_for_knight(board, pos)
    elif norm_piece == 'p':
        return get_legal_moves_for_pawn(board, pos)
    elif norm_piece == 'k':
        return get_legal_moves_for_king(board, pos)
    return []

def is_mine(board, piece):
    return (board.turn == 'w') == (piece[0]).isupper()

def in_bounds(x, y):
    return (x < 8 and x >= 0) and (y < 8 and y >= 0)

# checks that a position is inbounds and does not block
def valid_br(board, pos):
    # out of bounds
    if not in_bounds(pos[0], pos[1]): return False
    # can't take own piece
    piece = board.get_piece(pos[0], pos[1])
    return (piece == None or not is_mine(board, piece))

# TO DO: FIX PAWN PROMOTION ON CAPTURE PROBLEM
def get_legal_moves_for_pawn(board, pos):
    direction = 1 if board.turn == 'w' else -1
    legal_moves = []

    # promotion
    if (pos[0] == 1 and board.turn == 'b') or (pos[0] == 6 and board.turn == 'w'):
        if (board.get_piece(pos[0] + direction, pos[1]) == None):
            for piece in promotion_pieces[board.turn]:
                legal_moves.append(Move(pos, (pos[0] + direction, pos[1]), piece[0]))

        if in_bounds(pos[0] + direction, pos[1] + direction):
            left_capture = board.get_piece(pos[0] + direction, pos[1] + direction)
            if left_capture != None and not is_mine(board, left_capture):
                for piece in promotion_pieces[board.turn]:
                    legal_moves.append(Move(pos, (pos[0] + direction, pos[1] + direction), piece[0]))

        if in_bounds(pos[0] + direction, pos[1] - direction):
            right_capture = board.get_piece(pos[0] + direction, pos[1] - direction)
            if right_capture != None and not is_mine(board, right_capture):
                for piece in promotion_pieces[board.turn]:
                    legal_moves.append(Move(pos, (pos[0] + direction, pos[1] - direction), piece[0]))

    else:

        # have to check l/r capture, move forward in all circumstances
        # nothing right ahead (different for promotion)
        if pos[0] != 1 and pos[0] != 6 and \
        (board.get_piece(pos[0] + direction, pos[1]) == None):
            legal_moves.append(Move(pos, (pos[0] + direction, pos[1])))

        # forward, right capture, first condition is ep check
        # conditions checked are in the following order:
        #   -> right capture square is in bounds
        #   -> is right capture square the en passant target
        #   -> is there a piece on the right capture square
        #   -> is that piece mine for the taking
        if in_bounds(pos[0] + direction, pos[1] + direction) and \
        (board.ep == (pos[0] + direction, pos[1] + direction) or
        ((board.get_piece(pos[0] + direction, pos[1] + direction) != None) and
         not is_mine(board, board.get_piece(pos[0] + direction, pos[1] + direction)))):
            legal_moves.append(Move(pos, (pos[0] + direction, pos[1] + direction)))

        # forward, left capture, same checks as right capture
        if in_bounds(pos[0] + direction, pos[1] - direction) and \
        (board.ep == (pos[0] + direction, pos[1] - direction) or
        ((board.get_piece(pos[0] + direction, pos[1] - direction) != None) and not
         is_mine(board, board.get_piece(pos[0] + direction, pos[1] - direction)))):
            legal_moves.append(Move(pos, (pos[0] + direction, pos[1] - direction)))

        # first move
        if (pos[0] == 1 and board.turn == 'w') or (pos[0] == 6 and board.turn == 'b'):
            if (board.get_piece(pos[0] + direction, pos[1]) == None):
                 legal_moves.append(Move(pos, (pos[0] + direction, pos[1])))
            if (board.get_piece(pos[0] + 2*direction, pos[1]) == None):
                legal_moves.append(Move(pos, (pos[0] + 2*direction, pos[1])))


    return legal_moves

def under_attack_by_pawn(board, pos):
    # opponent's pawn
    opp_pawn = 'P' if board.turn == 'b' else 'p'
    direction = 1 if board.turn == 'w' else -1

    # right capture
    if in_bounds(pos[0] + direction, pos[1] + direction) and \
    board.get_piece(pos[0] + direction, pos[1] + direction) == opp_pawn:
        return (pos[0] + direction, pos[1] + direction)

    # left capture
    if in_bounds(pos[0] + direction, pos[1] - direction) and \
    board.get_piece(pos[0] + direction, pos[1] - direction) == opp_pawn:
        return (pos[0] + direction, pos[1] - direction)

    return None




# done
def get_legal_moves_for_knight(board, pos):
    legal_moves = []
    pos_deltas = [
        (1, 2), (2, 1),
        (-1, 2), (-2, 1),
        (1, -2), (2, -1),
        (-1, -2), (-2, -1)
        ]
    for delta in pos_deltas:
        if in_bounds(delta[0] + pos[0], delta[1] + pos[1]):
            if (board.get_piece(delta[0] + pos[0], delta[1] + pos[1]) == None) or not\
             is_mine(board, board.get_piece(delta[0] + pos[0], delta[1] + pos[1])):
                legal_moves.append(Move(pos, (delta[0] + pos[0], delta[1] + pos[1])))
    return legal_moves

def under_attack_by_knight(board, pos):
    opp_knight = 'N' if board.turn == 'b' else 'n'
    pos_deltas = [
        (1, 2), (2, 1),
        (-1, 2), (-2, 1),
        (1, -2), (2, -1),
        (-1, -2), (-2, -1)
        ]
    for delta in pos_deltas:
        if in_bounds(delta[0] + pos[0], delta[1] + pos[1]) and \
        (board.get_piece(delta[0] + pos[0], delta[1] + pos[1]) == opp_knight):
            return (delta[0] + pos[0], delta[1] + pos[1])
    return None

# done
def get_legal_moves_for_bishop(board, pos):
    legal_moves = []
    pos_deltas = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for delta in pos_deltas:
        dist = 1
        while valid_br(board, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)):
            legal_moves.append(Move(pos, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)))
            # check if above takes an opponent's piece (blocks)
            piece = board.get_piece(pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece != None : break
            dist += 1
    return legal_moves

def under_attack_by_bishop(board, pos):
    opp_bishop = 'B' if board.turn == 'b' else 'b'
    pos_deltas = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for delta in pos_deltas:
        dist = 1
        while valid_br(board, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)):
            piece = board.get_piece(pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece == opp_bishop: return (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece != None : break
            dist += 1
    return None

# done
def get_legal_moves_for_rook(board, pos):
    legal_moves = []
    pos_deltas = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    for delta in pos_deltas:
        dist = 1
        while valid_br(board, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)):
            legal_moves.append(Move(pos, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)))
            # check if above takes an opponent's piece (blocks)
            piece = board.get_piece(pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece != None : break
            dist += 1
    return legal_moves

def under_attack_by_rook(board, pos):
    opp_rook = 'R' if board.turn == 'b' else 'r'
    pos_deltas = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    for delta in pos_deltas:
        dist = 1
        while valid_br(board, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)):
            piece = board.get_piece(pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece == opp_rook: return (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece != None : break
            dist += 1
    return None


# done
def get_legal_moves_for_queen(board, pos):
    return get_legal_moves_for_bishop(board, pos) + get_legal_moves_for_rook(board, pos)

def under_attack_by_queen(board, pos):
    opp_queen = 'Q' if board.turn == 'b' else 'q'
    pos_deltas = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (0, 1), (0, -1), (-1, 0)]
    for delta in pos_deltas:
        dist = 1
        while valid_br(board, (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)):
            piece = board.get_piece(pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece == opp_queen: return (pos[0] + delta[0]*dist, pos[1] + delta[1]*dist)
            if piece != None : break
            dist += 1
    return None


def kingside_clear(board, pos):
    return (board.get_piece(pos[0], pos[1] - 1) == None) \
    and (board.under_attack((pos[0], pos[1] - 1), board.turn) == None) \
    and (board.get_piece(pos[0], pos[1] - 2) == None) \
    and (board.under_attack((pos[0], pos[1] - 2), board.turn) == None)

def queenside_clear(board, pos):
    return (board.get_piece(pos[0], pos[1] + 1) == None) \
    and (board.under_attack((pos[0], pos[1] + 1), board.turn) == None) \
    and (board.get_piece(pos[0], pos[1] + 2) == None) \
    and (board.under_attack((pos[0], pos[1] + 2), board.turn) == None) \
    and (board.get_piece(pos[0], pos[1] + 3) == None) \
    and (board.under_attack((pos[0], pos[1] + 3), board.turn) == None)

# done
def get_legal_moves_for_king(board, pos):
    legal_moves = []
    # non-castle case
    pos_deltas = pos_deltas = [
        (1, 0), (0, 1),
        (-1, 0), (0, -1),
        (1, 1), (-1, -1),
        (-1, 1), (1, -1)
        ]
    for delta in pos_deltas:
        if valid_br(board, (delta[0] + pos[0], delta[1] + pos[1])) and \
        (board.under_attack((delta[0] + pos[0], delta[1] + pos[1]), board.turn) == None):
            legal_moves.append(Move(pos, (delta[0] + pos[0], delta[1] + pos[1])))

    # kingside castle case
    if (not board.in_check) and board.can_castle(board.turn, 'k') and kingside_clear(board, pos):
        # legal_moves.append(Move(pos, (pos[0], pos[1] - 2)));
        legal_moves.append(Move(pos, (pos[0], pos[1] - 2), None, None, ('K' if board.turn == 'w' else 'k')));

    # queenside castle case
    if (not board.in_check) and board.can_castle(board.turn, 'q') and queenside_clear(board, pos):
        # legal_moves.append(Move(pos, (pos[0], pos[1] + 2)))
        legal_moves.append(Move(pos, (pos[0], pos[1] + 2), None, None, ('Q' if board.turn == 'w' else 'q')))

    return legal_moves

def under_attack_by_king(board, pos):
    opp_king = 'K' if board.turn == 'b' else 'k'
    pos_deltas = pos_deltas = [
        (1, 0), (0, 1),
        (-1, 0), (0, -1),
        (1, 1), (-1, -1),
        (-1, 1), (1, -1)
        ]
    for delta in pos_deltas:
        if valid_br(board, (delta[0] + pos[0], delta[1] + pos[1]))and \
        (board.get_piece(delta[0] + pos[0], delta[1] + pos[1]) == opp_king):
            return (delta[0] + pos[0], delta[1] + pos[1])
    return None
