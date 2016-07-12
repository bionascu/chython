class chess_game:
    def __init__(self):
        self.pieces = {}
        self.board = [['00','00','00','00','00','00','00','00','00','00'],
                    ['00','WR','WN','WB','WQ','WK','WB','WN','WR','00'],
                    ['00','WP','WP','WP','WP','WP','WP','WP','WP','00'],
                    ['00','--','--','BN','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','WN','--','--','--','--','--','--','00'],
                    ['00','BP','BP','BP','BP','BP','BP','BP','BP','00'],
                    ['00','BR','BN','BB','BQ','BK','BB','BN','BR','00'],
                    ['00','00','00','00','00','00','00','00','00','00']]
        self.side_to_move = 'black'
        self.previous_move = None
        self.king_has_moved = {'white': False, 'black': False}
        self.queen_rook_has_moved = {'white': False, 'black': False}
        self.king_rook_has_moved = {'white': False, 'black': False}
        self.moves_since_last_capture = 0


    def check_occupancy(self, location):
        square = self.board[int(location[0])][int(location[1])]
        if not square == "--" and not square == "00":
            return square
        return False

    def get_possible_pawn_moves(self, location):
        chess_moves = []
        # check 1 move up
        if self.side_to_move == 'white':
            front = str(int(location[0])+1)+location[1]
        else:
            front = str(int(location[0])-1)+location[1]
        if not self.check_occupancy(front):
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

        if self.side_to_move == 'white':
            left_diag = (int(location[0])+1, int(location[1])-1)
            right_diag = (int(location[0])+1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'B':
                    chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1])))
        if self.side_to_move == 'black':
            left_diag = (int(location[0])-1, int(location[1])-1)
            right_diag = (int(location[0])-1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'W':
                    chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1])))




        return chess_moves

    def get_possible_rook_moves(self, location):
        return []

    def get_possible_knight_moves(self,location):
        return []

    def get_possible_bishop_moves(self, location):
        return []

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
    def __init__(self, piece_type, starting_location, ending_location, promotion = False):
        self.piece_type = piece_type
        self.starting_location = starting_location
        self.ending_location = ending_location

    def print_move(self):
        print self.piece_type+","+self.starting_location+","+self.ending_location


c = chess_game()
moves = c.get_all_legal_moves()
for move in moves:
    move.print_move()
