from Board import *
from Evaluation import get_eval

class Minimax:
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
        return best_move, best_eval

    def evaluate(self, board, maximizing_player=False, d=1):
        # self.count += 1
        # if self.count % 1 == 0:
        #     print self.count
        # print d
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
                this_eval = self.evaluate(next_pos, False, d-1)
                # print move.move_to_str() + "*evals to" + str(this_eval)
                if this_eval > highest_eval:
                    highest_eval = this_eval
            return highest_eval
        else:
            lowest_eval = float('inf')
            for move in moves:
                next_pos = board.make_move_from_move(move)
                this_eval = self.evaluate(next_pos, True, d-1)
                # print move.move_to_str() + "evals to" + str(this_eval)
                if this_eval < lowest_eval:
                    lowest_eval = this_eval
            return lowest_eval
