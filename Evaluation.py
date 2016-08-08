from Board import *

def get_eval(board):
    return is_checkmate(board)

def is_checkmate(board):
    if board.result == board.turn:
        return 1
    if board.result == opponent[board.turn]:
        return -1
    return 0

def on_board_material_advantage(board):
    return 0

def in_hand_material_advantage(board):
    return 0

def king_safety(board):
    return 0

def num_moves(board):
    return len(board.get_legal_moves())

def attacking_center(board):
    no_placing_moves = [move for move in board.get_legal_moves() if move.placing_piece == None]
    # check if we can move a piece into the center
    # for move in board.get_legal_moves():

    return 0

def pieces_at_center(board):
    return 0
