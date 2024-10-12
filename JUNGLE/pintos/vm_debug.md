1. spt table kill에서 발생하는 문제

기존 코드

```
/* Free the resource hold by the supplemental page table */
void
supplemental_page_table_kill (struct supplemental_page_table *spt UNUSED) {
	/* TODO: Destroy all the supplemental_page_table hold by thread and
	 * TODO: writeback all the modified contents to the storage. */
	hash_destroy(&spt->page_table, hash_delete);
}
```

터미널 로그

```
pintos -v -k -T 60 -m 20   --fs-disk=10 -p tests/userprog/args-none:args-none --swap-disk=4 -- -q   -f run args-none < /dev/null 2> tests/userprog/args-none.errors > tests/userprog/args-none.output
perl -I../.. ../../tests/userprog/args-none.ck tests/userprog/args-none tests/userprog/args-none.result
FAIL tests/userprog/args-none
Kernel panic in run: PANIC at ../../lib/kernel/list.c:242 in list_remove(): assertion `is_interior (elem)' failed.
Call stack: 0x8004218ede 0x8004219802 0x800421986b 0x800421b768 0x800421b81b 0x8004222978 0x800421d2bc 0x800421d254 0x80042075a5 0x800421e557 0x800421e0bc 0x8004209227 0x800420967f 0x800421c03e 0x800421b9be 0x8004222345 0x800422223f 0x800421dadf 0x800421d6a7 0x800421ce7b 0x800421c93a 0x80042078fd
Translation of call stack:
0x0000008004218ede: debug_panic (lib/kernel/debug.c:32)
0x0000008004219802: list_remove (lib/kernel/list.c:243)
0x000000800421986b: list_pop_front (lib/kernel/list.c:254)
0x000000800421b768: hash_clear (lib/kernel/hash.c:59)
0x000000800421b81b: hash_destroy (lib/kernel/hash.c:84)
0x0000008004222978: supplemental_page_table_kill (vm/vm.c:328)
0x000000800421d2bc: process_cleanup (userprog/process.c:428)
0x000000800421d254: process_exit (userprog/process.c:410)
0x00000080042075a5: thread_exit (threads/thread.c:383)
0x000000800421e557: create (userprog/syscall.c:168)
0x000000800421e0bc: page_fault (userprog/exception.c:149)
0x0000008004209227: intr_handler (threads/interrupt.c:352)
0x000000800420967f: intr_entry (intr-stubs.o:?)
0x000000800421c03e: find_elem (lib/kernel/hash.c:295)
0x000000800421b9be: hash_find (lib/kernel/hash.c:125)
0x0000008004222345: spt_find_page (vm/vm.c:119)
0x000000800422223f: vm_alloc_page_with_initializer (vm/vm.c:60)
0x000000800421dadf: load_segment (userprog/process.c:843)
0x000000800421d6a7: load (userprog/process.c:600)
0x000000800421ce7b: process_exec (userprog/process.c:282)
0x000000800421c93a: initd (userprog/process.c:73)
0x00000080042078fd: kernel_thread (threads/thread.c:506)
```

수정 함수
```
void action_func(struct hash_elem *e, void *aux) {
	struct page *page = hash_entry(e, struct page, hash_elem);
	destroy(page);
	free(page);
}

/* Free the resource hold by the supplemental page table */
void
supplemental_page_table_kill (struct supplemental_page_table *spt UNUSED) {
	/* TODO: Destroy all the supplemental_page_table hold by thread and
	 * TODO: writeback all the modified contents to the storage. */
	hash_clear(&spt->page_table, action_func);
}
```

# 설명
Kernel Panic의 원인:

결론적으로, hash_destroy()는 해시 테이블의 메모리까지 해제하려는 반면, hash_clear()는 요소만 삭제하기 때문에, 리스트의 일관성 문제가 커널 패닉으로 이어지는 정도의 차이가 발생하는 것이다
