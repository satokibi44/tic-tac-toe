from board import Board

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