const stage = document.getElementById("stage");
const squareTemplate = document.getElementById("square-template");
//追加
const stoneStateList = [];

const onClickSquare = (index) => {
  console.log(index);
};

const createSquares = () => {
  for (let i = 0; i < 64; i++) {
    const square = squareTemplate.cloneNode(true); //テンプレートから要素をクローン
    square.removeAttribute("id"); //テンプレート用のid属性を削除
    stage.appendChild(square); //マス目のHTML要素を盤に追加

    const stone = square.querySelector(".stone");

    //ここから編集
    let defaultState;
    //iの値によってデフォルトの石の状態を分岐する
    if (i == 27 || i == 36) {
      defaultState = 1;
    } else if (i == 28 || i == 35) {
      defaultState = -1;
    } else {
      defaultState = 0;
    }

    stone.setAttribute("data-state", defaultState);

    stone.setAttribute("data-index", i); //インデックス番号をHTML要素に保持させる
    stoneStateList.push(defaultState); //初期値を配列に格納
    square.addEventListener("click", () => {
      onClickSquare(i);
    });
  }
};

window.onload = () => {
  createSquares();
};

function getElements() {
  let User1 = document.getElementsByName("User1");
  let User2 = document.getElementsByName("User2");
  let len = User1.length;
  for (let i = 0; i < len; i++) {
    if (User1.item(i).checked) {
      console.log(User1.item(i).value + " is checked");
    } else {
      console.log(User1.item(i).value + " is not checked");
    }
  }
  board = [];
  for (let i = 0; i < 64; i++) {
    let a = document
      .querySelector(`[data-index='${i}']`)
      .getAttribute("data-state");
    board.push(a);
  }
  const userId = "js-primer-example";
  fetch(`https://api.github.com/users/${encodeURIComponent(userId)}`).then(
    (response) => {
      console.log(response.status); // => 200
      return response.json().then((userInfo) => {
        // JSONパースされたオブジェクトが渡される
        console.log(userInfo); // => {...}
      });
    }
  );
}
