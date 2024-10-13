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

******** 진짜 모르겠었던 부분!!!**************
palloc_get_page -> 사용자 풀에서 새로운 physical page를 가져온다.
사용자 pool에서 palloc을 하면 사용자 영역에서 페이지를 할당하는 것이 아닌가?

->
사용자 공간에서 사용할 수 있는 물리 페이지가 뭐야?

palloc 함수를 보면
void *
palloc_get_page (enum palloc_flags flags) {
	return palloc_get_multiple (flags, 1);
}

/* Frees the PAGE_CNT pages starting at PAGES. */
void
palloc_free_multiple (void *pages, size_t page_cnt) {
	struct pool *pool;
	size_t page_idx;

	ASSERT (pg_ofs (pages) == 0);
	if (pages == NULL || page_cnt == 0)
		return;

	if (page_from_pool (&kernel_pool, pages))
		pool = &kernel_pool;
	else if (page_from_pool (&user_pool, pages))
		pool = &user_pool;
	else
		NOT_REACHED ();

	page_idx = pg_no (pages) - pg_no (pool->base);

#ifndef NDEBUG
	memset (pages, 0xcc, PGSIZE * page_cnt);
#endif
	ASSERT (bitmap_all (pool->used_map, page_idx, page_cnt));
	bitmap_set_multiple (pool->used_map, page_idx, page_cnt, false);
}

유저 풀에서 메모리를 할당해주는 것으로 보이는데 이게 왜 물리 메모리야?

ChatGPT의 말:
ChatGPT
"사용자 공간에서 사용할 수 있는 물리 페이지"라는 개념은 다음과 같이 설명할 수 있습니다:

물리 메모리와 가상 메모리:

물리 메모리: 실제 RAM에 해당하며, 운영 체제가 프로세스에 물리적으로 할당하는 메모리입니다.
가상 메모리: 각 프로세스가 가진 메모리 주소 공간으로, 프로세스가 사용하는 주소는 실제 물리 메모리 주소와 매핑됩니다.
사용자 공간:

사용자 공간은 사용자 프로세스가 실행되는 메모리 영역으로, 일반적으로 사용자 프로그램의 코드, 데이터, 스택 등이 포함됩니다.
사용자 프로세스는 커널의 개입 없이 이 공간에서 메모리를 할당하고 사용할 수 있습니다.
palloc_get_page 함수**:

palloc_get_page는 메모리 할당을 요청하는 함수로, PAL_USER 플래그를 사용하면 사용자 프로세스에서 사용할 수 있는 메모리를 요청하게 됩니다.
이 함수는 내부적으로 palloc_get_multiple를 호출하여 페이지를 할당받습니다. 이때 user_pool에서 사용 가능한 물리 페이지를 찾아 할당하게 됩니다.
물리 페이지 할당:

palloc_get_page를 통해 할당된 페이지는 사용자 프로세스가 사용할 수 있는 물리 페이지입니다. 즉, 이 페이지는 프로세스의 가상 메모리 주소와 매핑되며, 프로세스가 직접 접근할 수 있습니다.
물리 메모리에서 할당된 페이지가 사용자 공간에 매핑되어 사용되므로, 이러한 페이지를 "사용자 공간에서 사용할 수 있는 물리 페이지"라고 부르는 것입니다.
요약
결론적으로, 사용자 공간에서 사용할 수 있는 물리 페이지는 사용자 프로세스가 사용할 수 있도록 커널에 의해 할당된 실제 RAM의 페이지를 의미합니다. 이러한 페이지는 사용자 프로그램의 가상 메모리 주소와 연결되어 있어 프로세스가 직접적으로 사용할 수 있습니다.
뭔 개솔?? 일단 패스

static struct frame *vm_get_frame (void);
-> 유저 메모리 풀에서 페이지를 성공적으로 가져오면 프레임을 할당하고 프레임 구조체의 멤버들을 초기화하고 해당 프레임을 반환한다.
프레임 할당

bool vm_do_claim_page (struct page *page);
- 페이지, 프레임 연동

bool vm_claim_page (void *va);
- 주어진 va에 대응하는 페이지를 프레임에 연
일단 나중에,,,
