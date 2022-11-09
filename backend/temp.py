from board import Board

board_inst = Board()
board = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '-1', '0', '0',
         '0', '0', '0', '0', '-1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
board_inst.mk_board(board)
print(board_inst.RawBoard)
ans = []

for x in range(board_inst.BOARD_SIZE):
        for y in range(board_inst.BOARD_SIZE):
            if board_inst.checkMobility(x,y,-1):
                ans.append((x,y))
                
print(ans)