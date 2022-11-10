from player import CornerPlayer, GreedyPlayer, EdgePlayer, MiniMaxPlayer, Corner1_Edge2_Ungreedy3

Reversi = {
    # add player
    'GREEDY': GreedyPlayer(),
    'Corner': CornerPlayer(),
    'MINMAX': MiniMaxPlayer(depth=3),
    'Edge': EdgePlayer(),
    'Chimera': Corner1_Edge2_Ungreedy3(), }
