import sys
import json
from backend.board import Board
#from game import Reversi
#from backend.play import Play
#import copy

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
        
    now_board = []
    flip_point = []
    
    responce = {
        'statusCode': 200,
        'body': {
            'next_board':now_board,
            'flip_point':flip_point,
            'next_player':-now_user["color"]
        }
    }
    
    return responce
