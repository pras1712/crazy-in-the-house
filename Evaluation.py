from Board import *



def get_eval(board):
    eval_weights = {
        is_checkmate: 10000,
        on_board_material_advantage: 20,
        in_hand_material_advantage: 30,
        king_safety: 7,
        mobility: 0.5,
        pieces_at_center: 5
    }
    total = 0
    for fn, weight in eval_weights.iteritems():
        total += fn(board)*weight
    return total



def is_checkmate(board):
    if board.result == board.turn:
        return 1
    if board.result == opponent[board.turn]:
        return -1
    return 0


def on_board_material_advantage(board):
    position = board.position
    white_adv = 0
    for (row, col) in product(xrange(len(position)), xrange(len(position))):
        piece  = position[row][col]
        if piece != None:
            piece = piece[0]
            white_adv += (piece_values[piece]) if piece.islower() else -1*(piece_values[piece])
    return white_adv if board.turn == 'w' else -1*white_adv

def in_hand_material_advantage(board):
    adv = 0
    for piece, num in board.in_hand[board.turn].iteritems():
        adv += piece_values[piece]*num
    for piece, num in board.in_hand[opponent[board.turn]].iteritems():
        adv -= piece_values[piece]*num
    return adv

def king_safety(board):
    total = 0
    if board.castled[board.turn]: total += 4
    total += len([castle for castle in board.castling[board.turn] if castle == True])
    return total

def mobility(board):
    legal_moves = [move for move in board.get_legal_moves() if move.placing_piece == None]
    total = len(legal_moves)
    for move in legal_moves:
        end_piece = board.get_piece(move.end[0], move.end[1])
        if end_piece != None:
            if end_piece.lower()[0] == 'k':
                total += 4
            else:
                total += piece_values[end_piece]
    return total

def attacking_center(board):
    return 0

def pieces_at_center(board):
    center_positions = [(3, 3), (3, 4), (4, 3), (4, 3)]
    center_pieces = [board.get_piece(pos[0], pos[1]) for pos in center_positions]
    return len([piece for piece in center_pieces if (piece in chess_pieces[board.turn])])
