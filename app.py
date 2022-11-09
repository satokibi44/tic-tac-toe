import sys
from backend.a import Board
def handler(event, context): 
    user1 = event.get('queryStringParameters').get('USER1')
    user2 = event.get('queryStringParameters').get('USER2')
    user1_color = "black"
    user2_color = "white"
    board = event.get('queryStringParameters').get('board')

    print(user1)


    board_inst = Board()
    board_inst.mk_board(board)
    for i in range(board_inst.BOARD_SIZE*board_inst.BOARD_SIZE):
        board_inst.checkIN(i)
       
    return 'Hello from AWS Lambda using Python' + sys.version + '!'