export class playerState{
    color = 1;
    setState(color, strategy){
        this.strategy = strategy
    }

}

export class boardState{
    ch2d(board){
        let boardXY = []
        let index = 0
        for(let y = 0; y<7; y++){
            let boardX = []
            for(let x = 0; x<7; x++){
                boardX.push(board[index])
                index ++
            }
            boardXY.push(boardX)
        }
        return boardXY
    }

    ch1d(boardXY){
        for (let y = 0; y < 8; y++) {
            for (let x = 0; x < 8; x++) {
              board.push(boardXY[y][x]);
            }
        }
        return board
    }

    setState(board){
        this.board = board
        this.boardXY = this.ch2d(board)
    }
    update1dState(boardXY){
        this.boardXY = boardXY
        this.board = this.ch1d(boardXY)
    }
}