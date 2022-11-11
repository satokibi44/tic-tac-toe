from operator import le
import random
import numpy as np
from reversi.strategies import AbstractStrategy, Timer
 
class CornerPlayer(AbstractStrategy):
    def next_move(self, color, board):
        random.seed(100)
        size = board.size
        #wallついてない
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner
 
        return random.choice(legal_moves)
 
class GreedyPlayer(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        base_score = board._black_score if color == 'black' else board._white_score
        max_score = base_score
        max_move = None
        for move in legal_moves:
            move_x, move_y = move
            score = base_score + len(board.get_flippable_discs(color, move_x, move_y))
            if score > max_score:
                max_score = score
                max_move = move
        return max_move
 
class EdgePlayer(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for move in legal_moves:
            move_x, move_y = move
            if move_x in [0, size-1] or move_y in [0, size-1]:
                return move
        return random.choice(legal_moves)
 
class MiniMaxPlayer(AbstractStrategy):
    """decide next move by MinMax method
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000
 
        self.depth = depth
        self.evaluator = evaluator
 
 
    def next_move(self, color, board):
        """next_move
        """
        pid = Timer.get_pid(self)  # タイムアウト監視用のプロセスID
 
        # select best move
        next_color = 'white' if color == 'black' else 'black'
        next_moves = {}
        best_score = self._MIN if color == 'black' else self._MAX
        legal_moves = board.get_legal_moves(color)
        for move in legal_moves:
            board.put_disc(color, *move)
            score = self.get_score(next_color, board, self.depth-1, pid=pid)
            board.undo()
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)
           
            # memorize next moves
            if score not in next_moves:
                next_moves[score] = []
            next_moves[score].append(move)
 
        return random.choice(next_moves[best_score])  # random choice if many best scores
 
    def board_score(self, color, board, possibility_b, possibility_w):
        score = [[100,  30, 50, 50, 50, 50,  30, 100],
                [  30, -25, 45, 45, 45, 45, -25, 30],
                [  50,  45, 50, 50, 50, 50,  45, 50],
                [  50,  45, 50, 50, 50, 50,  45, 50],
                [  50,  45, 50, 50, 50, 50,  45, 50],
                [  50,  45, 50, 50, 50, 50,  45, 50],
                [  30, -25, 45, 45, 45, 45, -25, 30],
                [  100, 30, 50, 50, 50, 50,  30, 100]]
        product = np.multiply(score,board.get_board_info())
        return np.sum(product)
       
        # return self.evaluator.evaluate(color=color, board=board, possibility_b=possibility_b, possibility_w=possibility_w)
 
    def get_score(self, color, board, depth, pid=None):
        """get_score
        """
        # game finish or max-depth
        legal_moves_b_bits = board.get_legal_moves_bits('black')
        legal_moves_w_bits = board.get_legal_moves_bits('white')
        is_game_end = True if not legal_moves_b_bits and not legal_moves_w_bits else False
        if is_game_end or depth <= 0:
            return self.board_score(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits))  # noqa: E501
 
        # in case of pass
        legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
        next_color = 'white' if color == 'black' else 'black'
        if not legal_moves_bits:
            return self.get_score(next_color, board, depth, pid=pid)
 
        # get best score
        best_score = self._MIN if color == 'black' else self._MAX
        size = board.size
        mask = 1 << ((size**2)-1)
        for y in range(size):
            for x in range(size):
                if legal_moves_bits & mask:
                    board.put_disc(color, x, y)
                    score = self.get_score(next_color, board, depth-1, pid=pid)
                    board.undo()
                    best_score = max(best_score, score) if color == 'black' else min(best_score, score)
                mask >>= 1
 
        return best_score

class Corner1_Edge2_Ungreedy3(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner

        for move in legal_moves:
            move_x, move_y = move
            if move_x in [0,size-1] or move_y in [0,size-1]:
                return move
        
        base_score = board._black_score if color == 'black' else board._white_score
        max_score = base_score
        max_move = random.choice(legal_moves)
        
        for move in legal_moves:
            move_x, move_y = move
            score = base_score + len(board.get_flippable_discs(color,move_x,move_y))
            if score < max_score:
                max_score = score
                max_move = move
        return max_move