# Anonymous Page

anonymous page : file backed 페이지가 아닌 페이지 (파일로 부터 매핑된 페이지가 아니고 커널로부터 할당된페이지)
anonymous 매핑은 백업 파일이나 장치가 없다. 또한 메모리의 힙, 스택 섹션에 할당되게 된다.
디스크에 있던 프로그램이 실행될 때 코드 섹션과 데이터 섹션은 메모리에 파일 기반 페이지로 load된다.

# Page Initialization with Lazy Loading
페이지의 타입 별로 초기화 루틴이 다르다. 
페이지가 할당 되었다 : 대응되는 페이지 구조체는 있지만, 연결된 프레임은 아직 없다 -> 페이지에 대한 실제 콘텐츠들이 아직 메모리에 로드 되지 않았다. (페이지 폴트가 발생하면 그 때 로드된다.)

가장 먼저 커널이 새로운 페이지를 요청한다. (프로세스가 추가적인 메모리 할당을 부탁한다. 즉, 스택 확장 또는 파일 기반 페이지 접근 힙 영역 할당 (malloc) 등임)
그러면 vm_alloc_page_with_initializer가 호출된다.
: 이때 type에 따라ㅓㅅ 
