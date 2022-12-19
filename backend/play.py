from board import Board
from game2 import Reversi
import copy
import numpy

class Play():
    def __init__(self, board, user) -> None:
        self.now_user = user
        self.board_inst = Board(self.now_user['color'])
        self.board_inst.mk_board(board)
        self.board_inst.initMovable()
        
    
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
        
        try:
            next_move = player.next_move(now_user["color"] , self.board_inst)
        except IndexError as e:
            print(e)
            res_board = self.board_inst.delete_wall()
            return res_board, self.board_inst.get_diff_board(res_board)
            
        board = self.board_inst.put_disc(now_user["color"], next_move[0], next_move[1])
        self.board_inst.RawBoard = board
        board = self.board_inst.delete_wall()
        
        diff = self.board_inst.get_diff_board(prev_board)
        
        
        return board, diff
        
    def tic_tac_toe_human(self, now_user, flip_point):
        prev_board = copy.copy(self.board_inst.RawBoard)
        color = 1 if now_user['color'] == 'black' else -1
        flag = True
        if not self.board_inst.checkMobility(flip_point[0]+1,flip_point[1]+1,color):
            flag = False
            board = self.board_inst.delete_wall()
            return board, self.board_inst.get_diff_board(board), flag
        board = self.board_inst.put_disc(now_user["color"], flip_point[0], flip_point[1])
        self.board_inst.RawBoard = board
        board = self.board_inst.delete_wall()
        
        diff = self.board_inst.get_diff_board(prev_board)
        
        return board, diff, flag