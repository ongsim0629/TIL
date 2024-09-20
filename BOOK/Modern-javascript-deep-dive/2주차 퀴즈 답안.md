# OX 문제
#### 1. <code>x = 10;</code> 은 표현식이다. ( ) -> 5장
<details>
   <summary>답</summary>
   <div markdown="1">
      O, 할당문은 그 자체가 표현식이지만 완전한 문이기도 하다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      <code>let x = 10;</code> 은 표현식이다 ( ) 
      <details>
         <summary>답</summary>
            <div markdown="1">
               X, 변수 선언문은 표현식이 아닌 문이다.
            </div>
      </details>
   </div>
</details>

#### 2. 
```
x = 'Hello';
console.log(+x)
```
의 결과는 nan이다. ( ) -> 7장 + 6장
<details>
   <summary>답</summary>
   <div markdown="1">
      X, 문자열을 숫자로 타입 변환할 수 없으므로 NaN을 반환한다. (JS는 대소문자를 구분한다.)
   </div>
</details>

#### 3. ++ 연산자와 -- 연산자는 부수효과가 있다. ( ) -> 7장
<details>
   <summary>답</summary>
   <div markdown="1">
      O, 증가/감소 연산자는 피연산자의 값을 변경하는 부수 효과가 있다
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
     + 연산자와 - 연산자는 부수효과가 있다.
      <details>
         <summary>답</summary>
            <div markdown="1">
               X, 피연산자를 변경하는 것이 아니고 숫자타입으로 변환한 값을 생성해서 반환한다.
            </div>
      </details>
   </div>
</details>

#### 4. 암묵적 타입 변환은 기존 변수의 값을 재할당하는 것이다 ( ) -> 9장
<details>
   <summary>답</summary>
   <div markdown="1">
      X, 표현식을 에러없이 평가하기 위해 피연산자의 값을 암묵적 타입 변환해 새로운 타입의 값을 만들어 단 한 번 사용하고 버린다.
   </div>
</details>

#### 5. 출력되는 결과는 두 개 모두 동일하다 ( ) -> 10장
```
var person = {
   name : 'Lee';
};

console.log(person[name]);
console.log(person.age);
```
<details>
   <summary>답</summary>
   <div markdown="1">
      X, 첫번째 -> ReferenceError : 대괄호 연산자 내에 따옴표로 감싸지 않으면 식별자로 해석한다. 두번째 -> undefined : 객체에 존재하지 않는 프로퍼티에 접근하면 undefined를 반환한다
   </div>
</details>

#### 6. 일반 객체를 호출할 수 있다. ( ) -> 12장
<details>
   <summary>답</summary>
   <div markdown="1">
      X, 호출할 수 없다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
    함수는 호출할 수 있다. 그렇다면 함수는 객체가 아닐 것이다. ()
      <details>
         <summary>답</summary>
            <div markdown="1">
               X, 함수는 객체지만 일반 객체와는 다르다. 함수가 객체라는 사실은 자바스크립트의 중요한 특징이다.
            </div>
      </details>
   </div>
</details>

#### 7. 변수는 어떤 경우에도 같은 스코프 내에서 중복 선언할 수 없다. ( ) -> 13장
<details>
   <summary>답</summary>
   <div markdown="1">
      X, var 키워드로 선언된 변수는 같은 스코프 내에서 중복 선언이 가능하다.
   </div>
</details>


# 단답형
#### 1. <code>console.log(7 === 7.0)</code> 의 결과를 말하시오. -> 6장
<details>
   <summary>답</summary>
   <div markdown="1">
       true, js에서 숫자 타입은 모두 실수로 처리된다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      <code>console.log(0.1 + 0.2 === 0.3);</code> 의 결과를 말하시오.
      <details>
         <summary>답</summary>
            <div markdown="1">
               false, 0.30000000000000004로 js의 부동소수점 연산은 정확하지 않다.
            </div>
      </details>
   </div>
</details>

#### 2. typeof 연산자로 null 값을 연산해보면 어떤 값을 반환하나요? -> 7장
<details>
   <summary>답</summary>
   <div markdown="1">
       object를 반환한다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      그렇다면 값이 null 타입인지 확인할 때는 typeof 연산자 대신 어떤 연산자를 사용하는 것이 좋을까요?
      <details>
         <summary>답</summary>
            <div markdown="1">
               === : 일치 연산자
            </div>
      </details>
   </div>
</details>

#### 3. for문의 변수 선언문, 조건식, 증감식 모두 옵션입니다. 어떤 식도 선언하지 않으면 어떻게 될까요? -> 8장
<details>
   <summary>답</summary>
   <div markdown="1">
       무한루프
   </div>
</details>

#### 4. 결과를 예상하세요.
```
var elem = null;
var value = elem?.value;
console.log(value);
```
<details>
   <summary>답</summary>
   <div markdown="1">
      undefined -> ?. 좌측의 값이 null 또는 undefined일때 undefined를 반환한다.
   </div>
</details>

#### 5. 결과를 예상하세요. -> 11장
```
var name = 'sujin';

name[2] = 'b';
console.log(name);
```
<details>
   <summary>답</summary>
   <div markdown="1">
      suujin, 문자열은 원시값이므로 불변한다.
   </div>
</details>

#### 6. 결과를 예상하세요. -> 11장
```
var person1 = {
   name : 'Lee';
};

var person2 = {
   name : 'Lee';
};

console.log(person1 === person2);
console.log(person1.name === person2.name);
```
<details>
   <summary>답</summary>
   <div markdown="1">
      false,참조 값이 다르므로
      true, 값으로 평가될 수 있으므로
   </div>
</details>

#### 7. 순수함수와 비순수함수를 구분해보세요. -> 12장
```
// 함수 A
let counter = 0;
function incrementCounter() {
  counter++;
  return counter;
}

// 함수 B
function add(a, b) {
  return a + b;
}
```
<details>
   <summary>답</summary>
   <div markdown="1">
       A는 비순수, B는 순수
   </div>
</details>

#### 8. 결과를 예상하세요. -> 13장
```
var x = 1;
function test() {
  if (true) {
    var x = 10;
  }
  console.log(x);
}

test();
```
<details>
   <summary>답</summary>
   <div markdown="1">
      10 출력, var 은 함수 레벨 스코프를  따라서 함수에서만 지역스코프다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      그렇다면 var을 let으로 바꾸면 어떻게 될까요?
      <details>
         <summary>답</summary>
            <div markdown="1">
               1, let은 블록 레벨 스코프여서
            </div>
      </details>
   </div>
</details>

# 빈칸 채우기
#### 1. 동적 타입 언어는 변수를 선언할 때 ( )을 선언하지 않는다. 자바스크립트의 변수는 선언이 아닌 ( )에 의해 타입이 결정된다. ( )에 의해 변수의 타입은 언제든지 동적으로 변할 수 있다. -> 6장
<details>
   <summary>답</summary>
   <div markdown="1">
       타입, 할당, 재할당 
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      변수는 타입을 가질까? => ( )는 타입을 갖지 않는다. 하지만 ( )은 타입을 갖는다.
      <details>
         <summary>답</summary>
            <div markdown="1">
               변수, 값
            </div>
      </details>
   </div>
</details>

#### 2. () 연산자를 사용하면 객체의 프로퍼티를 삭제할 수 있으며, 존재하지 않는 프로퍼티를 삭제해도 ()가 발생하지 않는다. -> 10장
<details>
   <summary>답</summary>
   <div markdown="1">
       delete, 에러
   </div>
</details>


#### 3. 식별자가 기억하는 것은 값이 아니라 () 이다. 따라서 식별자는 ()에 붙인 이름이라고 할 수 있다. -> 11장
<details>
   <summary>답</summary>
   <div markdown="1">
  메모리 주소
   </div>
</details>


# 서술형
#### 1. + 연산자가 문자열 연결 연산자로 동작하기 위한 조건을 설명하세요. -> 6장
<details>
   <summary>답</summary>
  피연산자 중 하나 이상이 문자열인 경우에는 + 연산자가 문자열 연결 연산자로 동작한다.
</details>

#### 2. 동등 비교 연산자와 일치 비교 연산자의 차이를 설명하세요 -> 7장
<details>
   <summary>답</summary>
  동등 비교 연산자는 좌항과 우항의 피연산자를 비교할 때 먼저 암묵적 타입 변환을 통해 타입을 일치시킨 후 같은 값인지 비교한다. 
</details>

#### 3. 식별자 네이밍 규칙을 준수하는 프로퍼티 키와 그렇지 않은 프로퍼티 키의 차이를 설명하세요 -> 10장
<details>
   <summary>답</summary>
  식별자 네이밍 규칙을 따르지 않는 이름에는 반드시 따옴표를 사용해야한다. 대괄호 표기법만 사용가능하다.
   네이밍 규칙을 따르는 이름은 마침표 표기법과 대괄호 표기법을 모두 사용할 수 있다.
</details>


#### 4. 결과를 예상하세요 -> 12장
```
console.log(myFunction);

var myFunction = function() {
  console.log("Hello, World!");
};

myFunction();
```
<details>
   <summary>답</summary>
  undefined, 함수 표현식으로 정의되어 있어서 호이스팅은 일어났지만 함수의 값은 할당 되지 않았다.
   Hello, world, 표현식이 실행된 후에 함수가 할당되어서
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      함수 표현식과 선언문의 차이를 설명하세
      <details>
         <summary>답</summary>
            <div markdown="1">
               함수 선언문은 선언과 동시에 정의가 이루어져, 코드의 어디서든 호출할 수 있다. 반면 함수 표현식은 할당된 시점 이후에만 사용할 수 있다.
            </div>
      </details>
   </div>
</details>

#### 5. 매개변수보다 인수가 부족할 때, 매개변수보다 인수가 초과됐을 때의 결과를 설명하세요 -> 12장
<details>
   <summary>답</summary>
  부족한 경우 : undefined, 초과한 경우 (arguments 객체의 프로퍼티로 보관)
</details>

#### 6. 자바스크립트는 동적 타입 언어이기 때문에 함수의 매개변수 타입을 사전에 지정할 수 없습니다. 이로 인해서 함수 내부에 적절한 인수가 전달되었는지를 사전에 방지할 수 없고 에러가 런타임에 발생하게 되는데요 이를 방지하기 위한 방법을 말해보세요 -> 12장
<details>
   <summary>답</summary>
  타입스크립트를 사용한다 (정적 타입 선언 가능) -> 컴파일 시점에 부적절한 호출 방지, arguments객체 확인, 매개변수 기본값 사용 (ES6), 인수 전달 안된 경우에는 단축평가사용하기
</details>


# 객관식
#### 1. 올바른 결과의 번호를 고르세요 -> 9장
```
console.log(null + 1);
```
① 1 <br>
② null1 <br>
③ NaN <br>
④ undefined <br>
<details>
   <summary>답</summary>
   <div markdown="1">
       ① null은 암묵적으로 숫자 0으로 변환된다. 따라서 0 + 1이 되어 결과는 1이다.
   </div>
</details>

<details>
   <summary> 꼬리 질문 </summary>
   <div markdown="1">
      <code> console.log(true + false); </code> <br>
      ① 1 <br>
      ② true <br>
      ③ NaN <br>
      ④ truefalse <br>
      <details>
         <summary>답</summary>
            <div markdown="1">
               자바스크립트에서 true는 숫자 1로, false는 숫자 0으로 암묵적으로 변환된ㄷ다. 따라서 1 + 0이 되어 결과는 1이다.
            </div>
      </details>
   </div>
</details>

#### 2. 올바른 출력 결과를 고르세요 -> 9장
```
let user = null;
let defaultUser = "Guest";

let username = user || defaultUser;
console.log(username);
```
① null <br>
② "null" <br>
③ "Guest" <br>
④ "user" <br>
<details>
   <summary>답</summary>
   <div markdown="1">
      3. 단축평가 || 연산자는 좌항이 fasly일 경우 우항의 값을 반환한다.
   </div>
</details>


#### 3. 결과를 예상하세요 -> 12장
```
(function myFunction() {
    console.log("Hello!");
})();

myFunction();
```
① "Hello!"가 두 번 출력된다. <br>
② "Hello!"가 한 번 출력되고, 에러가 발생하지 않는다. <br>
③ "Hello!"가 한 번 출력되고, 에러가 발생한다. <br>
④ 에러가 발생하여 아무것도 출력되지 않는다. <br>
<details>
   <summary>답</summary>
   <div markdown="1">
      3. 즉시 실행 함수는 선언과 동시에 실행되고, myFunction은 함수 이름으로 함수 내부에서만 접근 가능해서 reference오류가 발생한다.
   </div>
</details>

