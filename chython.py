class chess_game:
    def __init__(self):
        self.pieces = {}
        self.board = [['00','00','00','00','00','00','00','00','00','00'],
                    ['00','WR','WN','WB','WQ','WK','--','WN','WR','00'],
                    ['00','WP','WP','WP','--','WP','BP','WP','WP','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','WP','BP','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','BP','BP','BP','BP','--','BP','BP','BP','00'],
                    ['00','BR','BN','BB','BQ','BK','BB','BN','BR','00'],
                    ['00','00','00','00','00','00','00','00','00','00']]
        self.side_to_move = 'black'
        self.previous_move = None
        self.king_has_moved = {'white': False, 'black': False}
        self.queen_rook_has_moved = {'white': False, 'black': False}
        self.king_rook_has_moved = {'white': False, 'black': False}
        self.moves_since_last_capture = 0

    def print_board(self):
        row_bounds = "-"*37
        print row_bounds
        for i in range(8,0,-1):
            rank = self.board[i][1:9]
            print " | ".join(rank)
            print row_bounds


    def check_occupancy(self, location):
        square = self.board[int(location[0])][int(location[1])]
        if not square == "--" and not square == "00":
            return square
        return False

    def get_promotion_moves(self, starting_location, ending_location):
        promotion_pieces = ['N', 'B', 'R', 'Q']
        moves = []
        for piece in promotion_pieces:
             moves.append(chess_move('P', starting_location, ending_location, piece))
        return moves

    def get_possible_pawn_moves(self, location):
        chess_moves = []
        # check 1 move up
        if self.side_to_move == 'white':
            front = str(int(location[0])+1)+location[1]
            if not self.check_occupancy(front):
                if front[0] == '8':
                    promotions = self.get_promotion_moves(location, front)
                    chess_moves += promotions
                else:
                    chess_moves.append(chess_move('P', location, front))

        if self.side_to_move == 'black':
            front = str(int(location[0])-1)+location[1]
            if not self.check_occupancy(front):
                if front[0] == '1':
                    promotions = self.get_promotion_moves(location, front)
                    chess_moves += promotions
                else:
                    chess_moves.append(chess_move('P', location, front))

        # check 2 moves up
        if self.side_to_move == 'white' and location[0]=='2':
            frontfront = str(int(location[0])+2)+location[1]
            if not self.check_occupancy(frontfront):
                chess_moves.append(chess_move('P', location, frontfront))

        elif self.side_to_move == 'black' and location[0]=='7':
            frontfront = str(int(location[0])-2)+location[1]
            if not self.check_occupancy(frontfront):
                chess_moves.append(chess_move('P', location, frontfront))

        #check attacking moves
        if self.side_to_move == 'white':
            left_diag = (int(location[0])+1, int(location[1])-1)
            right_diag = (int(location[0])+1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'B':
                    if location[0] == '7':
                        promotions = self.get_promotion_moves(location, str(diag[0])+str(diag[1]))
                        chess_moves += promotions
                    else:
                        chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1])))
        if self.side_to_move == 'black':
            left_diag = (int(location[0])-1, int(location[1])-1)
            right_diag = (int(location[0])-1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'W':
                    if location[0] == '2':
                        promotions = self.get_promotion_moves(location, str(diag[0])+str(diag[1]))
                        chess_moves += promotions
                    else:
                        chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1])))

        #en passant
        if self.side_to_move == 'white':
            if location[0] == '5':
                if self.previous_move != None and self.previous_move.piece_type == 'P':
                    if self.previous_move.starting_location[0]=='7' and self.previous_move.ending_location[0] == '5':
                        if self.previous_move.ending_location[1]==str(int(location[1])-1) or self.previous_move.ending_location[1]==str(int(location[1])+1):
                            ending_column = self.previous_move.ending_location[1]
                            move = chess_move('P', location, str(int(location[0])+1)+ending_column)
                            chess_moves.append(move)
        if self.side_to_move == 'black':
            if location[0] == '4':
                if self.previous_move != None and self.previous_move.piece_type == 'P':
                    if self.previous_move.starting_location[0]=='2' and self.previous_move.ending_location[0] == '4':
                        if self.previous_move.ending_location[1]==str(int(location[1])-1) or self.previous_move.ending_location[1]==str(int(location[1])+1):
                            ending_column = self.previous_move.ending_location[1]
                            move = chess_move('P', location, str(int(location[0])-1)+ending_column)
                            chess_moves.append(move)


        return chess_moves

    def get_possible_rook_moves(self, location):
        return []

    def get_possible_knight_moves(self,location):


        return []

    def get_possible_bishop_moves(self, location):
        chess_moves = []

        # main diagonal

        new_location = str(int(location[0])+1)+str(int(location[1])+1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])+1)+str(int(new_location[1])+1)
        
        if self.side_to_move == 'white' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location))
        if self.side_to_move == 'black' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location))

        new_location = str(int(location[0])-1)+str(int(location[1])-1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])-1)+str(int(new_location[1])-1)
        
        if self.side_to_move == 'white' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location))
        if self.side_to_move == 'black' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location))

        # secondary diagonal

        new_location = str(int(location[0])+1)+str(int(location[1])-1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])+1)+str(int(new_location[1])-1)
        
        if self.side_to_move == 'white' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location))
        if self.side_to_move == 'black' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location))            

        new_location = str(int(location[0])-1)+str(int(location[1])+1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])-1)+str(int(new_location[1])+1)
        
        if self.side_to_move == 'white' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location))
        if self.side_to_move == 'black' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location))  

        return chess_moves

    def get_possible_queen_moves(self, location):
        return []

    def get_possible_king_moves(self, location):
        return []

    def get_all_legal_moves(self):
        possible_moves = []

        if self.side_to_move == 'white':
            color = "W"
        else:
            color = "B"

        for row in range(1,9):
            for column in range(1,9):
                location = str(row)+str(column)
                piece = self.board[row][column]
                if piece[0]==color:
                    piece_type = piece[1]
                    if piece_type == 'P':
                        possible_moves += self.get_possible_pawn_moves(location)
                    elif piece_type == 'R':
                        possible_moves += self.get_possible_rook_moves(location)
                    elif piece_type == 'B':
                        possible_moves += self.get_possible_bishop_moves(location)
                    elif piece_type == 'Q':
                        possible_moves += self.get_possible_queen_moves(location)
                    elif piece_type == 'N':
                        possible_moves += self.get_possible_knight_moves(location)
                    else:
                        possible_moves += self.get_possible_king_moves(location)

        return possible_moves



class chess_move:
    def __init__(self, piece_type, starting_location, ending_location, promotion = False, capture = False):
        self.piece_type = piece_type
        self.starting_location = starting_location
        self.ending_location = ending_location
        self.promotion = promotion
        self.capture = capture

    def print_move(self):
        if self.promotion:
            print self.piece_type+","+self.starting_location+","+self.ending_location+","+self.promotion
        else:
            print self.piece_type+","+self.starting_location+","+self.ending_location


c = chess_game()
c.print_board()
#c.previous_move = chess_move('P', '24','44')
moves = c.get_all_legal_moves()
for move in moves:
    move.print_move()
