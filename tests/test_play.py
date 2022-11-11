import unittest
import sys
import os
sys.path.append( "/Users/sf/Dropbox/project/tic-tac-toe/backend" )

class Play(unittest.TestCase):

    def test_tic_tac_toe(self):
        from backend.play import Play
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
                 '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        user = {"strategy": "GREEDY", "color": 'white'}
        play = Play(board,user)
        board, diff = play.tic_tac_toe(user)
        print("OK")
        
    def test_tic_tac_toe_2nd(self):
        from backend.play import Play
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '-1', '-1', '-1', '0', '0',
                 '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        user = {"strategy": "GREEDY", "color": 'black'}
        play = Play(board,user)
        board, diff = play.tic_tac_toe(user)
        print("OK")
