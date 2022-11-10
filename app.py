import sys
from backend.board import Board
from game import Reversi
from play import Play
import copy

def handler(event, context): 
    user1 = event.get('queryStringParameters').get('USER1')
    user2 = event.get('queryStringParameters').get('USER2')
    user1_color = "black"
    user2_color = "white"
    now_user_color = event.get('queryStringParameters').get('now_user_color')
    now_user = {}
    board = event.get('queryStringParameters').get('board')
    
    if now_user_color == "Black":
        now_user["color"] = 1
        now_user["strategy"] = user1
    else:
        now_user["color"]  = -1
        now_user["strategy"] = user2
        
    play = Play(board)
    mobilities = play.get_legal_moves(now_user_color) 
    player = Reversi[now_user["strategy"]]
    next_move = player.next_move(1, play.board_inst)
    prev_board = copy.copy(board_inst.RawBoard)
    
    
    return 'Hello from AWS Lambda using Python' + sys.version + '!'