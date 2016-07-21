import copy

class chess_game:
    def __init__(self):
        self.pieces = {}
        self.board = [['00','00','00','00','00','00','00','00','00','00'],
                    ['00','WR','WN','WB','WQ','WK','WB','WN','WR','00'],
                    ['00','WP','WP','WP','WP','WP','WP','WP','WP','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','--','--','--','--','--','--','--','--','00'],
                    ['00','BP','BP','BP','BP','BP','BP','BP','BP','00'],
                    ['00','BR','BN','BB','BQ','BK','BB','BN','BR','00'],
                    ['00','00','00','00','00','00','00','00','00','00']]
        self.side_to_move = 'W'

        self.can_castle_kingside = {'W':[True],'B':[True]}
        self.can_castle_queenside = {'W':[True], 'B':[True]}

        self.king_has_moved = {'W': False, 'B': False}
        self.queen_rook_has_moved = {'W': False, 'B': False}
        self.king_rook_has_moved = {'W': False, 'B': False}
        self.moves_since_last_capture = [0]
        self.move_history = [None]

    def __setitem__(self, location, value): # use like self['12']= 'BB'
        self.board[int(location[0])][int(location[1])] = value

    def __getitem__(self, location):
        return self.board[int(location[0])][int(location[1])] # use like self['12']

    def get_new_location(self, location, row_delta, column_delta):
        end_row = int(location[0])+row_delta
        end_column = int(location[1])+column_delta
        return str(end_row)+str(end_column)

    @property
    def opponent_color(self):
        if self.side_to_move == 'W':
            return 'B'
        else:
            return 'W'

    def update_board(self,move):
        # add move to move_history
        self.move_history.append(move)

        # check and update king move
        if move.piece_type == 'K':
            #self.king_has_moved[self.side_to_move] = True
            self.can_castle_kingside[self.side_to_move].append(False)
            self.can_castle_queenside[self.side_to_move].append(False)

        # check and update rook moves
        if move.piece_type == 'R':
            if move.starting_location[1]=='8':
                if move.starting_location[0]=='1':
                    self.can_castle_kingside['W'].append(False)
                elif move.starting_location[0]=='8':
                    self.can_castle_kingside['B'].append(False)
            elif move.starting_location[1]=='1':
                if move.starting_location[0]=='1':
                    self.can_castle_queenside['W'].append(False)
                elif move.starting_location[0]=='8':
                    self.can_castle_queenside['B'].append(False)

        # update opponents castling rights
        self.can_castle_queenside[self.opponent_color].append(self.can_castle_queenside[self.opponent_color][-1])
        self.can_castle_kingside[self.opponent_color].append(self.can_castle_kingside[self.opponent_color][-1])

        # update movers castling rights if they haven't changed
        if len(self.can_castle_kingside[self.side_to_move])!=len(self.can_castle_kingside[self.opponent_color]):
            self.can_castle_kingside[self.side_to_move].append(self.can_castle_kingside[self.side_to_move][-1])
        if len(self.can_castle_queenside[self.side_to_move])!= len(self.can_castle_queenside[self.opponent_color]):
            self.can_castle_queenside[self.side_to_move].append(self.can_castle_kingside[self.side_to_move][-1])

        # update last capture tracker
        if move.capture == False:
            self.moves_since_last_capture.append(self.moves_since_last_capture[-1]+1)
        else:
            self.moves_since_last_capture.append(0)

        # update side to move
        self.side_to_move = self.opponent_color

        # update board state
        piece_to_move = self[move.starting_location]
        self[move.starting_location] = '--'

        # check for promotion
        if move.promotion:
            self[move.ending_location] = piece_to_move[0]+move.promotion
        else:
            self[move.ending_location] = piece_to_move

        # check for en passant
        if move.en_passant:
            self[move.en_passant] = '--'

        # check for castling and update rook position
        if move.castling == 'Q':
            rook_to_move = self[self.get_new_location(move.starting_location,0,-4)]
            self[self.get_new_location(move.ending_location,0,1)] = rook_to_move
            self[self.get_new_location(move.starting_location,0,-4)] = '--'
        if move.castling == 'K':
            rook_to_move = self[self.get_new_location(move.starting_location,0,3)]
            self[self.get_new_location(move.ending_location,0,-1)] = rook_to_move
            self[self.get_new_location(move.starting_location,0,3)] = '--'


    def unupdate_board(self,move):
        # step back move history
        del self.move_history[-1]

        # step back castling rights
        del self.can_castle_queenside['W'][-1]
        del self.can_castle_queenside['B'][-1]
        del self.can_castle_kingside['W'][-1]
        del self.can_castle_kingside['B'][-1]

        # update capture counter
        del self.moves_since_last_capture[-1]

        # update side to move
        self.side_to_move = self.opponent_color

        # update board state
        piece_to_move = self[move.ending_location]
        if move.promotion:
            self[move.starting_location] = self.side_to_move+'P'
        else:
            self[move.starting_location] = piece_to_move

        # update move end position for captures
        if move.capture:
            self[move.ending_location] = move.capture
        else:
            self[move.ending_location] = '--'

        # update for en passant
        if move.en_passant:
            self[move.en_passant] = self.opponent_color+'P'

        # check for castling and update rook position
        if move.castling == 'Q':
            rook_to_move = self[self.get_new_location(move.ending_location,0,1)]
            self[self.get_new_location(move.ending_location,0,-2)] = rook_to_move
            self[self.get_new_location(move.ending_location,0,1)] = '--'
        if move.castling == 'K':
            rook_to_move = self[self.get_new_location(move.ending_location,0,-1)]
            self[self.get_new_location(move.ending_location,0,1)] = rook_to_move
            self[self.get_new_location(move.ending_location,0,-1)] = '--'


    def check_occupancy(self, location):
        # returns false if square is unoccupied, the piece otherwise (or boundary)
        square = self.board[int(location[0])][int(location[1])]
        if not square == "--":
            return square
        return False

    def get_promotion_moves(self, starting_location, ending_location, capture = False):
        promotion_pieces = ['N', 'B', 'R', 'Q']
        moves = []
        for piece in promotion_pieces:
            if capture:
                moves.append(chess_move('P', starting_location, ending_location, promotion = piece, capture = True))
            else:
                moves.append(chess_move('P', starting_location, ending_location, promotion = piece))
        return moves

    def get_possible_pawn_moves(self, location):
        chess_moves = []
        # check 1 move up
        if self.side_to_move == 'W':
            front = str(int(location[0])+1)+location[1]
            if not self.check_occupancy(front):
                if front[0] == '8':
                    promotions = self.get_promotion_moves(location, front)
                    chess_moves += promotions
                else:
                    chess_moves.append(chess_move('P', location, front))
        if self.side_to_move == 'B':
            front = str(int(location[0])-1)+location[1]
            if not self.check_occupancy(front):
                if front[0] == '1':
                    promotions = self.get_promotion_moves(location, front)
                    chess_moves += promotions
                else:
                    chess_moves.append(chess_move('P', location, front))

        # check 2 moves up
        if self.side_to_move == 'W' and location[0]=='2':
            front = str(int(location[0])+1)+location[1]
            frontfront = str(int(location[0])+2)+location[1]
            if not self.check_occupancy(frontfront) and not self.check_occupancy(front):
                chess_moves.append(chess_move('P', location, frontfront))
        elif self.side_to_move == 'B' and location[0]=='7':
            front = str(int(location[0])-1)+location[1]
            frontfront = str(int(location[0])-2)+location[1]
            if not self.check_occupancy(frontfront) and not self.check_occupancy(front):
                chess_moves.append(chess_move('P', location, frontfront))

        #check attacking moves
        if self.side_to_move == 'W':
            left_diag = (int(location[0])+1, int(location[1])-1)
            right_diag = (int(location[0])+1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'B':
                    if location[0] == '7':
                        promotions = self.get_promotion_moves(location, str(diag[0])+str(diag[1]), capture = self.board[diag[0]][diag[1]])
                        chess_moves += promotions
                    else:
                        chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1]), capture = self.board[diag[0]][diag[1]]))
        if self.side_to_move == 'B':
            left_diag = (int(location[0])-1, int(location[1])-1)
            right_diag = (int(location[0])-1, int(location[1])+1)
            diagonals = [left_diag, right_diag]
            for diag in diagonals:
                if self.board[diag[0]][diag[1]][0] == 'W':
                    if location[0] == '2':
                        promotions = self.get_promotion_moves(location, str(diag[0])+str(diag[1]), capture = self.board[diag[0]][diag[1]])
                        chess_moves += promotions
                    else:
                        chess_moves.append(chess_move('P', location, str(diag[0])+str(diag[1]), capture = self.board[diag[0]][diag[1]]))

        #en passant
        previous_move = self.move_history[-1]
        if self.side_to_move == 'W':
            if location[0] == '5':
                if previous_move != None and previous_move.piece_type == 'P':
                    if previous_move.starting_location[0]=='7' and previous_move.ending_location[0] == '5':
                        if previous_move.ending_location[1]==str(int(location[1])-1) or previous_move.ending_location[1]==str(int(location[1])+1):
                            ending_column = previous_move.ending_location[1]
                            move = chess_move('P', location, str(int(location[0])+1)+ending_column, capture = False, en_passant = location[0]+ending_column)
                            chess_moves.append(move)
        if self.side_to_move == 'B':
            if location[0] == '4':
                if previous_move != None and previous_move.piece_type == 'P':
                    if previous_move.starting_location[0]=='2' and previous_move.ending_location[0] == '4':
                        if previous_move.ending_location[1]==str(int(location[1])-1) or previous_move.ending_location[1]==str(int(location[1])+1):
                            ending_column = previous_move.ending_location[1]
                            move = chess_move('P', location, str(int(location[0])-1)+ending_column, capture = False, en_passant = location[0]+ending_column)
                            chess_moves.append(move)

        return chess_moves

    def get_possible_rook_moves(self, location):
        if self.side_to_move == 'W':
            enemy_color = 'B'
        else:
            enemy_color = 'W'
        moves = []

        #up
        new_location = str(int(location[0])+1)+location[1]
        while not self.check_occupancy(new_location):
            moves.append(chess_move('R',location,new_location))
            new_location = str(int(new_location[0])+1)+location[1]
        if self.check_occupancy(new_location)[0]==enemy_color:
            moves.append(chess_move('R',location,new_location,capture = self[new_location]))

        #down
        new_location = str(int(location[0])-1)+location[1]
        while not self.check_occupancy(new_location):
            moves.append(chess_move('R',location,new_location))
            new_location = str(int(new_location[0])-1)+location[1]
        if self.check_occupancy(new_location)[0]==enemy_color:
            moves.append(chess_move('R',location,new_location,capture = self[new_location]))

        #left
        new_location = location[0]+str(int(location[1])-1)
        while not self.check_occupancy(new_location):
            moves.append(chess_move('R',location,new_location))
            new_location = location[0]+str(int(new_location[1])-1)
        if self.check_occupancy(new_location)[0]==enemy_color:
            moves.append(chess_move('R',location,new_location,capture = self[new_location]))

        #right
        new_location = location[0]+str(int(location[1])+1)
        while not self.check_occupancy(new_location):
            moves.append(chess_move('R',location,new_location))
            new_location = location[0]+str(int(new_location[1])+1)
        if self.check_occupancy(new_location)[0]==enemy_color:
            moves.append(chess_move('R',location,new_location,capture = self[new_location]))

        return moves

    def get_possible_knight_moves(self,location):
        if self.side_to_move == 'W':
            enemy_color = 'B'
        else:
            enemy_color = 'W'

        moves = []
        deltas = [2,-2,1,-1]
        for d1 in deltas:
            for d2 in [d for d in deltas if abs(d)!=abs(d1)]:
                x_coord = int(location[0])+d1
                y_coord = int(location[1])+d2
                new_location = str(x_coord)+str(y_coord)
                if x_coord>=0 and y_coord >=0 and x_coord<=9 and y_coord<=9:
                    if not self.check_occupancy(new_location):
                        moves.append(chess_move('N',location,new_location))
                    else:
                        if self.check_occupancy(new_location)[0]==enemy_color:
                            moves.append(chess_move('N',location,new_location,capture = self[new_location]))

        return moves

    def get_possible_bishop_moves(self, location):
        chess_moves = []

        # main diagonal
        new_location = str(int(location[0])+1)+str(int(location[1])+1)
        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])+1)+str(int(new_location[1])+1)

        if self.side_to_move == 'W' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))
        if self.side_to_move == 'B' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))

        new_location = str(int(location[0])-1)+str(int(location[1])-1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])-1)+str(int(new_location[1])-1)

        if self.side_to_move == 'W' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))
        if self.side_to_move == 'B' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))

        # secondary diagonal

        new_location = str(int(location[0])+1)+str(int(location[1])-1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])+1)+str(int(new_location[1])-1)

        if self.side_to_move == 'W' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))
        if self.side_to_move == 'B' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))

        new_location = str(int(location[0])-1)+str(int(location[1])+1)

        while not self.check_occupancy(new_location):
            chess_moves.append(chess_move('B', location, new_location))
            new_location = str(int(new_location[0])-1)+str(int(new_location[1])+1)

        if self.side_to_move == 'W' and self.board[int(new_location[0])][int(new_location[1])][0] == 'B':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))
        if self.side_to_move == 'B' and self.board[int(new_location[0])][int(new_location[1])][0] == 'W':
            chess_moves.append(chess_move('B', location, new_location, capture = self[new_location]))

        return chess_moves

    def get_possible_queen_moves(self, location):
        diagonal_moves = self.get_possible_bishop_moves(location)
        straight_moves = self.get_possible_rook_moves(location)
        moves = diagonal_moves+straight_moves
        for move in moves:
            move.piece_type = "Q"
        return moves

    def get_possible_king_moves(self, location):
        if self.side_to_move == 'W':
            enemy_color = 'B'
        else:
            enemy_color = 'W'

        moves = []
        deltas = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        for delta in deltas:
            x_coord = int(location[0])+delta[0]
            y_coord = int(location[1])+delta[1]
            new_location = str(x_coord)+str(y_coord)
            if not self.check_occupancy(new_location):
                moves.append(chess_move('K',location,new_location))
            else:
                if self.check_occupancy(new_location)[0]==enemy_color:
                    moves.append(chess_move('K',location,new_location,capture = self[new_location]))
        return moves

    def get_all_legal_moves(self):
        possible_moves = []

        if self.side_to_move == 'W':
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
                        possible_moves += self.get_castling_moves(location)

        legal_moves = []
        for move in possible_moves:
            if not self.check_move_for_check(move):
                legal_moves.append(move)
        return legal_moves

    def get_king_location(self):
        if self.side_to_move == 'W':
            king = 'BK'
        else:
            king = 'WK'
        for row in range(1,len(self.board)-1):
            for column in range(1,len(self.board)-1):
                if self.board[row][column] == king:
                    return str(row)+str(column)


    def check_move_for_check(self, move):
        potential_game = copy.deepcopy(self)
        potential_game.update_board(move)

        king_location = potential_game.get_king_location()
        if potential_game.side_to_move == 'W':
            potential_game.side_to_move = 'B'
        else:
            potential_game.side_to_move = 'W'
        moves = []
        moves += potential_game.get_possible_pawn_moves(king_location)
        moves += potential_game.get_possible_rook_moves(king_location)
        moves += potential_game.get_possible_bishop_moves(king_location)
        moves += potential_game.get_possible_knight_moves(king_location)
        moves += potential_game.get_possible_queen_moves(king_location)
        moves += potential_game.get_possible_king_moves(king_location)

        for m in moves:
            ending_square = potential_game.board[int(m.ending_location[0])][int(m.ending_location[1])]
            if ending_square[1] == m.piece_type:
                return True
        return False

    def get_castling_moves(self, location):
        queen_side, king_side = True, True
        if self.side_to_move == 'W': row = 1
        else: row = 8
        queen_side_columns = [2, 3, 4]
        queen_side_check_columns = [3, 4]
        king_side_columns = [6, 7]
        king_side_check_columns = [5, 6]

        # queen side
        if self.can_castle_queenside[self.side_to_move]:
        #if not self.king_has_moved[self.side_to_move] and not self.queen_rook_has_moved[self.side_to_move]:
            # check occupancy
            for column in queen_side_columns:
                if self.board[row][column] != '--':
                    queen_side = False
            # check for check
            for column in queen_side_check_columns:
                move = chess_move('K', location, str(row)+str(column))
                if self.check_move_for_check(move):
                    queen_side = False
        else:
            queen_side = False

        # king side
        if self.can_castle_kingside[self.side_to_move]:
        #if not self.king_has_moved[self.side_to_move] and not self.king_rook_has_moved[self.side_to_move]:
            # check occupancy
            for column in king_side_columns:
                if self.board[row][column] != '--':
                    king_side = False
            # check for check
            for column in king_side_check_columns:
                move = chess_move('K', location, str(row)+str(column))
                if self.check_move_for_check(move):
                    king_side = False
        else:
            king_side = False

        moves = []
        if queen_side:
            moves.append(chess_move('K', location, location[0]+str(int(location[1])-2), castling = 'Q'))
        if king_side:
            moves.append(chess_move('K', location, location[0]+str(int(location[1])+2), castling = 'K'))
        return moves

class chess_move:
    def __init__(self, piece_type, starting_location, ending_location, promotion = False, capture = False, en_passant = False, castling = False):
        self.piece_type = piece_type
        self.starting_location = starting_location
        self.ending_location = ending_location
        self.promotion = promotion
        self.capture = capture
        self.en_passant = en_passant
        self.castling = castling

    def print_move(self):
        column_names = list('abcdefgh')
        starting_position = column_names[int(self.starting_location[1])-1]+self.starting_location[0]
        ending_position = column_names[int(self.ending_location[1])-1]+self.ending_location[0]

        if self.promotion and self.capture:
            return self.piece_type+": "+starting_position+","+ending_position+","+"Capture, "+"P="+self.promotion
        elif self.promotion:
            return self.piece_type+": "+starting_position+","+ending_position+","+"P="+self.promotion
        elif self.capture:
            return self.piece_type+": "+starting_position+","+ending_position+','+"Capture"
        elif self.castling:
            return self.piece_type+": "+starting_position+","+ending_position+','+"Castling"+'-'+self.castling
        else:
            return self.piece_type+": "+starting_position+","+ending_position

if __name__ == "__main__":
    c = chess_game()
    c.print_board()
    #c.previous_move = chess_move('P', '24','44')
    moves = c.get_all_legal_moves()
    for move in moves:
        print move.print_move()
