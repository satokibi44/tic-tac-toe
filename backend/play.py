from board import Board
from game2 import Reversi
import copy

class Play():
    def __init__(self, board, user) -> None:
        self.now_user = user
        self.board_inst = Board(self.now_user['color'])
        self.board_inst.mk_board(board)
        self.board_inst.initMovable()
        print("a")
        
    
    def check_mobilities(self, color):
        mobilities = []
        for x in range(self.board_inst.size):
             for y in range(self.board_inst.size):
                   if self.board_inst.checkMobility(x,y,color):
                     mobilities.append((x,y))
        mobilities = self.delete_wall_from_moves(mobilities)
        return mobilities
    
    def tic_tac_toe(self, now_user):
        prev_board = copy.copy(self.board_inst.RawBoard)
        player = Reversi[now_user["strategy"]]
        
        next_move = player.next_move(now_user["color"] , self.board_inst)
        
        board = self.board_inst.put_disc(now_user["color"], next_move[0], next_move[1])
        self.board_inst.RawBoard = board
        
        diff = self.board_inst.get_diff_board(prev_board)
        
        return board, diff