// input 처리 - [[색종이 개수], [x,y], [x,y] ... ]
const input = require('fs').readFileSync(process.platform === "linux" ? "/dev/stdin" : "./example.txt").toString().trim().split("\n").map((el) => el.split(" ").map(Number));
// n = 색종이 개수 (3);
let n = input[0][0];
// list = [[3,7], [15,7], [5,2]]
let list = [];
for(let i = 1; i<input.length; i++){
    list.push(input[i]);
}

// 크기 100*100인 종이
let paper =  Array.from(Array(100), () => new Array(100));

// 색종이 놓여있는 좌표면 1로 바꿔주고
for(let value = 0; value <list.length; value++){
    for(let x = list[value][0]; x < list[value][0]+10; x++){
        for(let y = list[value][1]; y < list[value][1]+10; y++){
            paper[x][y] = 1;
        }
    }
}

// paper[x][y]가 1인 부분 -> 색종이가 놓여있는 부분 -> 크기 계산
let answer = 0;
for(let i = 0; i < 100; i++){
    for(let j = 0; j < 100; j++){
        if (paper[i][j]==1){
            answer++;
        }
    }
}

console.log(answer)
