import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './backend'))

from backend.play import Play

def handler(event, context):
    user_color = event['queryStringParameters']['now_user_color']
    user_strategy = event['queryStringParameters']['now_user_strategy']
    board = eval(event['queryStringParameters']['board'])
    user = {"strategy": user_strategy, "color": user_color}
    fllipable = True
    if user['strategy'] == 'human':
        play = Play(board,user)
        flip_point = eval(event['queryStringParameters']['flip_point'])
        board, flip_point, fllipable = play.tic_tac_toe_human(user, flip_point)
    else:
        play = Play(board,user)
        board, flip_point = play.tic_tac_toe(user)
    
    body = {
            'next_board':board,
            'flip_point':flip_point,
            'next_player':-play.board_inst.CurrentColor if fllipable else play.board_inst.CurrentColor
        }
    
    res = {
        "statusCode" : 200,
        "headers" : {"Access-Control-Allow-Origin" : '*'},
        "body" : json.dumps(body)
    }
    
    return res