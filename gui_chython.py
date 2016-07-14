import chython

class chess_gui:
    def __init__(self):
        print "\n================================== CHYTHON ===============================\n"
        print "Welcome to chess! A new game has begun. The current state of the board is: \n"
        self.game = chython.chess_game()
        self.game.print_board()
        self.prompt_move()

    def prompt_move(self):
        side = self.game.side_to_move
        moves = self.game.get_all_legal_moves()
        print "\nIt is the {} pieces side to move! The legal moves are listed below. Enter \nthe move number to select your move.\n".format(side)
        for i in range(len(moves)):
            move = moves[i]
            print "  "+str(i+1)+'. '+move.print_move()




c = chess_gui()
