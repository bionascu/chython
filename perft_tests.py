import chython

test_1 = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','WN','WB','WQ','WK','WB','WN','WR','00'],
            ['00','WP','WP','WP','WP','WP','WP','WP','WP','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','--','--','--','--','--','--','--','--','00'],
            ['00','BP','BP','BP','BP','BP','BP','BP','BP','00'],
            ['00','BR','BN','BB','BQ','BK','BB','BN','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]

test_2 = [['00','00','00','00','00','00','00','00','00','00'],
            ['00','WR','--','--','--','WK','--','--','WR','00'],
            ['00','WP','WP','WP','WB','WB','WP','WP','WP','00'],
            ['00','--','--','WN','--','--','WQ','--','BP','00'],
            ['00','--','BP','--','--','WP','--','--','--','00'],
            ['00','--','--','--','WP','WN','--','--','--','00'],
            ['00','BB','BN','--','--','BP','BN','BP','--','00'],
            ['00','BP','--','BP','BP','BQ','BP','BB','--','00'],
            ['00','BR','--','--','--','BK','--','--','BR','00'],
            ['00','00','00','00','00','00','00','00','00','00']]

def test(board, max_depth):
    game = chython.chess_game()
    game.board = board
    states = 1
    current_depth = 0
    todo = game.get_all_legal_moves()
    count = 0
    for move in todo:
        print "NEW 1ST MOVE"
        game.update_board(move)
        next_moves = game.get_all_legal_moves()
        print [x.print_move() for x in next_moves]
        for move2 in next_moves:
            print move.print_move(), move2.print_move()
            game.update_board(move2)
            count+=len(game.get_all_legal_moves())
            game.unupdate_board(move2)
        game.unupdate_board(move)
    print count


test(test_1, 1)
test(test_2, 1)
