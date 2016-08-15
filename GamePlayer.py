from Board import Board
from HumanEngine import Human

class GamePlayer:
    def __init__(self, white_engine=Human(), black_engine=Human(), log=True):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.board = Board()
        self.log = log

    def set_engine(self, color, engine):
        if color == 'w':
            self.white_engine = engine
        elif color == 'b':
            self.black_engine = engine

    def print_log(self, s):
        if self.log:
            print s

    def print_result(self):
        board = self.board
        # winner
        if board.result == 'd':
            print "DRAWN GAME"
        else:
            print "WINNER: ", (board.white if board.result == 'w' else board.black)
        print "Number of moves: ", board.moves


    def play_game(self):
        while self.board.result == None:
            self.print_log(self.board)
            if self.board.turn == 'w':
                move, ev = self.white_engine.get_best_move(self.board)
            else:
                move, ev = self.black_engine.get_best_move(self.board)
            self.board = self.board.make_move_from_move(move)
        self.print_result()
