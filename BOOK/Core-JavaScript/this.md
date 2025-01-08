# JavaScript에서의 `this`

## 1. 다른 객체 지향 언어에서의 `this`

- 클래스 기반 언어에서는 `this`는 **클래스로 생성된 인스턴스 객체**를 가리킵니다.

## 2. JavaScript에서의 `this`

- JavaScript에서는 **함수를 호출하는 방식에 따라** `this`가 결정됩니다.
- `this`는 코드 어디에서든 사용할 수 있습니다.

---

## 3. 전역 공간에서의 `this`

- **전역 객체**를 가리킵니다.
    - 브라우저 환경: `window`
    - Node.js 환경: `global`

### 전역 변수와 전역 객체의 관계

- 전역 변수를 선언하면 자바스크립트 엔진은 이를 **전역 객체의 프로퍼티**로도 할당합니다.

### 예시:

```
var a = 1;
console.log(a);          // 1
console.log(window.a);   // 1 (브라우저 환경)
console.log(this.a);     // 1
```

- **전역 변수 선언과 전역 객체 프로퍼티의 차이**:
    - 전역 변수는 `configurable: false`로 설정됩니다.

### 예시:

```
var a = 1;
window.b = 2;
delete window.a; // false
delete window.b; // true
```

- **원인**: 전역 변수는 자바스크립트 엔진이 전역 객체의 프로퍼티로 추가하면서 `configurable` 속성을 `false`로 설정해 삭제를 방지합니다.

---

## 4. 메서드로서 호출할 때의 `this`

- **함수와 메서드의 차이**:
    - **함수**: 독립적으로 동작.
    - **메서드**: 자신을 호출한 **객체에 대한 동작**을 수행.

### 예시:

```
var func = function (x) {
    console.log(this, x);
};
func(1); // `this`는 전역 객체 (window, global)

var obj = {
    method: func,
};
obj.method(2); // `this`는 obj
```

- **`this`의 값**: 메서드를 호출한 **객체** (마지막 점 앞의 객체)가 `this`입니다.

---

## 5. 함수로서 호출할 때의 `this`

- **독립적으로 호출된 함수**의 `this`는 기본적으로 **전역 객체**를 참조합니다.

### 메서드 내부 함수에서의 `this`

- 내부 함수의 `this`는 호출 주체가 없으므로 기본적으로 전역 객체를 참조합니다.

### 우회 방법:

1. **상위 스코프의 `this`를 저장**:

```
var obj = {
    method: function () {
        var self = this; // `this`를 저장
        function innerFunc() {
            console.log(self); // obj
        }
        innerFunc();
    },
};
obj.method();
```

1. **ES6 화살표 함수 사용**:
- 화살표 함수는 `this`를 바인딩하지 않고 상위 스코프의 `this`를 상속받습니다.

```
var obj = {
    method: function () {
        const innerFunc = () => {
            console.log(this); // obj
        };
        innerFunc();
    },
};
obj.method();
```

---

## 6. 콜백 함수 호출 시의 `this`

- 콜백 함수의 `this`는 **제어권을 넘겨받은 함수의 내부 로직**에 따라 결정됩니다.

### 예시:

```
setTimeout(function () {
    console.log(this); // 전역 객체 (window, global)
}, 300);

[1, 2, 3].forEach(function (x) {
    console.log(this, x); // 전역 객체, 1, 2, 3
});

var obj = {
    value: 42,
};
[1, 2, 3].forEach(function (x) {
    console.log(this.value, x);
}, obj); // 42, 1, 42, 2, 42, 3
```

---

## 7. 생성자 함수에서의 `this`

- **생성자 함수**: 객체 인스턴스를 생성하는 데 사용하는 함수.
- `new` 키워드로 호출하면, 생성자 함수 내부의 `this`는 **새로 생성된 객체 인스턴스**를 가리킵니다.

### 예시:

```
function Person(name) {
    this.name = name;
}
var person = new Person("Alice");
console.log(person.name); // Alice
```

---

## 8. 명시적으로 `this`를 바인딩하는 방법

### 1. `call` 메서드

- `Function.prototype.call(thisArg, arg1, arg2, ...)`
- `call` 메서드는 함수 호출 시 첫 번째 인자를 `this`로 명시적으로 설정합니다.

### 예시:

```
function greet(greeting) {
    console.log(greeting + ", " + this.name);
}
var user = { name: "Alice" };
greet.call(user, "Hello"); // Hello, Alice
```

---

### 2. `apply` 메서드

- `Function.prototype.apply(thisArg, [argsArray])`
- `apply`는 `call`과 비슷하지만 인자를 **배열로 전달**합니다.

### 예시:

```
function greet(greeting, punctuation) {
    console.log(greeting + ", " + this.name + punctuation);
}
var user = { name: "Alice" };
greet.apply(user, ["Hello", "!"]); // Hello, Alice!
```

---

### 3. `bind` 메서드

- `Function.prototype.bind(thisArg, ...args)`
- `bind`는 새로운 함수를 반환하며, `this`와 초기 인수를 미리 설정합니다.

### 예시:

```
function greet(greeting) {
    console.log(greeting + ", " + this.name);
}
var user = { name: "Alice" };
var boundGreet = greet.bind(user, "Hi");
boundGreet(); // Hi, Alice
```

- `bind`를 사용하면 `this`를 사전에 고정할 수 있어 편리합니다.

---

## 요약

- **`this`의 결정**:
    - **전역 공간**: 전역 객체 (`window`, `global`).
    - **메서드 호출**: 메서드를 호출한 객체.
    - **함수 호출**: 기본적으로 전역 객체.
    - **생성자 함수 호출**: 새로 생성된 객체 인스턴스.
    - **화살표 함수**: 상위 스코프의 `this`를 상속.
- **명시적 바인딩**:
    - `call`, `apply`, `bind`를 사용해 `this`를 명시적으로 설정할 수 있음.
