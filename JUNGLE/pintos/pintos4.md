# 유집좌 영상 정리

시스템 콜 구현
system call handler 테이블을 채우는 것

# 시스템 콜
커널 모드에서 실행되는 것이고, 그 결과를 사용자 모드에 반환한다.

syscall 다음의 숫자 : 인자의 개수를 의미한다.

syscall_handler() 완전 비어있음

먼저 시스템 콜 넘버로 
valid 하지 않은 주소 : 페이지 폴트

# PML4
Page Map Level 4라는 의미로 x86-64 아키텍쳐에서 사용하는 4단계 페이징의 최상위 레벨 페이지 테이블이다. 이는 가상 주소를 물리 주소로 변환하기 위한 과정의 일부인데

4단계 페이징은 PML4-PDPT-PD-PT의 순서로 이루어져있다.

즉, 64비트의 가상 주소의 상위 9비트는 PML4 테이블의 인덱스로 사용되고 해당 인덱스에 저장된 값이 PDPT의 주소를 가리킨다. PDPT에서 그 다음 9비트로 PDPT엔트리를 찾고 그 다음 9비트를 사용해서 PD 엔트리를 찾는다 -> 이 과정을 계속 반복하다가 PT에서 마지막 9비트를 사용해서 페이지 테이블 엔트리를 찾는다. 이 페이지 테이블 엔트리는 실제 물리 주소를 가리키며 마지막 12비트는 페이지 내부 오프셋을 가리킨다. 이 과정을 통해서 가상 주소가 물리 주소로 변환된다.
