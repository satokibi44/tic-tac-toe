from board import Board
from game import Reversi
import copy

class Play():
    def __init__(self, board) -> None:
        self.board_inst = Board()
        self.board_inst.mk_board(board)
        
    
    def check_mobilities(self, color):
        mobilities = []
        for x in range(self.board_inst.size):
             for y in range(self.board_inst.size):
                   if self.board_inst.checkMobility(x,y,color):
                     mobilities.append((x,y))
        mobilities = self.delete_wall_from_moves(mobilities)
        return mobilities
    
    def tic_tac_toe(self, now_user):
        mobilities = self.get_legal_moves(now_user["color"]) 
        player = Reversi[now_user["strategy"]]
        next_move = player.next_move(now_user["color"], self.board_inst)
        prev_board = copy.copy(self.board_inst.RawBoard)
        
        self.board_inst.CurrentColor = now_user["color"]
        next_move = player.next_move(self.board_inst.CurrentColor, self.board_inst)
        
        move = self.board_inst.add_wall2move(next_move)
        self.board_inst.flipDiscs(move[0], move[1])
        board = self.board_inst.RawBoard
        
        diff = self.board_inst.get_diff_board(prev_board)