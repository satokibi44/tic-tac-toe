const stage = document.getElementById("stage");
const squareTemplate = document.getElementById("square-template");
//追加
let stoneStateList = [];

const onClickSquare = (i) => {
  const square = document.getElementById(`square-${i}`);
  const stone = square.querySelector(".stone");
  const color = stone.getAttribute("data-state");
  if (color == 0) {
    callHumanAPI(i);
    asynccall();
  }
};

async function asynccall(){
    await resolveAfter2Seconds();
}

function resolveAfter2Seconds() {
    return new Promise(resolve => {
      setTimeout(() => {
        callAiAPI();
      }, 2000);
    });
  }

const callAiAPI = () => {
  board = [];
  for (let y = 0; y < 8; y++) {
    for (let x = 0; x < 8; x++) {
      board.push(boardXY[y][x]);
    }
  }
  fetch(
    `https://7oe9q5o7cc.execute-api.ap-northeast-1.amazonaws.com/test/xxx?now_user_color=black&now_user_strategy=${User}&board=[${board}]`
  ).then((response) => {
    console.log(response.status); // => 200
    return response.json().then((boardInfo) => {
      boardXY = boardInfo["next_board"];
      updateSquares(boardInfo["next_board"]);
    });
  });
}

function sleep(waitMsec) {
  var startMsec = new Date();

  // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
  while (new Date() - startMsec < waitMsec);
}

const callHumanAPI = (index) => {
  board = [];
  console.log(boardXY);
  for (let y = 0; y < 8; y++) {
    for (let x = 0; x < 8; x++) {
      board.push(boardXY[y][x]);
    }
  }
  index_x = Math.floor((index + 1) / 8);
  index_y = ((index + 1) % 8) - 1;
  fetch(
    `https://7oe9q5o7cc.execute-api.ap-northeast-1.amazonaws.com/test/xxx?now_user_color=white&now_user_strategy=human&board=[${board}]&flip_point=[${index_x},${index_y}]`
  ).then((response) => {
    console.log(response.status); // => 200
    return response.json().then((boardInfo) => {
      // JSONパースされたオブジェクトが渡される
      console.log(boardInfo["next_player"]);
      boardXY = boardInfo["next_board"];
      if (boardInfo["next_player"] == 1) {
        updateSquares(boardInfo["next_board"]);
      }
    });
  });
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
    stoneStateList.push(defaultState); //初期値を配列に格納
    square.addEventListener("click", () => {
      onClickSquare(i);
    });

    stage.appendChild(square); //マス目のHTML要素を盤に追加
  }
};
const updateSquares = (board) => {
  stoneStateList = [];
  let i = 0;
  if (Player == "black") {
    Player = "white";
  } else {
    Player = "black";
  }
  for (let x = 0; x < 8; x++) {
    for (let y = 0; y < 8; y++) {
      let defaultState;
      if (board[x][y] == 1) {
        defaultState = 1;
        const square = document.getElementById(`square-${i}`);
        const stone = square.querySelector(".stone");
        stone.setAttribute("data-state", 1);
        stone.setAttribute("data-index", i);
      } else if (board[x][y] == -1) {
        defaultState = -1;
        const square = document.getElementById(`square-${i}`);
        const stone = square.querySelector(".stone");
        stone.setAttribute("data-state", -1);
        stone.setAttribute("data-index", i);
      } else {
        defaultState = 0;
      }
      stoneStateList.push(defaultState);
      i++;
    }
  }
};

window.onload = () => {
  createSquares();
};

function delete_select() {
  var select = document.getElementById("select_user1");
  select.remove();
  var select = document.getElementById("select_user2");
  select.remove();
}

let Player = "black";
let User = "GREEDY";
let boardXY = [];
function getElements() {
  User = document.getElementsByName("User1");
  User = User[0].options[User[0].selectedIndex].value;
  board = [];
  for (let i = 0; i < 64; i++) {
    let a = document
      .querySelector(`[data-index='${i}']`)
      .getAttribute("data-state");
    board.push(a);
  }
  const userId = "js-primer-example";
  fetch(
    `https://7oe9q5o7cc.execute-api.ap-northeast-1.amazonaws.com/test/xxx?now_user_color=${Player}&now_user_strategy=${User}&board=[${board}]`
  ).then((response) => {
    console.log(response.status); // => 200
    return response.json().then((boardInfo) => {
      boardXY = boardInfo["next_board"];
      if (boardInfo["next_player"] == -1) {
        updateSquares(boardInfo["next_board"]);
      }
      delete_select();
    });
  });
}
