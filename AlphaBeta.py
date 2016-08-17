from Board import *
from Evaluation import get_eval

class AlphaBeta:
    def __init__(self):
        self.count = 0
        pass

    def get_best_move(self, board):
        moves = board.get_legal_moves()
        best_move = None
        best_eval = float("-inf")
        for move in moves:
            next_pos = board.make_move_from_move(move)
            this_eval = self.evaluate(next_pos)
            if this_eval > best_eval:
                best_move = move
                best_eval = this_eval
        print "positions evaluated: ", self.count
        return best_move, best_eval

    def evaluate(self, board, alpha=float("-inf"), beta=float("inf"), maximizing_player=False, d=2):
        self.count += 1
        # ''' Evaluates the position given by board to depth d '''
        if d == 0:
            # print "eval: " + str(get_eval(board))
            return get_eval(board) if maximizing_player else -1*get_eval(board)
        # white's turn, and maximizing_player is True, that means that i am white
        if board.result == 'w' or board.result == 'b':
            return float('inf') if maximizing_player else float('-inf')
        if board.result == 'd':
            return 0
        moves = board.get_legal_moves()
        if maximizing_player:
            highest_eval = float('-inf')
            for move in moves:
                next_pos = board.make_move_from_move(move)
                highest_eval = max(highest_eval, self.evaluate(next_pos, alpha, beta, False, d - 1))
                if beta <= alpha:
                    break
            return highest_eval
        else:
            lowest_eval = float('inf')
            for move in moves:
                next_pos = board.make_move_from_move(move)
                lowest_eval = min(lowest_eval, self.evaluate(next_pos, alpha, beta, True, d - 1))
                if beta <= alpha:
                    break
            return lowest_eval
