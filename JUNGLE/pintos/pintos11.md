# Memory Management

spt와 frame을 다루는 부분, 페이지와 프레임을 관리하는 것에 대한 구현이다. -> 사용하고 있는 가상/ 물리 영역에 대한 추적
어떤 메모리 영역이 어떤 목적으로 누구에 의해 사용되고 있는지를 추적해야한다.

```
struct page {
  const struct page_operations *operations;
  void *va;              /* Address in terms of user space */
  struct frame *frame;   /* Back reference for frame */

  union {
    struct uninit_page uninit;
    struct anon_page anon;
    struct file_page file;
#ifdef EFILESYS
    struct page_cache page_cache;
#endif
  };
};
```
page 구조체에서의 union : 멤버 변수끼리 메모리를 공유해서 메모리를 아낄 수 있다. 한 멤버 변수에 값을 넣으면 기존의 값은 지워지게 된다.
즉 페이지는 uninit, anon, file 중 하나의 타입을 가질 수 있다.

페이지는 swap in, swap out, destroy 등의 액션을 취할 수 있고 각각의 타입에 따라서 페이지의 초기화, 각 동작 등의 내용이 달라지게 된다!
이때 switch-case문을 사용해서 각각의 케이스를 처리할 수 있다. -> 상속 개념을 실현하기 위해서 함수 포인터를 사용한다.

```
struct supplemental_page_table {
	/** vm_entry 를 관리하는 테이블: 해시 구현 */
	struct hash page_table;  // 해시 테이블로 페이지를 관리
};
```
해시를 통해서 spt를 구현 -> 빠르고, 이미 핀토스 내에서 해시 관련 함수가 구현되어 있다.
또한 연속적인 공간을 쓰는게 아니므로 공간복잡도 측면에서도 효율적이다.

```
/* Hash table. */
struct hash {
	size_t elem_cnt;            /* Number of elements in table. */
	size_t bucket_cnt;          /* Number of buckets, a power of 2. */
	struct list *buckets;       /* Array of `bucket_cnt' lists. */
	hash_hash_func *hash;       /* Hash function. */
	hash_less_func *less;       /* Comparison function. */
	void *aux;                  /* Auxiliary data for `hash' and `less'. */
};
```
해시 구조체 : (key, value)로 데이터를 저장한다.
해시 함수를 통해서 해시 인덱스를 지정하고, (vaddr을 hash 계산하게 된다) 그리고 페이지의 정보가 value가 된다.
해시 계산을 통해서 해시 인덱스가 같게 되는 경우도 있는데, 이러한 해시 충돌을 처리하기 위해서 같은 해시 인덱스를 가지는 페이지들은 연결리스트로 관리된다.

버킷 : 해시 테이블 안에서 값이 저장되는 공간 -> 각 엔트리가 담기게 된다.

hash 관련 함수는 모두 hash_elem 위에서 동작하고, hash_entry 매크로는 hash_elem 구조체로부터 해당 elem을 갖고 있는 구조체로 전환 한다.
근데 이게 hash가 아니라 페이지라는 사실을 유의해야함!!!! 즉 해시 테이블에 value로 들어가는 page 구조체는 hash_elem을 멤버로 가져야한다는 말임

## hash_hash_func
주어진 aux 데이터에서 해시 요소에 대한 해시 값을 계산하고 반환하는 함수
```
uint64_t
vm_entry_hash (const struct hash_elem *e, void *aux UNUSED) {
	struct page *page = hash_entry(e, struct page, hash_elem);
	return hash_bytes(&page->va, sizeof(page->va));  // vaddr을 해시
}

```

## hash_less_func
해시 요소들을 비교하는 함수
```
bool 
vm_entry_less (const struct hash_elem *a, const struct hash_elem *b, void *aux UNUSED) {
	struct page *page_a = hash_entry(a, struct page, hash_elem);
	struct page *page_b = hash_entry(b, struct page, hash_elem);

	/* 가상 주소가 더 작은 항목을 우선순위가 높다고 판단 */
	return page_a->va < page_b->va;
}
```

## vm_get_fram
palloc_get_page() 함수를 호출해서 유저풀로부터 새로운 물리 페이지를 받는다.
만약에 유저풀로 부터 페이지를 받고 프레임을 할당 받았으면 초기화하고 유효한 주소를 리턴한다.
만약에 유저풀 메모리가 가득 차서 가용한 페이지가 없으면 가용한 메모리 공간을 얻기 위해서 할당되어있는 프레임을 제거하기도 한다.
```
static struct frame *
vm_get_frame (void) {
	struct frame *frame = NULL;
	/* TODO: Fill this function. */
	// palloc_get_page 함수를 호출하여 사용자 풀에서 새로운 physical page(frame)를 가져온다
	void *kva = palloc_get_page(PAL_USER);

	// 페이지 할당을 실패할 경우, PANIC ("todo")로 표시한다. (swap out을 구현한 이후 변경한다.)
	if (kva == NULL) {
		PANIC("todo");
	}

	// 사용자 풀에서 페이지를 성공적으로 가져오면, 프레임을 할당하고 해당 프레임의 멤버를 초기화한 후 반환한다.
	frame = (struct frame *)malloc(sizeof(struct frame));
	frame->kva = kva;
	frame->page = NULL;

	// 리스트에 추가
	lock_acquire(&frame_table_lock);
	list_push_back(&frame_table, &frame->frame_elem);
	lock_release(&frame_table_lock);

	ASSERT (frame != NULL);
	ASSERT (frame->page == NULL);
	return frame;
}
```
PAL_USER를 사용해야지 사용자 풀에서 메모리를 할당할 수 있다.
PAL_USER : 사용자 풀의 페이지가 부족해지면 사용자 프로그램의 페이지가 부족해지지만 커널 풀의 페이지가 부족해지면 커널 함수들이 메모리 확보하는데 문제가 발생하고 오류가 발생한다

