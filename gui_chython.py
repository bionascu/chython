import chython

class chess_gui:
    def __init__(self, play_game = True):
        self.game = chython.chess_game()
        self.pieces = ['BK', 'BQ', 'BR', 'BB', 'BN', 'BP', 'WK', 'WQ', 'WR', 'WB', 'WN', 'WP']
        self.piece_mapping = {self.pieces[x]: unichr(9812+x) for x in range(len(self.pieces))}
        self.piece_mapping['--'] = ' '
        if play_game:
            print "\n================================== CHYTHON ===============================\n"
            print "Welcome to chess! A new game has begun. The current state of the board is: \n"
            self.print_board()
            self.prompt_move()

    def get_box_borders(self):
        allbox = u''.join(unichr(9472 + x) for x in range(200))
        box = [ allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60) ]
        (vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box
        h3 = hbar * 3
        topline = ul + (h3 + nt) * 7 + h3 + ur
        midline = wt + (h3 + plus) * 7 + h3 + et
        botline = ll + (h3 + st) * 7 + h3 + lr
        return topline, midline, botline, vbar

    def print_board(self):
        topline, midline, botline, vbar = self.get_box_borders()
        print "  " + topline
        for i in range(8,0,-1):
            rank = self.game.board[i][1:9]
            rank = [self.piece_mapping[x] for x in rank]
            print str(i) + " " + vbar + " " + (' ' + vbar + ' ').join(rank) + ' ' + vbar#" + " | ".join(rank) + " | "
            if i != 1:
                print "  " + midline
            else:
                print "  " + botline
        column_names = list('abcdefgh')
        padded_columns = [" "+x for x in column_names]
        print "   "+'  '.join(padded_columns)

    def prompt_move(self):
        print self.game.can_castle_queenside
        side = self.game.side_to_move
        moves = self.game.get_all_legal_moves()
        print "\nIt is the {} pieces side to move! The legal moves are listed below. Enter \nthe move number to select your move.\n".format(side)
        for i in range(len(moves)):
            move = moves[i]
            print "  "+str(i+1)+'. '+move.print_move()
        player_move = raw_input('\nChoose your move from the above list. Type only the number for the move you desire. If you would like to step back a move, enter 0.\n\n')
        if self.validate_move(player_move, moves):
            if int(player_move) > 0:
                self.execute_move(moves[int(player_move)-1])
            else:
                self.undo_move()
        else:
            print "Wrong"

    def validate_move(self,player_input,moves):
        move_list = range(0,len(moves)+1)
        if int(player_input) not in move_list:
            return False
        return True

    def execute_move(self, move):
        print "\nThank you for the move! Executing your move now. The updated board is below:\n"
        self.game.update_board(move)
        self.print_board()
        self.prompt_move()

    def undo_move(self):
        move = self.game.move_history[-1]
        print "\nUndoing previous move..."
        self.game.unupdate_board(move)
        self.print_board()
        self.prompt_move()




if __name__ == "__main__":
    c = chess_gui()
