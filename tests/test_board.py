import unittest

class TestBoard(unittest.TestCase):

    def test_mk_board(self):
        from backend.board import Board
        board_inst = Board()
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
                 '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        board_inst.mk_board(board)
        ans_board = [[2,2,2,2,2,2,2,2,2,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,1,-1,0,0,0,2], [2,0,0,0,-1,1,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,2,2,2,2,2,2,2,2,2]]
        
        assert(ans_board, board_inst.RawBoard)
        
    def test_checkMobility(self):
        from backend.board import Board
        board_inst = Board()
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
         '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        board_inst.mk_board(board)
        ans = []

        for x in range(board_inst.size):
             for y in range(board_inst.size):
                   if board_inst.checkMobility(x,y,-1):
                     ans.append((x,y))
        self.assertEqual([(3, 4), (4, 3), (5, 6), (6, 5)], ans)
        
    def test_delete_wall(self):
        from backend.board import Board
        board_inst = Board()
        ans = board_inst.delete_wall_from_moves([(3, 4), (4, 3), (5, 6), (6, 5)])
        self.assertEqual([(2, 3), (3, 2), (4, 5), (5, 4)], ans)
        
    def test_get_legal_moves(self):
        from backend.board import Board
        board_inst = Board()
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
         '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        board_inst.mk_board(board)
        ans = board_inst.get_legal_moves(-1)
        self.assertEqual([(2, 3), (3, 2), (4, 5), (5, 4)], ans)
        
    def test_ひっくり返えった後のboardを算出(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        board_inst = Board()
        corner_player = CornerPlayer()
        board_inst.CurrentColor = 1
        next_move = corner_player.next_move(
            board_inst.CurrentColor, board_inst)
        move = board_inst.add_wall2move(next_move)
        board = board_inst.get_flippable_discs(board_inst.CurrentColor, move[0], move[1])
        board_inst.RawBoard = board
        board_ans = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 1, 1, 1, 0, 0, 0, 2], [2, 0, 0, 0, 1, -1, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        flag = True
        for i in range(len(board_ans)):
            if not all(board[i] == board_ans[i]):
                flag = False
        self.assertEqual(flag, True)
    
    def test_現在の得点を算出(self):
        pass
        
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
        board = board_inst.get_flippable_discs(board_inst.CurrentColor, move[0], move[1])
        board_inst.RawBoard = board
        diff = board_inst.get_diff_board(prev_board)
        print(diff)
    
