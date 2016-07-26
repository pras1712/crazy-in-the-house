
class Move:
    # a4a5 = (self, 0, 3, 0, 4, board)
    def __init__(self, start, end, promoting_piece=None, placing_piece=None):
        self.start = start
        self.end = end
        self.promoting_piece = promoting_piece
        self.placing_piece = placing_piece

    # def __init__(self, start_row, start_col, end_row, end_col, board):
    #     self.start_row = start_row
    #     self.start_col = start_col
    #     self.end_row = end_row
    #     self.end_col = end_col
    #     self.board = board
    #     self.player = board.turn
    #     self.is_ep =  ((self.board).ep == (end_row, end_col))
    #     self.captured = self.captured_piece()
    #     self.is_capture = (self.captured != None)

    # def captured_piece(self):
    #     # general case
    #     end_piece = (self.board).position[self.end_row][self.end_col]
    #     if end_piece in chess_pieces[opponent[(self.board).turn]]:
    #         return end_piece

        # en passant case -_-
        # if self.is_ep:
        #     return 'P' if self.player == 'w' else 'p'
        #
        # return None
