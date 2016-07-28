
KNIGHT_POSITION_WEIGHT = 1
PAWN_STRUCTURE_WEIGHT = 1
BISHOP_POSITION_WEIGHT = 1
ROOK_POSITION_WEIGHT = 1
PASSED_PAWN_WEIGHT = 1
KING_SAFETY_WEIGHT = 1
KING_CENTRALITY_WEIGHT = 1

def evaluate_material_score(chess_game):
    side_to_move = chess_game.side_to_move[0].upper()
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
    pass

def evaluate_pawn_structure(chess_game): # J
    pass

def evaluate_bishop_positions(chess_game): # B
    pass

def evaluate_rook_positions(chess_game): # J
    pass

def evaluate_passed_pawns(chess_game): # J
    pass

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
    
