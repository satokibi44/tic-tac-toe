from player2 import CornerPlayer, GreedyPlayer, EdgePlayer, MiniMaxPlayer, Corner1_Edge2_Ungreedy3, Switch

Reversi = {
    # add player
    'GREEDY': GreedyPlayer(),
    'Corner': CornerPlayer(),
    'MINMAX': MiniMaxPlayer(depth=3),
    'Edge': EdgePlayer(),
    'Chimera': Corner1_Edge2_Ungreedy3(), 
    'SWITCH': Switch(      # 戦略切り替え
            turns=[
                29,            # 1～30手目まではRandom              (30手目-1を設定)
                49,            # 21～50手目まではTable              (50手目-1を設定)
                60             # それ以降(残り10手)からはMobteCarlo (最後は60を設定)
            ],
            strategies=[
                CornerPlayer(),      # Random AI
                CornerPlayer(),       # Table AI
                MiniMaxPlayer(depth=3),  # MonteCarlo AI
            ],
        ),}
