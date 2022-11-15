const stage = document.getElementById("stage");
const squareTemplate = document.getElementById("square-template");
//追加
let stoneStateList = [];

const onClickSquare = (index) => {
  console.log(index);
};

const createSquares = () => {
    for (let i = 0; i < 64; i++) {
        const square = squareTemplate.cloneNode(true);//テンプレートから要素をクローン
        square.setAttribute('id',`square-${i}`); //テンプレート用のid属性を削除
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
        stoneStateList.push(defaultState); //初期値を配列に格納
        square.addEventListener("click", () => {
            onClickSquare(i);
        });

        stage.appendChild(square); //マス目のHTML要素を盤に追加
    }
};

const createSquares2 = (board) => {
    stoneStateList = [];
    console.log(board.length)
    let i = 0;
    if(Player == 'black'){
        Player = 'white'
    }else{
        Player = 'black'
    }
    for (let x = 0; x < 8; x++) {
        for(let y = 0; y <8; y ++){
            let defaultState;
            if(board[x][y] == 1){
                defaultState = 1;
                const square = document.getElementById(`square-${i}`);
                const stone = square.querySelector(".stone");
                stone.setAttribute("data-state", 1);
                stone.setAttribute("data-index", i);
            }else if(board[x][y] == -1){
                defaultState = -1;
                const square = document.getElementById(`square-${i}`);
                const stone = square.querySelector(".stone");
                stone.setAttribute("data-state", -1);
                stone.setAttribute("data-index", i);
            }else{
                defaultState = 0;
            }
            stoneStateList.push(defaultState);
            i++
        }
    }
};

window.onload = () => {
  createSquares();
};

let Player = 'black'

function getElements() {
  let User1 = document.getElementsByName("User1");
  let User2 = document.getElementsByName("User2");
  let len = User1.length;
  _val = User1[0].options[User1[0].selectedIndex].value;
  board = [];
  for (let i = 0; i < 64; i++) {
    let a = document
      .querySelector(`[data-index='${i}']`)
      .getAttribute("data-state");
    board.push(a);
  }
  const userId = "js-primer-example";
  fetch(
    `https://7oe9q5o7cc.execute-api.ap-northeast-1.amazonaws.com/test/xxx?now_user_color=${Player}&now_user_strategy=${_val}&board=[${board}]`
  ).then((response) => {
    console.log(response.status); // => 200
    return response.json().then((boardInfo) => {
      // JSONパースされたオブジェクトが渡される
      console.log(boardInfo["flip_point"]); // => {...}
      console.log(boardInfo["next_board"]);
      console.log(boardInfo["next_player"]);
      createSquares2(boardInfo["next_board"]);
    });
  });
}
