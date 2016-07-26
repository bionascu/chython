# Helper function for testing Chython's game tree against the perft results
# available at https://chessprogramming.wikispaces.com/Perft+Results
#
# The count_positions function takes two arguments:
#
#       1. chess_game - A Chython chess_game object
#       2. depth - the depth of the desired perft search
#
# It returns the number of positions at the chosen depth for comparison
# against the perft tables at the given link.

import chython
import gui_chython
import copy

# Standard starting position
test_1 = chython.chess_game()
test_1.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','WN','WB','WQ','WK','WB','WN','WR','00'],
            ['00','WP','WP','WP','WP','WP','WP','WP','WP','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','BP','BP','BP','BP','BP','BP','BP','BP','00'],
            ['00','BR','BN','BB','BQ','BK','BB','BN','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]

# Kiwi Pete
test_2 = chython.chess_game()
test_2.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','--','--','--','WK','--','--','WR','00'],
            ['00','WP','WP','WP','WB','WB','WP','WP','WP','00'],
            ['00','--','--','WN','--','--','WQ','--','BP','00'],
            ['00','--','BP','--','--','WP','--','--','--','00'],
            ['00','--','--','--','WP','WN','--','--','--','00'],
            ['00','BB','BN','--','--','BP','BN','BP','--','00'],
            ['00','BP','--','BP','BP','BQ','BP','BB','--','00'],
            ['00','BR','--','--','--','BK','--','--','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]

test_3 = chython.chess_game()
test_3.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','WP','--','WP','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','WR','--','--','--','BP','--','BK','00'],
            ['00','WK','WP','--','--','--','--','--','BR','00'],
            ['00','--','--','--','BP','--','--','--','--','00'],
            ['00','--','--','BP','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','00','00','00','00','00','00','00','00','00']]
test_3.can_castle_kingside['B'][-1] = False
test_3.can_castle_queenside['B'][-1] = False
test_3.can_castle_kingside['W'][-1] = False
test_3.can_castle_queenside['W'][-1] = False

test_4 = chython.chess_game()
test_4.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','--','--','WQ','--','WR','WK','--','00'],
            ['00','WP','BP','--','WP','--','--','WP','WP','00'],
            ['00','BQ','--','--','--','--','WN','--','--','00'],
            ['00','WB','WB','WP','--','WP','--','--','--','00'],
            ['00','BN','WP','--','--','--','--','--','--','00'],
            ['00','--','BB','--','--','--','BN','BB','WN','00'],
            ['00','WP','BP','BP','BP','--','BP','BP','BP','00'],
            ['00','BR','--','--','--','BK','--','--','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]
test_4.can_castle_kingside['W'][-1] = False
test_4.can_castle_queenside['W'][-1] = False

test_5 = chython.chess_game()
test_5.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','WN','WB','WQ','WK','--','--','WR','00'],
            ['00','WP','WP','WP','--','WN','BN','WP','WP','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','WB','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','BP','--','--','--','--','--','00'],
            ['00','BP','BP','--','WP','BB','BP','BP','BP','00'],
            ['00','BR','BN','BB','BQ','--','BK','--','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]
test_4.can_castle_kingside['B'][-1] = False
test_4.can_castle_queenside['B'][-1] = False

test_6 = chython.chess_game()
test_6.board = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','--','--','--','--','WR','WK','--','00'],
            ['00','--','WP','WP','--','WQ','WP','WP','WP','00'],
            ['00','WP','--','WN','WP','--','WN','--','--','00'],
            ['00','--','--','WB','--','WP','--','BB','--','00'],
            ['00','--','--','BB','--','BP','--','WB','--','00'],
            ['00','BP','--','BN','BP','--','BN','--','--','00'],
            ['00','--','BP','BP','--','BQ','BP','BP','BP','00'],
            ['00','BR','--','--','--','--','BR','BK','--','00'],
            ['00','00','00','00','00','00','00','00','00','00']]
test_6.can_castle_kingside['B'][-1] = False
test_6.can_castle_queenside['B'][-1] = False
test_6.can_castle_kingside['W'][-1] = False
test_6.can_castle_queenside['W'][-1] = False

def undo_move_sequence(game, move_sequence):
    for move in reversed(move_sequence):
        game.unupdate_board(move)

def do_move_sequence(game, move_sequence):
    for move in move_sequence:
        game.update_board(move)

def count_positions(game, depth):
    depth_tracker = 0
    position_counter = 0
    todo = [([], depth_tracker)]
    while len(todo)>0:
        current_sequence, current_depth = todo.pop(-1)
        do_move_sequence(game, current_sequence)
        potential_moves = game.get_all_legal_moves()
        new_depth = current_depth+1
        if new_depth == depth:
            position_counter+=len(potential_moves)
        elif new_depth < depth:
            for move in potential_moves:
                new_sequence = copy.deepcopy(current_sequence)
                new_sequence.append(copy.deepcopy(move))
                todo.append((new_sequence, new_depth))
        undo_move_sequence(game, current_sequence)
    return position_counter

if __name__=="__main__":
    print count_positions(test_3, 3)
