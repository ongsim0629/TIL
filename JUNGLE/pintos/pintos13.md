# Stack growth
기존의 스택 : USER_STACK을 시작으로 하는 단일 페이지고, 크기가 제한되어 있었다.
stack growth를 통해서 stack이 현재 크기를 초과하면 추가 페이지를 할당할 수 있도록 한다.

스택 또한 페이지 (anonymous page)이다. 따라서 유저 프로그램에서 함수가 호출되면 그 리턴 값이 차곡차곡 쌓이게 되고
이 쌓이는 과정은 스택 페이지에 접근해서 해당 내용을 작성하는 것이다. (rsp가 내려오면서 해당 위치에 정보를 적재한다.)
근데 할당해준 영영 밑으로 rsp가 접근하면 page fault가 발생한다. -> 이때 stack growth가 필요하다.

이때 최대 스택 크기는 1MB로 제한하고, rsp보다 높은 주소 값에 접근한 경우만 stack growth로 해결한다.
-> stack growth로 해결할 지 말지는 rsp를 보고 판단한다.

rsp멤버가 유저 스택을 가리키고 있다면 그냥 스택 포인터를 사용하면 된다.
근데 커널 스택을 가리키고 있다면 thread에 rsp를 저장해야한다.
(intr_frame안의 rsp는 f-> rsp로 접근할 수 있다.)

또한 페이지 폴트의 발생 주소가 유저 스택 내인지에 대해서도 확인이 필요하다.
