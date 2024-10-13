# Memory Management
union 자료형 : 하나의 메모리 영역에 다른 타입의 데이터를 저장하는 것을 허용하는 특별한 자료형

핀토스에서의 페이지 : uninit_page, anon_page, file_page, page_cache 4가지 중 하나이다.
페이지의 타입별로 swap in, swap out, 페이지 삭제들의 동작의 과정과 작업이 다르다.
따라서 페이지의 종류 별로 서로 다른 함수들을 호출해서 동작을 수행한다. -> switch case를 통해 구현

함수 포인터 : 다른 검사 없이 런타임에 결정되는 값을 바탕으로 특정한 함수를 호출하는 방법을 제공한다.

struct page_operations : 3개의 함수 포인터를 포함한 하나의 함수 테이블

vm/file.c의 struct page_operations file_ops : file_backed 페이지에 대한 함수 포인터 테이블

함수 포인터로 인해서 어떻게 file_backed_destroy가 호출되는가
vm_dealloc_page(page) -> 함수 내부의 destroy(page) 함수 호출 

```
#define destroy(page) 
if ((page)->operations->destroy) (page)->operations->destroy (page)
```

## supplemental page table
spt : 각 프로세스는 자신의 spt를 가지고 프로세스의 가상 주소에 해당하는 정보를 저장한다. 

pml4 : 가상 메모리와 물리 메모리를 매핑 관리하는 페이지 테이블 -> 간단히 각 주소를 포인팅하기만 한다. (핀토스에서 말하는 페이지 테이블이 얘다)

```
void supplemental_page_table_init (struct supplemental_page_table *spt);
```
보조 페이지 테이블을 초기화하는 함수
: initd 함수로 새로운 프로세스가 시작하거나, process.c의 __do_fork로 자식 프로세스가 생성될 때 이 함수가 호출된다.

```
struct page *spt_find_page (struct supplemental_page_table *spt, void *va);
```
: 인자로 주어진 spt에서 va와 대응되는 페이지 구조체를 찾아서 반환한다.

```
bool spt_insert_page (struct supplemental_page_table *spt, struct page *page);
```
: 인자로 주어진 spt에 페이지 구조체 삽입

# Frame Management
struct frame: 물리 메모리를 관리하는 구조체, 커널 가상 주소와 페이지 구조체를 담기 위한 멤버, 2개의 멤버를 가진다. (다른 거 더 추가해도 된다.)
