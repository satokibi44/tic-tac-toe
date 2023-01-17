const stage = document.getElementById("stage");
const squareTemplate = document.getElementById("square-template");

const apiUrl = "https://dxscjo6mrh.execute-api.ap-northeast-1.amazonaws.com/test"

class CallApi{
    async callAiApi(playerState, boardState){
        const response = await fetch(`${apiUrl}?now_user_color=black&now_user_strategy=${playerState.strategy}&board=[${boardState.board}]`);
        const jsondata = await response.json();
        const next_board = jsondata['next_board'];
        const next_player = jsondata['next_player'];
        boardState.update1dState(next_board);
        updateSquares(boardState.board);
        playerState.updateState(next_player);
    }
    
    async callHumanApi(playerState, boardState, index){
        const index_x = Math.floor(index / 8);
        const index_y = index % 8;
        const response = await fetch(`${apiUrl}?now_user_color=white&now_user_strategy=human&board=[${boardState.board}]&flip_point=[${index_x},${index_y}]`);
        const jsondata = await response.json();
        const next_board = jsondata['next_board'];
        const next_player = jsondata['next_player'];
        console.log(next_player)

        if (next_player == 1) {
            boardState.update1dState(next_board);
            updateSquares(boardState.board);
            playerState.updateState(next_player);
            asynccall();
          }
    }
}

class PlayerState{
    color = 1;
    setState(color, strategy){
        this.strategy = strategy;
    }
    updateState(color){
        this.color = color;
    }
}

class BoardState{
    ch2d(board){
        let boardXY = [];
        let index = 0;
        for(let y = 0; y<7; y++){
            let boardX = [];
            for(let x = 0; x<7; x++){
                boardX.push(board[index]);
                index++;
            }
            boardXY.push(boardX);
        }
        return boardXY
    }

    ch1d(boardXY){
        const board = []
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
        console.log(this.boardXY)
        this.board = this.ch1d(boardXY)
    }
}

const onClickSquare = (i) => {
  const square = document.getElementById(`square-${i}`);
  const stone = square.querySelector(".stone");
  const color = stone.getAttribute("data-state");
  if (color == 0 && playerState.color == -1) {
    callApi.callHumanApi(playerState, boardState, i)
  }
};

async function asynccall(){
    await resolveAfter2Seconds();
}

function resolveAfter2Seconds() {
    return new Promise(resolve => {
      setTimeout(() => {
        callApi.callAiApi(playerState, boardState);
      }, 2000);
    });
  }

function sleep(waitMsec) {
  var startMsec = new Date();

  // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
  while (new Date() - startMsec < waitMsec);
}

const callHumanAPI = (index) => {
  callApi.callHumanApi(playerState, boardState, index)
}

const createSquares = () => {
  for (let i = 0; i < 64; i++) {
    const square = squareTemplate.cloneNode(true); //テンプレートから要素をクローン
    square.setAttribute("id", `square-${i}`); //テンプレート用のid属性を削除
    const stone = square.querySelector(".stone");

    //ここから編集
    let defaultState;
    //iの値によってデフォルトの石の状態を分岐する
    if (i == 27 || i == 36) {
      defaultState = -1;
    } else if (i == 28 || i == 35) {
      defaultState = 1;
    } else {
      defaultState = 0;
    }

    stone.setAttribute("data-state", defaultState);

    stone.setAttribute("data-index", i); //インデックス番号をHTML要素に保持させる
    square.addEventListener("click", () => {
      onClickSquare(i);
    });

    stage.appendChild(square); //マス目のHTML要素を盤に追加
  }
};
const updateSquares = (board) => {
  for (let i = 0; i <64; i++){
    if(board[i] == 1){
        const square = document.getElementById(`square-${i}`);
        const stone = square.querySelector(".stone");
        stone.setAttribute("data-state", 1);
        stone.setAttribute("data-index", i);
    }else if(board[i] == -1){
        const square = document.getElementById(`square-${i}`);
        const stone = square.querySelector(".stone");
        stone.setAttribute("data-state", -1);
        stone.setAttribute("data-index", i);
    }
  }
};

window.onload = () => {
  createSquares();
};

function delete_select() {
  var select = document.getElementById("select_user1");
  select.remove();
  var select = document.getElementById("button");
  select.remove();
  const passButton = document.createElement('button');
  passButton.innerText = "PASS";
  passButton.id = "pass-button";
  passButton.onclick = function pass(){
    if(playerState.color == -1){
        callApi.callAiApi(playerState, boardState);
    }
};
  document.body.appendChild(passButton);
}

let User = "GREEDY";
let playerState = new PlayerState();
let boardState = new BoardState();
let callApi = new CallApi();

function getElements() {
  User = document.getElementsByName("User1");
  User = User[0].options[User[0].selectedIndex].value;
  delete_select();
  let board = [];
  for (let i = 0; i < 64; i++) {
    let a = document
      .querySelector(`[data-index='${i}']`)
      .getAttribute("data-state");
    board.push(a);
  }
  playerState.setState(1, User);
  boardState.setState(board);
  callApi.callAiApi(playerState, boardState);
}
