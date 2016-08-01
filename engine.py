
KNIGHT_POSITION_WEIGHT = 1
PAWN_STRUCTURE_WEIGHT = 1
BISHOP_POSITION_WEIGHT = 1
ROOK_POSITION_WEIGHT = 1
PASSED_PAWN_WEIGHT = 1
KING_SAFETY_WEIGHT = 1
KING_CENTRALITY_WEIGHT = 1

def evaluate_material_score(chess_game):
    side_to_move = chess_game.side_to_move
    side_to_move_counter = 0
    other_side_counter = 0
    piece_values = {'Q':9,'R':5,'B':3,'N':3,'P':1,'K':500}
    for row in chess_game.board:
        for occupant in row:
            if occupant[0]==side_to_move:
                side_to_move_counter+=piece_values[occupant[1]]
            elif occupant[0]!='-' and occupant[0]!='0':
                other_side_counter+=piece_values[occupant[1]]
    return side_to_move_counter-other_side_counter

def evaluate_knight_positions(chess_game): # B
    side_to_move = chess_game.side_to_move 
    side_to_move_counter = 0
    other_side_counter = 0
    max_value = 8.0
    values = [1,2,3,4]
    position_values = [[0]*9]*9
    for i in range(1, 9):
        for j in range(1, 9):
            if (i in [4,5]) and (j in range(4, 6)):
                position_values[i][j] = values[3]
            if i in (3,6) and j in range(3, 7):
                position_values[i][j] = values[2]
            if i in (2,7) and j in range(2, 8):
                position_values[i][j] = values[1]
            if i in (1,8):
                position_values[i][j] = values[0]

            if chess_game.board[i][j][1] == 'N':
                if chess_game.board[i][j][0] == side_to_move:
                    side_to_move_counter += position_values[i][j]
                else:
                    other_side_counter += position_values[i][j]
    # Scaling
    scaled_value = (side_to_move_counter - other_side_counter) / max_value
    return scaled_value

def get_doubled_pawns(chess_game, pawn_color):
    score = 2
    for column in range(1,9):
        pawn_count = 0
        for row in range(1,9):
            piece = chess_game[str(row)+str(column)]
            if piece == pawn_color:
                pawn_count+=1
        score-=(pawn_count-1)*.5
    return max(score, 0)

def get_pawn_centrality_score(chess_game, pawn_color):
    central_rows = (0,0)
    for column in range(4,5):
        for row in range(1,9):
            piece = chess_game[str(row)+str(column)]
            if piece == pawn_color:
                central_rows[column-4] = row
                break
    c4, c5 = central_rows
    if c4 in [4,5] and c5 == c4:
        return 1
    elif c4 in [3,4,5] and c5 in [3,4,5] and abs(c4-c5)<=1:
        return .5
    else:
        return 0

def evaluate_pawn_structure(chess_game): # J
    side_to_move = chess_game.side_to_move
    opponent_color = chess_game.opponent_color
    scores = {'WP': 0, 'BP': 0}
    for pawn_color in [side_to_move+'P', opponent_color+'P']:
        doubled_pawns = get_doubled_pawns(chess_game, pawn_color)
        centrality_score = get_pawn_centrality_score(chess_game, pawn_color)
        scores[pawn_color] = (doubled_pawns+centrality_score)/3.0 # max of 3, 2 from doubled pawns (or lack thereof, 1 from pawn centrality)
    return scores[side_to_move+'P']-scores[opponent_color+'P']


def evaluate_bishop_positions(chess_game): # B
    side_to_move = chess_game.side_to_move
    side_to_move_counter = 0
    opponent_counter = 0
    bonus = 6.0
    max_value = 14.0 + bonus
    # Possible attacking squares
    side_bishop_moves = [move for move in chess_game.get_all_legal_moves() if move.piece_type == 'B']
    side_to_move_counter += len(side_bishop_moves)
    chess_game.side_to_move = chess_game.opponent_color
    opponent_bishop_moves = [move for move in chess_game.get_all_legal_moves() if move.piece_type == 'B']
    opponent_counter += len(opponent_bishop_moves)
    chess_game.side_to_move = side_to_move
    # Bonus for both bishops
    bishop_count = {'side':0, 'opponent':0}
    for row in chess_game.board:
        for occupant in row:
            if occupant[1] == 'B':
                if occupant[0] == side_to_move:
                    bishop_count['side'] += 1
                else:
                    bishop_count['opponent'] += 1
    if bishop_count['side'] == 2: side_to_move_counter += bonus
    if bishop_count['opponent'] == 2: opponent_counter += bonus
    # Scaling
    scaled_value = (side_to_move_counter - opponent_counter) / max_value
    return scaled_value

def evaluate_rook_positions(chess_game): # B
    side_to_move = chess_game.side_to_move
    side_to_move_counter = 0
    opponent_counter = 0
    bonus = 2.0
    max_value = 28.0 + bonus
    # Possible attacking squares
    side_rook_moves = [move for move in chess_game.get_all_legal_moves() if move.piece_type == 'R']
    side_to_move_counter += len(side_rook_moves)
    chess_game.side_to_move = chess_game.opponent_color
    opponent_rook_moves = [move for move in chess_game.get_all_legal_moves() if move.piece_type == 'R']
    opponent_counter += len(opponent_rook_moves)
    chess_game.side_to_move = side_to_move
    # Bonus for 7th rank 
    for occupant in chess_game.board[7]:
        if occupant[1] == 'R':
            if occupant[0] == 'W':
                if side_to_move == 'W':
                    side_to_move_counter += bonus
                else:
                    opponent_counter += bonus
    for occupant in chess_game.board[2]:
        if occupant[1] == 'R':
            if occupant[0] == 'B':
                if side_to_move == 'B':
                    side_to_move_counter += bonus
                else:
                    opponent_counter += bonus
    # Scaling
    scaled_value = (side_to_move_counter - opponent_counter) / max_value
    return scaled_value

def get_passed_pawn_score_in_this_column(chess_game, column, color):
    passed = 0
    if color == 'W':
        queening_row = 8
        for row in range(2,8):
            if game[str(row)+str(column)]=='WP':
                passed = row
                for row2 in range(row+1,8):
                    if game[str(row2)+str(column-1)]=='BP' or game[str(row2)+str(column+1)]=='BP':
                        passed = 0
    else:
        queening_row = 1
        for row in range(7,1,-1):
            if game[str(row)+str(column)]=='BP':
                passed = 8-row
                for row2 in range(row-1,1,-1):
                    if game[str(row2)+str(column-1)]=='WP' or game[str(row2)+str(column+1)]=='WP':
                        passed = 0
    return passed



def evaluate_passed_pawns(chess_game): # J
    side_to_move = chess_game.side_to_move
    opponent_color = chess_game.opponent_color
    scores = {'W': 0, 'B': 0}
    for color = ['W', 'B']:
        score = 0
        for column in range(1,9):
            score += get_passed_pawn_score_in_this_column(chess_game, column, color)
        score[color] = min(1,score/14.0)
    return score[side_to_move]-score[opponent_color]

def evaluate_king_safety(chess_game): # j
    pass

def evaluate_position(chess_game):
    m_score = evaluate_material_score(chess_game)
    n_score = KNIGHT_POSITION_WEIGHT*evaluate_knight_positions(chess_game)
    p_score = PAWN_STRUCTURE_WEIGHT*evaluate_pawn_structure(chess_game)
    b_score = BISHOP_POSITION_WEIGHT*evaluate_bishop_positions(chess_game)
    r_score = ROOK_POSITION_WEIGHT*evaluate_rook_positions(chess_game)
    pp_score = PASSED_PAWN_WEIGHT*evaluate_passed_pawns(chess_game)
    ks_score = KING_SAFETY_WEIGHT*evaluate_king_safety(chess_game)
    return m_score+n_score+p_score+b_score+r_score+pp_score+ks_score
