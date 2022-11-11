import unittest


class TestPlayer(unittest.TestCase):
    def test_corner_player(self):
        from backend.player2 import CornerPlayer
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        corner_player = CornerPlayer()
        next_move = corner_player.next_move(now_user["color"], board_inst)
        self.assertEqual(next_move, (3, 5))
        
    def test_greedy_player(self):
        from backend.player2 import GreedyPlayer
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        greedy_player = GreedyPlayer()
        next_move = greedy_player.next_move(now_user["color"], board_inst)
        self.assertEqual(board_inst.add_wall2move(next_move), board_inst.add_wall2move((2, 4)))
        
    def test_min_max_player(self):
        from backend.player2 import MiniMaxPlayer
        from backend.board import Board
        now_user = {"strategy": "GREEDY", "color": 'white'}
        board_inst = Board(now_user['color'])
        min_max_player = MiniMaxPlayer()
        next_move = min_max_player.next_move(now_user["color"], board_inst)
        self.assertEqual(next_move, (2, 3))