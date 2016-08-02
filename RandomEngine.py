from Board import Board
from random import randint

# plays a random game
b = Board()
while b.result == None:
    b.print_board()
    if b.turn == 'b':
        #black is human
        new_b = "ILLEGAL_MOVE"
        while new_b == "ILLEGAL_MOVE":
            human_move_str = raw_input("Play a move: ")
            new_b = b.make_move(human_move_str)
        b = new_b
    else:
        print "Now it's my turn"
        moves = b.get_legal_moves()
        rand_index = randint(0, len(moves) - 1)
        print "I'm going to play " + moves[rand_index].move_to_str()
        b = b.make_move_from_move(moves[rand_index])
print b.result + " won!!"
