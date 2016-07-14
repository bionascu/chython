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
        player_move = raw_input('\nChoose your move from the above list. Type only the number for the move you desire.\n\n')
        if self.validate_move(player_move, moves):
            self.execute_move(moves[int(player_move)-1])
        else:
            print "Wrong"

    def validate_move(self,player_input,moves):
        move_list = range(1,len(moves)+1)
        if int(player_input) not in move_list:
            return False
        return True

    def execute_move(self, move):
        print "\nThank you for the move! Executing your move now. The updated board is below:\n"
        self.game.update_board(move)
        self.game.print_board()
        self.prompt_move()






c = chess_gui()
