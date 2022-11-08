import sys
from app.game import Reversi
def handler(event, context): 
    user1 = event.get('queryStringParameters').get('USER1')
    user2 = event.get('queryStringParameters').get('USER2')
    user1_color = "black"
    user2_color = "white"
    board = event.get('queryStringParameters').get('board')

    user1_strate = Reversi[user1]
    user2_strate = Reversi[user1]

    user1_strate.next_move(user1_color,board)
    user2_strate.next_move(user2_color,board)
       
    return 'Hello from AWS Lambda using Python' + sys.version + '!'