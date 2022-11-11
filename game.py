from reversi import Reversi
from reversi.strategies import Random, Greedy, AlphaBeta
from player import CornerPlayer, GreedyPlayer, EdgePlayer,MiniMaxPlayer
from reversi.strategies.coordinator import Evaluator
 
if __name__ == '__main__':
    Reversi(
        {
            #add player
            'RANDOM': Random(),
            'GREEDY': GreedyPlayer(),
            'Corner': CornerPlayer(),
            'MINMAX': MiniMaxPlayer(depth = 3),
            'Edge' : EdgePlayer(),
        }
    ).start()
 
