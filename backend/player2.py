from operator import le
import random
import numpy as np
from abstract import AbstractStrategy, Timer
 
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
        b = score,board.get_board_info()
        
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
    
class SwitchSizeError(Exception):
    """
    入力サイズのエラー
    """
    pass

class _Switch_(AbstractStrategy):
    """
    複数戦略を切り替える
    """
    def __init__(self, turns=None, strategies=None):
        if len(turns) != len(strategies):
            raise SwitchSizeError

        self.turns = turns
        self.strategies = strategies

    def next_move(self, color, board):
        """
        次の一手
        """
        disc_num = board._black_score + board._white_score

        # 現在の手数が閾値以下
        strategy = self.strategies[-1]

        for i, turn in enumerate(self.turns):
            if disc_num - 4 <= turn:
                strategy = self.strategies[i]
                break

        return strategy.next_move(color, board)


class Switch(_Switch_):
    """Switch + Measure
    """
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)
    
# 植村くん
class middlePlayer(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        near_edges=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
        near2_edges=[(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)]
        near3_edges=[(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
        near4_edges=[(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)]
        near5_edges = near_edges+near2_edges+near3_edges+near4_edges
 
        new_legal_moves=[]
        for move in legal_moves:
            if move not in near5_edges :
                new_legal_moves.append(move)
 
        for move in new_legal_moves:
            return move
       
        return random.choice(legal_moves)

#日下くん
class doppelplayer(AbstractStrategy):
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
        score = [[150,  -40, 40, 50, 50, 40, -40, 150],
                [  500, -40, 30, 20, 20, 30, 500, -40],
                [  40,  30, 40, 50, 50, 40,  30, 40],
                [  50,  20, 50, 50, 100, 50,  20, 50],
                [  50,  20, 100, 100, 50, 50,  20, 50],
                [  40,  30, 40, 50, 50, 40,  30, 40],
                [  -40, -40, 30, 20, 20, 30, -40, -40],
                [  150, 500, 40, 50, 50, 40,  500, 150]]
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

#村上くん (Switchを使用)

class RandomPlayer(AbstractStrategy):
    def next_move(self, color, board):
        legal_moves = board.get_legal_moves(color)
        return random.choice(legal_moves)

class originalPlayer(AbstractStrategy):
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
        score = [[450,  -50, 80, 50, 50, 80,  -50, 450],
                [  -50, -50, 30, 45, 45, 30, -50, -50],
                [  80,  30, 70, 50, 50, 70,  30, 80],
                [  60,  45, 50, 50, 50, 50,  45, 60],
                [  60,  45, 50, 50, 50, 50,  45, 60],
                [  80,  30, 70, 50, 50, 70,  30, 80],
                [  -50, -50, 30, 45, 45, 30, -50, -50],
                [  450, -50, 80, 50, 50, 80,  -50, 450]]
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