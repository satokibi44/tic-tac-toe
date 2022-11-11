import unittest

class TestBoard(unittest.TestCase):

    def test_mk_board(self):
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
                 '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        board_inst.mk_board(board)
        ans_board = [[2,2,2,2,2,2,2,2,2,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,1,-1,0,0,0,2], [2,0,0,0,-1,1,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,0,0,0,0,0,0,0,0,2], [2,2,2,2,2,2,2,2,2,2]]
        
        assert(ans_board, board_inst.RawBoard)
        
    def test_checkMobility(self):
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
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
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        ans = board_inst.delete_wall_from_moves([(3, 4), (4, 3), (5, 6), (6, 5)])
        self.assertEqual([(2, 3), (3, 2), (4, 5), (5, 4)], ans)
        
    def test_get_legal_moves(self):
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
         '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        board_inst.mk_board(board)
        ans = board_inst.get_legal_moves(-1)
        self.assertEqual([(2, 3), (3, 2), (4, 5), (5, 4)], ans)
        
    def test_ひっくり返えった後のboardを算出(self):
        from backend.player2 import CornerPlayer
        from backend.board import Board
        corner_player = CornerPlayer()
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        #wallついてない
        move = corner_player.next_move(now_user['color'], board_inst)
        board = board_inst.put_disc(now_user['color'], move[0], move[1])
        board_inst.RawBoard = board
        board_ans = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, -1, 1, 0, 0, 0, 2], 
                     [2, 0, 0, 0, -1, -1, 0, 0, 0, 2], 
                     [2, 0, 0, 0, -1, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
                     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        flag = True
        for i in range(len(board_ans)):
            for i2 in range(len(board_ans[i])):
                if not board[i][i2] == board_ans[i][i2]:
                    flag = False
        self.assertEqual(flag, True)
    
    def test_現在の得点を算出(self):
        pass
        
    def test_ひっくり返る場所の算出(self):
        from backend.player2 import CornerPlayer
        from backend.board import Board
        import copy
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        corner_player = CornerPlayer()
        prev_board = copy.copy(board_inst.RawBoard)
        move = corner_player.next_move(
            board_inst.CurrentColor, board_inst)
        board = board_inst.get_flippable_discs(board_inst.CurrentColor, move[0], move[1])
        board_inst.RawBoard = board
        #壁なし
        diff = board_inst.get_diff_board(prev_board)
        ans_diff = [[True, True, True, True, True, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True],
                    [True, True, True, True, False, True, True, True, True, True], 
                    [True, True, True, True, False, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True], 
                    [True, True, True, True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True, True, True, True]]
        flag = True
        for i in range(len(diff)):
            for i2 in range(len(diff[i])):
                if not ans_diff[i][i2] == diff[i][i2]:
                    flag = False
        self.assertEqual(flag, True)
    
