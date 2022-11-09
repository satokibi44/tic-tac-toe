import unittest


class TestPlayer(unittest.TestCase):
    def test_corner_player(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        board_inst = Board()
        corner_player = CornerPlayer()
        next_move = corner_player.next_move(1, board_inst)
        self.assertEqual(next_move, (3, 2))
    
    

    def test_ひっくり返えった後のboardを算出(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        board_inst = Board()
        corner_player = CornerPlayer()
        board_inst.CurrentColor = 1
        next_move = corner_player.next_move(
            board_inst.CurrentColor, board_inst)
        move = board_inst.add_wall2move(next_move)
        board_inst.flipDiscs(move[0], move[1])
        board = board_inst.RawBoard
        board_ans = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 1, 1, 1, 0, 0, 0, 2], [2, 0, 0, 0, 1, -1, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        self.assertEqual(board, board_ans)
        
    def test_ひっくり返る場所の算出(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        import copy
        board_inst = Board()
        corner_player = CornerPlayer()
        prev_board = copy.copy(board_inst.RawBoard)
        board_inst.CurrentColor = 1
        next_move = corner_player.next_move(
            board_inst.CurrentColor, board_inst)
        move = board_inst.add_wall2move(next_move)
        board_inst.flipDiscs(move[0], move[1])
        board = board_inst.RawBoard
        diff = board_inst.get_diff_board(prev_board)
        print(diff)
        pass
