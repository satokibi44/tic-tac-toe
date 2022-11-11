import unittest


class TestPlayer(unittest.TestCase):
    def test_corner_player(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        board_inst = Board()
        corner_player = CornerPlayer()
        next_move = corner_player.next_move(1, board_inst)
        self.assertEqual(next_move, (3, 2))
        
    def test_greedy_player(self):
        from backend.player import GreedyPlayer
        from backend.board import Board
        board_inst = Board()
        greedy_player = GreedyPlayer()
        next_move = greedy_player.next_move(1, board_inst)
        self.assertEqual(next_move, (2, 3))
        
    def test_min_max_player(self):
        from backend.player import MiniMaxPlayer
        from backend.board import Board
        board_inst = Board()
        min_max_player = MiniMaxPlayer()
        next_move = min_max_player.next_move(1, board_inst)
        self.assertEqual(next_move, (2, 3))