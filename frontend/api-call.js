export class CallApi{
    apiUrl = 'https://7oe9q5o7cc.execute-api.ap-northeast-1.amazonaws.com/test/xxx'
    callAiApi(playerState, boardState){
        fetch(
            `${apiUrl}?now_user_color=black&now_user_strategy=${playerState.strategy}&board=[${boardState.board}]`
          ).then((response) => {
            console.log(response.status); // => 200
            return response.json().then((boardInfo) => {
                boardState.update1dState(boardInfo["next_board"]);
            });
          });
          return boardState
    }
    
    callHumanApi(){

    }
}