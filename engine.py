def evaluate_position(chess_game):
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
