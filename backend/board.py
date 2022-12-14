"""
ライブラリ
"""
import numpy as np
import copy
#import GetLegalMoves as BitBoardMethods
"""
定数宣言
"""
# マスの状態
EMPTY = 0  # 空きマス
WHITE = -1  # 白石
BLACK = 1  # 黒石
WALL = 2  # 壁

# ボードのサイズ
BOARD_SIZE = 8

# 方向(2進数)
NONE = 0
LEFT = 2**0  # =1
UPPER_LEFT = 2**1  # =2
UPPER = 2**2  # =4
UPPER_RIGHT = 2**3  # =8
RIGHT = 2**4  # =16
LOWER_RIGHT = 2**5  # =32
LOWER = 2**6  # =64
LOWER_LEFT = 2**7  # =128

# 手の表現
IN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IN_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']

# 手数の上限
MAX_TURNS = 60

"""
ボードの表現
"""


class Board:
    size = BOARD_SIZE

    def __init__(self,color):

        # 全マスを空きマスに設定
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)

        # 壁の設定
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL

        # 初期配置
        self.RawBoard[4, 4] = WHITE
        self.RawBoard[5, 5] = WHITE
        self.RawBoard[4, 5] = BLACK
        self.RawBoard[5, 4] = BLACK

        # 手番
        self.Turns = 0

        # 現在の手番の色
        #self.CurrentColor = BLACK
        self.CurrentColor = 1 if color == 'black' else -1

        # 置ける場所と石が返る方向
        self.MovablePos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.MovableDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        
        # MovablePosとMovableDirを初期化
        self.initMovable()
        
        self.color_black = 1
        self.color_white = -1
        
        self._black_score = self.get_score(self.color_black)
        self._white_score = self.get_score(self.color_white) 
        
        # ビットボードの初期配置
        # center = self.size // 2
        # self._black_bitboard = 1 << ((self.size*self.size-1)-(self.size*(center-1)+center))
        # self._black_bitboard |= 1 << ((self.size*self.size-1)-(self.size*center+(center-1)))
        # self._white_bitboard = 1 << ((self.size*self.size-1)-(self.size*(center-1)+(center-1)))
        # self._white_bitboard |= 1 << ((self.size*self.size-1)-(self.size*center+center))
        # size = self.size
         # 置ける場所の検出用マスク
        #BitMask = namedtuple('BitMask', 'h v d u ur r br b bl l ul')
        '''
        self._mask = BitMask(
            int(''.join((['0'] + ['1'] * (size-2) + ['0']) * size), 2),                                      # 水平方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-2) + ['0'] * size), 2),                          # 垂直方向のマスク値
            int(''.join(['0'] * size + (['0'] + (['1'] * (size-2)) + ['0']) * (size-2) + ['0'] * size), 2),  # 斜め方向のマスク値
            int(''.join(['1'] * size * (size-1) + ['0'] * size), 2),                                         # 上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * (size-1) + ['0'] * size), 2),                           # 右上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * size), 2),                                              # 右方向のマスク値
            int(''.join(['0'] * size + (['0'] + ['1'] * (size-1)) * (size-1)), 2),                           # 右下方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-1)), 2),                                         # 下方向のマスク値
            int(''.join(['0'] * size + (['1'] * (size-1) + ['0']) * (size-1)), 2),                           # 左下方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * size), 2),                                              # 左方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * (size-1) + ['0'] * size), 2)                            # 左上方向のマスク値
        )
        '''
        
    def get_legal_moves_bits(self, color):
        size = self.size
        mask = 1 << ((size**2)-1)
        legal_moves_bits = 0
        for x, y in self.get_legal_moves(color):
            bits = mask >> (y*size+x)
            legal_moves_bits |= bits
                    
        return legal_moves_bits

    """
    どの方向に石が裏返るかをチェック
    """
    
    def get_diff_board(self,prev_board):
        diff_boards = []
        for x in range(len(prev_board)):
            diff_board = []
            for y in range(len(prev_board)):
                if prev_board[x][y] == self.RawBoard[x][y]:
                    diff_board.append(True)
                else:
                    diff_board.append(False)
            diff_boards.append(diff_board)
        return diff_boards
                
                       
    
    def get_legal_moves(self, color):
        color = 1 if color == 'black' else -1
        legal_moves = []
        for x in range(self.size+1):
             for y in range(self.size+1):
                   if self.checkMobility(x,y,color):
                       legal_moves.append((x,y))
        legal_moves = self.delete_wall_from_moves(legal_moves)
        return legal_moves
    
    def delete_wall(self):
        delete_wall_board = []
        for x in range(BOARD_SIZE+1):
            low = []
            for y in range(BOARD_SIZE+1):
                if self.RawBoard[x, y] != 2:
                    low.append(int(self.RawBoard[x, y]))
            if len(low) != 0:
                delete_wall_board.append(low)
        return delete_wall_board
                
    def delete_wall_from_moves(self, moves):
        for i in range(len(moves)):
            moves[i] = (moves[i][0]-1, moves[i][1]-1)
        return moves
        
    def mk_board(self, board):
        for x in range(self.size):
            for y in range(self.size):
                self.RawBoard[y,x] = board[x*8+y]    

    def checkMobility(self, x, y, color):

        # 注目しているマスの裏返せる方向の情報が入る
        dir = 0

        # 既に石がある場合はダメ
        if(self.RawBoard[x, y] != EMPTY):
            return dir

        # 左
        if(self.RawBoard[x - 1, y] == - color):  # 直上に相手の石があるか

            x_tmp = x - 2
            y_tmp = y

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT

        # 左上
        if(self.RawBoard[x - 1, y - 1] == - color):  # 直上に相手の石があるか

            x_tmp = x - 2
            y_tmp = y - 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT

        # 上
        if(self.RawBoard[x, y - 1] == - color):  # 直上に相手の石があるか

            x_tmp = x
            y_tmp = y - 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER

        # 右上
        if(self.RawBoard[x + 1, y - 1] == - color):  # 直上に相手の石があるか

            x_tmp = x + 2
            y_tmp = y - 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT

        # 右
        if(self.RawBoard[x + 1, y] == - color):  # 直上に相手の石があるか

            x_tmp = x + 2
            y_tmp = y

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT

        # 右下
        if(self.RawBoard[x + 1, y + 1] == - color):  # 直上に相手の石があるか

            x_tmp = x + 2
            y_tmp = y + 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT

        # 下
        if(self.RawBoard[x, y + 1] == - color):  # 直上に相手の石があるか

            x_tmp = x
            y_tmp = y + 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER

        # 左下
        if(self.RawBoard[x - 1, y + 1] == - color):  # 直上に相手の石があるか

            x_tmp = x - 2
            y_tmp = y + 2

            # 相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1

            # 相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT

        return dir
    
    def add_wall2move(self,move):
        move = (move[0]+1,move[1]+1)
        return move
    """
    石を置くことによる盤面の変化をボードに反映
    """
    def flipDiscs(self, color, x, y):
        x, y = self.add_wall2move((x, y))
        color = 1 if color == 'black' else -1
        self.CurrentColor = color
        # 石を置く
        RawBoard = copy.copy(self.RawBoard)
        RawBoard[x, y] = color

        # 石を裏返す
        # MovableDirの(y, x)座標をdirに代入
        dir = self.MovableDir[x, y]

        # 左
        if dir & LEFT:  # AND演算子

            x_tmp = x - 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y] = color

                # さらに1マス左に進めてループを回す
                x_tmp -= 1

        # 左上
        if dir & UPPER_LEFT:  # AND演算子

            x_tmp = x - 1
            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y_tmp] = color

                # さらに1マス左上に進めてループを回す
                x_tmp -= 1
                y_tmp -= 1

        # 上
        if dir & UPPER:  # AND演算子

            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while RawBoard[x, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x, y_tmp] = color

                # さらに1マス上に進めてループを回す
                y_tmp -= 1

        # 右上
        if dir & UPPER_RIGHT:  # AND演算子

            x_tmp = x + 1
            y_tmp = y - 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y_tmp] = color

                # さらに1マス右上に進めてループを回す
                x_tmp += 1
                y_tmp -= 1

        # 右
        if dir & RIGHT:  # AND演算子

            x_tmp = x + 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y] = color

                # さらに1マス右に進めてループを回す
                x_tmp += 1

        # 右下
        if dir & LOWER_RIGHT:  # AND演算子

            x_tmp = x + 1
            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y_tmp] = color

                # さらに1マス右下に進めてループを回す
                x_tmp += 1
                y_tmp += 1

        # 下
        if dir & LOWER:  # AND演算子

            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while RawBoard[x, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x, y_tmp] = color

                # さらに1マス下に進めてループを回す
                y_tmp += 1

        # 左下
        if dir & LOWER_LEFT:  # AND演算子

            x_tmp = x - 1
            y_tmp = y + 1

            # 相手の石がある限りループが回る
            while RawBoard[x_tmp, y_tmp] == - color:

                # 相手の石があるマスを自分の石の色に塗り替えている
                RawBoard[x_tmp, y_tmp] = color

                # さらに1マス左下に進めてループを回す
                x_tmp -= 1
                y_tmp += 1
        return RawBoard
                
    def mk_board(self, board):
        for x in range(self.size):
            for y in range(self.size):
                self.RawBoard[x+1,y+1] = board[x*8+y]

    """
    石を置く
    """

    def move(self, x, y):

        # 置く位置が正しいかどうかをチェック
        if x < 1 or BOARD_SIZE < x:
            return False
        if y < 1 or BOARD_SIZE < y:
            return False
        if self.MovablePos[x, y] == 0:
            return False

        # 石を裏返す
        self.flipDiscs(x, y)

        # 手番を進める
        self.Turns += 1

        # 手番を交代する
        self.CurrentColor = - self.CurrentColor

        # MovablePosとMovableDirの更新
        self.initMovable()

        return True

    """
    MovablePosとMovableDirの更新
    """

    def initMovable(self):

        # MovablePosの初期化（すべてFalseにする）
        self.MovablePos[:, :] = False

        # すべてのマス（壁を除く）に対してループ
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):

                # checkMobility関数の実行
                dir = self.checkMobility(x, y, self.CurrentColor)

                # 各マスのMovableDirにそれぞれのdirを代入
                self.MovableDir[x, y] = dir

                # dirが0でないならMovablePosにTrueを代入
                if dir != 0:
                    self.MovablePos[x, y] = True

    """
    終局判定
    """

    def isGameOver(self):

        # 60手に達していたらゲーム終了
        if self.Turns >= MAX_TURNS:
            return True

        # (現在の手番)打てる手がある場合はゲームを終了しない
        if self.MovablePos[:, :].any():
            return False

        # (相手の手番)打てる手がある場合はゲームを終了しない
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):

                # 置ける場所が1つでもある場合はゲーム終了ではない
                if self.checkMobility(x, y, - self.CurrentColor) != 0:
                    return False

        # ここまでたどり着いたらゲームは終わっている
        return True

    """
    パスの判定
    """

    def skip(self):

        # すべての要素が0のときだけパス(1つでも0以外があるとFalse)
        if any(MovablePos[:, :]):
            return False

        # ゲームが終了しているときはパスできない
        if isGameOver():
            return False

        # ここまで来たらパスなので手番を変える
        self.CurrentColor = - self.CurrentColor

        # MovablePosとMovableDirの更新
        self.initMovable()

        return True

    """
    オセロ盤面の表示
    """

    def display(self):

        # 横軸
        print(' a b c d e f g h')
        # 縦軸方向へのマスのループ
        for y in range(1, 9):

            # 縦軸
            print(y, end="")
            # 横軸方向へのマスのループ
            for x in range(1, 9):

                # マスの種類(数値)をgridに代入
                grid = self.RawBoard[x, y]

                # マスの種類によって表示を変化
                if grid == EMPTY:  # 空きマス
                    print('□', end="")
                elif grid == WHITE:  # 白石
                    print('●', end="")
                elif grid == BLACK:  # 黒石
                    print('〇', end="")

            # 最後に改行
            print()

    """
    入力された手の形式をチェック
    """
    
    def put_disc(self, color,  *move):
        self.prev_RawBoard = self.RawBoard
        board = self.get_flippable_discs(color, move[0], move[1])
        return board
    
    def undo(self):
        self.RawBoard = self.prev_RawBoard
    
    def get_score(self, color):
        score = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.RawBoard[x][y] == color:
                    score += 1
        return score
    
    def get_flippable_discs(self, color, move_x, move_y):
        return self.flipDiscs(color, move_x, move_y)

    def checkIN(self, IN):

        # INが空でないかをチェック
        if not IN:
            return False

        # INの1文字目と2文字目がそれぞれa~h,1~8の範囲内であるかをチェック
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True

        return False
    
    def get_board_info(self):
        """get_board_info
        """
        board_info = []
        for row in self.RawBoard:
            tmp = []
            for col in row:
                if col == BLACK:
                    tmp += [1]
                elif col == WHITE:
                    tmp += [-1]
                elif col == 0:
                    tmp += [0]
            if len(tmp) != 0:
                board_info += [tmp]
        return board_info
    
    def get_bit_count(self, bits):
        """get_bit_count
        """
        count = 0
        size = self.size
        mask = 1 << ((size**2)-1)
        for _ in range(size**2):
            if bits & mask:
                count += 1
            mask >>= 1

        return count