process 관련 핸들러: halt, exit, exec, wait
file 관련 핸들러: create, remove, open, filesize, read, write, seek, tell, close

시스템콜은 커널 모드에서 실행된다.

syscall3() -> 인자 3개 의미한다.

파라미터 리스트의 포인터들의 검증이 필요하다.
-> 커널 구역에 있으면 안되고 유저 구역에 있어야한다.
-> 유효한 지역을 가리키지 않으면 이것은 페이지 폴트

유효하다면 -> 인자를 유저 스택에서 커널로 복사한다.
시스템 콜의 값을 eax 레지스터에 저장한다.

유효하지 않은 포인터
-> 널 포인터, 커널 구역의 포인터 (PHYS_BASE 보다 큰 값), 가상메모리에 매핑되지 않은 포인터)

malloc 이나 lock 등을 사용하고 페이지 폴트가 발생했을 때 unlock 이나 free를 꼭 해줘서
resource가 새어나가는 것을 방지해야한다.

wait -> while(1)
sema를 쓰기
