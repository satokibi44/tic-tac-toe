import unittest


class TestPlayer(unittest.TestCase):
    def test_corner_player(self):
        from backend.player import CornerPlayer
        from backend.board import Board
        board_inst = Board()
        corner_player = CornerPlayer()
        next_move = corner_player.next_move(1, board_inst)
        self.assertEqual(next_move, (3, 2))