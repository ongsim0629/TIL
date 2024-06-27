<h1>ready()</h1>
HTML이 완전히 불러와지면 실행되는 이벤트
<h3>$(document).ready(function(){})</h3>
셀렉터가 document이므로 DOM 객체가 불러와지면 실행된다. -> 익명 함수로 축약해서 사용하기도 한다.<br>
즉, 외부 리소스나 이미지 로딩되기 전에 실행된다. (window.onload 보다 빠름) <br>
사용하는 이유: 눈에 보이는 정보인 HTML을 먼저 처리하고, 눈에 보이지 않는 script를 처리하는 것이 사용자들의 관점에서 더 빠르게 처리된다고 느껴지게 한다.

<h1>attr()</h1>
요소의 속성의 값을 가져오거나 속성을 추가한다.<br> <br>
1. 요소의 속성의 값을 가져온다.<br>
<code>$( 'div' ).attr( 'class' );</code><br>
2. 요소의 속성의 값을 추가하거나 변경한다.<br>
<code>$( 'h1' ).attr( 'title', 'Hello' );</code>
