from Move import Move
from itertools import product

def get_legal_moves_for_piece(board, pos):
    piece = board.position[pos[0]][pos[1]]
    turn = board.turn
    norm_piece = piece.lower()
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
    return (board.turn == 'w') == piece.isupper()

def in_bounds(x, y):
    return (x < 8 and x >= 0) and (y < 8 and y >= 0)

# checks that a position is inbounds and does not block
def valid_br(board, pos):
    # out of bounds
    if not in_bounds(pos[0], pos[1]): return False
    # can't take own piece
    piece = board.get_piece(pos[0], pos[1])
    return (piece == None or not is_mine(board, piece))

# done
def get_legal_moves_for_pawn(board, pos):
    direction = 1 if board.turn == 'w' else -1
    legal_moves = []

    # have to check l/r capture, move forward in all circumstances
    # nothing right ahead (different for promotion)
    if pos[0] != 1 and pos[0] != 6 and \
    (board.get_piece(pos[0] + direction, pos[1]) == None):
        legal_moves.append(Move(pos, (pos[0] + direction, pos[1])))

    # forward, right capture, first condition is ep check
    if board.ep == (pos[0] + direction, pos[1] + direction) or \
    ((board.get_piece(pos[0] + direction, pos[1] + direction) != None) and not
     is_mine(board, board.get_piece(pos[0] + direction, pos[1] + direction))):
        legal_moves.append(Move(pos, (pos[0] + direction, pos[1] + direction)))
    # forward, left capturefirst condition is ep check

    if board.ep == (pos[0] + direction, pos[1] - direction) or
    ((board.get_piece(pos[0] + direction, pos[1] - direction) != None) and not
     is_mine(board, board.get_piece(pos[0] + direction, pos[1] - direction))):
        legal_moves.append(Move(pos, (pos[0] + direction, pos[1] - direction)))

    # first move
    if (pos[0] == 1 and board.turn == 'w') or (pos[0] == 6 and board.turn == 'b'):
        if (board.get_piece(pos[0] + direction, pos[1]) == None):
             legal_moves.append(Move(pos, (pos[0] + direction, pos[1])))
        if (board.get_piece(pos[0] + 2*direction, pos[1]) == None):
            legal_moves.append(Move(pos, (pos[0] + 2*direction, pos[1])))

    # promotion
    if (pos[0] == 1 and board.turn == 'b') or (pos[0] == 6 and board.turn == 'w'):
        for piece in promotion_pieces[board.turn]:
            legal_moves.append(Move(pos, (pos[0] + direction, pos[1]), piece))

    return legal_moves

# done
def get_legal_moves_for_knight(board, pos):
    legal_moves = []
    pos_deltas = [
        (1, 2), (2, 1),
        (-1, 2), (-2, 1),
        (1, -2), (2, -1),
        (-1, -2), (-2, 1)
        ]
    for delta in pos_deltas:
        if in_bounds(delta[0] + pos[0], delta[1] + pos[1]):
            if (board.get_piece(delta[0] + pos[0], delta[1] + pos[1]) == None) or not\
             is_mine(board, board.get_piece(delta[0] + pos[0], delta[1] + pos[1])):
                legal_moves.append(Move(pos, delta[0] + pos[0], delta[1] + pos[1]))
    return legal_moves

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

# done
def get_legal_moves_for_queen(board, pos):
    return get_legal_moves_for_bishop(board, pos) + get_legal_moves_for_rook(board, pos)

def kingside_clear(board, pos):
    return (board.get_piece(pos[0], pos[1] - 1) == None) \
    and (board.get_piece(pos[0], pos[1] - 2) == None)

def queenside_clear(board, pos):
    return (board.get_piece(pos[0], pos[1] + 1) == None) \
    and (board.get_piece(pos[0], pos[1] + 2) == None) \
    and (board.get_piece(pos[0], pos[1] + 3) == None)

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
        if valid_br(board, (delta[0] + pos[0], delta[1] + pos[1])):
            legal_moves.append(Move(pos, (delta[0] + pos[0], delta[1] + pos[1])))

    # kingside castle case
    if !board.in_check and board.can_castle(board.turn, 'k') and kingside_clear(board, pos):
        legal_moves.append(Move(pos, (pos[0], pos[1] - 2)))

    # queenside castle case
    if !board.in_check and board.can_castle(board.turn, 'q') and queenside_clear(board, pos):
        legal_moves.append(Move(pos, (pos[0], pos[1] + 2)))

    return legal_moves
