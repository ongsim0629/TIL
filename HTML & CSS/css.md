<h1>background-position</h1>
백그라운드 이미지의 위치를 설정하는 속성 <br>
<code>keyword</code>와 <code>none-keyword</code> 형태 모두 사용 ok. <br>
<br>
<table>
  <thead>
    <tr>
      <th>키워드</th>
      <th>값</th>
      <th>x,y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>left</td>
      <td>0%</td>
      <td>x</td>
    </tr>
    <tr>
      <td>right</td>
      <td>100%</td>
      <td>x</td>
    </tr>
    <tr>
      <td>top</td>
      <td>0%</td>
      <td>y</td>
    </tr>
    <tr>
      <td>bottom</td>
      <td>100%</td>
      <td>y</td>
    </tr>
    <tr>
      <td>center</td>
      <td>50%</td>
      <td>x,y</td>
    </tr>
  </tbody>
</table>

<h3>keyword: center 를 사용하는 경우</h3>
<code class="language-css">.example {background-position: center;}</code> <br>
이미지를 배경의 정가운데 위치시킴. none-keyword 필요없다.

<h3>4개의 값</h3>
<code class="language-css">.example {background-position: left 100px top 100px;}</code> <br>
1,3 번 째 keyword와 2,4 번 째 none-keyword로 이루어짐. <br>
키워드 x,y가 중복될 경우 속성이 적용되지 않음!! <br>
<code class="language-css">키워드 중복의 예
  .example {background-position: left 100px right 100px;}</code> <br>
</code> 

<h1>background-size</h1>
<h3>cover, contain의 차이</h3>
공통점 : 두 개 다 이미지의 비율을 유지하면서 사이즈를 스케일링한다. <br>
차이점 : <code>contain</code>은 비율을 유지하면서 이미지의 크기 중 크기가 큰 곳 (가로 혹은 세로)을 기준으로 사이즈를 스케일링한다. (이미지 반복되거나, 빈 공간 생길 수 있다)<br><code>cover</code>는 비율을 유지하면서 해당 태그의 사이즈에 꽉 차게 스케일링한다.
