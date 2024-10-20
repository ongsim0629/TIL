# Anonymous Page

Anonymous page: 파일 디스크 기반이 아닌 페이지  (백업 파일이나 장치가 없다.) -> 스택, 힙 같은 실행 파일에서 사용된다.
즉, 커널로부터 프로세스에게 할당된 일반적인 메모리 페이지이다. 

## vm_alloc_page_with_initializer()
커널이 새로운 페이지를 요청할 때 호출된다.
initializer는 페이지 구조체를 할당하고 페이지 타입에 따라서 initalizer를 설정해서 새 페이지를 초기화한 다음에 유저 프로그램으로 권한을 넘겨준다.
유조 프로그램이 실행되면서 페이지에 어떤 내용도 있지 않기 때문에 page fault가 발생하게 되고
이때 uninit_initializer가 호출된 다음에 이전에 설정했던 initializer가 호출된다.
이때 anonymous page면 anon_initializer가 호출되고, file_baced_page면 file_backed_initializer()가 호출된다.

## uninit_new()
uninit 타입으로 페이지를 초기화 시켜준다. 
이때 initializer는 매개변수로 들어온 type에 따라서 분기가 된다 (anon인지, file_backed인지)
페이지의 필드 값을 수정할 때는 uninit_new 함수가 호출된 이후에 수정해야한다. 왜냐하면 uninit_new 함수 안에서 구조체의 내용이 전부 새로 할당되기 때문이다.
이전에는 어떤 값을 수정해도 없던 내용으로 된다.

## lazy loading
프로세스가 실행될 때는 즉시 사용할 메모리만 메인 메모리에 로드한다.
페이지를 할당할 때 해당 페이지에 대응하는 페이지의 구조체만 만들고 프레임은 할당하지 않는다. 또한 실제 내용도 로딩하지 않는다!
페이지 폴트가 발생하는 시점에 내용을 로드해준다.

## vm_init()
모든 페이지들은 vm_init에서 생성된다. 초기화 되지 않은 상태의 타입이 VM_UNINIT이다.
페이지 폴트가 발생할 때 vm_try_handle_fault로 제어권을 전달한 다음에 유효한 페이지 폴트인지 확인하는 과정을 겪게 되는데
bogus fault(lazy loaded, swaped-out page, write-protexted page)는 페이지에 일부 내용을 로드하고 유저 프로그램에게 권한을 넘겨준다.

lazy-load 하기 위해서 세팅했던 이니셜라이즈 중 하나를 호출한다. 
또한 vm_type에 따라서 적절한 이니셜라이저를 가져와서 uninit_new를 호출해야한다.
```
bool
vm_alloc_page_with_initializer (enum vm_type type, void *upage, bool writable,
		vm_initializer *init, void *aux) {

	ASSERT (VM_TYPE(type) != VM_UNINIT)

	struct supplemental_page_table *spt = &thread_current ()->spt;

	/* Check wheter the upage is already occupied or not. */
	if (spt_find_page (spt, upage) == NULL) {

		/* TODO: Create the page, fetch the initialier according to the VM type,*/
		// 페이지를 생성하고,
		struct page *new_page = (struct page *)malloc(sizeof(struct page));
		bool (*page_initializer)(struct page *, enum vm_type, void *);
		page_initializer = NULL;

		switch (VM_TYPE(type)) {
		case VM_ANON:
			page_initializer = anon_initializer;
			break;
		case VM_FILE:
			page_initializer = file_backed_initializer;
			break;
		// default:
		// 	//free(new_page);
		// 	return false;
		}
		/* TODO: and then create "uninit" page struct by calling uninit_new. You
		 * TODO: should modify the field after calling the uninit_new. */
		// uninit_new를 호출해 "uninit" 페이지 구조체를 생성하세요.
		uninit_new(new_page, upage, init, type, aux, page_initializer);

		// uninit_new를 호출한 후에는 필드를 수정해야 합니다.
		new_page->writable = writable;

		/* TODO: Insert the page into the spt. */
		if (!spt_insert_page(spt, new_page)) {
				//free(new_page);
				return false;
		}
		return true;
	}
err:
	return false;
}
```

## uninit_initial_lize()
첫 번째로 페이지 폴트가 발생하면 페이지를 초기화 한다. 
```
static bool
uninit_initialize (struct page *page, void *kva) {
	struct uninit_page *uninit = &page->uninit;

	/* Fetch first, page_initialize may overwrite the values */
	vm_initializer *init = uninit->init;
	void *aux = uninit->aux;

	/* TODO: You may need to fix this function. */
	return uninit->page_initializer (page, uninit->type, kva) &&
		(init ? init (page, aux) : true);
}
```

## lazy_load_segment()
프로세스가 실행될 때 segment를 실제 메모리에 직접 로드하는 방식 -> load_segment() 함수에서 lazy_load_segment()를 불러와서 원하는 파일을 로드하도록 수정
```
static bool
lazy_load_segment (struct page *page, void *aux) {
	/* TODO: Load the segment from the file */
	/* TODO: This called when the first page fault occurs on address VA. */
	/* TODO: VA is available when calling this function. */

	struct file_page *file_info = (struct file_page *) aux;
	// struct file curr_file = file_info->file;

	// 데이터를 로드하지 않고 준비상태로 둠
    // 파일의 오프셋을 설정
    file_seek (file_info->file, file_info->ofs);

    // 파일에서 읽어야 할 바이트만큼 메모리 페이지로 로드
    if (file_read (file_info->file, page->frame->kva, file_info->read_bytes) != (int) file_info->read_bytes) {
		palloc_free_page(page->frame->kva);
        return false;
    }

    // 남은 페이지 부분을 0으로 채움
    memset (page->frame->kva + file_info->read_bytes, 0, file_info->zero_bytes);
		// free(aux) 과정이 필요함!!

    return true;

}
```

## load_segment()
파일의 내용을 upage에 로드하는 함수이다. 파일의 내용을 로드하기 위해서 upage를 할당할 페이지가 필요한데, 이 페이지를 vm_alloc_page_with_initializer로 호출해서 생성한다.
바로 파일의 내용을 로드하지 않는다 왜냐하면 lazy load 해야하기 때문이다.
페이지 폴트가 처음 발생했을 때 lazy_load_segment가 실행되고 file_page가 인자로 사용되어 내용이 로딩된다.
```
static bool
load_segment (struct file *file, off_t ofs, uint8_t *upage,
		uint32_t read_bytes, uint32_t zero_bytes, bool writable) {
	ASSERT ((read_bytes + zero_bytes) % PGSIZE == 0);
	ASSERT (pg_ofs (upage) == 0);
	ASSERT (ofs % PGSIZE == 0);

	while (read_bytes > 0 || zero_bytes > 0) {
		/* Do calculate how to fill this page.
		 * We will read PAGE_READ_BYTES bytes from FILE
		 * and zero the final PAGE_ZERO_BYTES bytes. */
		size_t page_read_bytes = read_bytes < PGSIZE ? read_bytes : PGSIZE;
		size_t page_zero_bytes = PGSIZE - page_read_bytes;

		/* TODO: Set up aux to pass information to the lazy_load_segment. */
		// file 구조체에 정보를 담아서 aux 로 전달
		struct file_page *file_info = (struct file_page*)malloc(sizeof(struct file_page));
		file_info->file = file;
		file_info->ofs = ofs;
		file_info->read_bytes = read_bytes;
		file_info->zero_bytes = zero_bytes;

		if (!vm_alloc_page_with_initializer (VM_ANON, upage,
					writable, lazy_load_segment, file_info))
			return false;

		/* Advance. */
		read_bytes -= page_read_bytes;
		zero_bytes -= page_zero_bytes;
		upage += PGSIZE;
		ofs += page_read_bytes;
	}
	return true;
}
```

## setup_stack()
스택은 아래로 성장하기 때문에 스택의 시작점인 USER_STACK에서 PGSIZE 만큼 아래로 내린 지점에서 페이지를 생성한다.
첫 번쨰 스택 페이지는 레이지 로딩할 필요가 없다. 그냥 바로 물리 프레임을 할당 받아 놓자!
페이지를 할당 받을 때 타입과 함께 보조 마커를 사용해서 스택의 페이지인지 아닌지를 마커를 통해서 구분하자
```
static bool
setup_stack (struct intr_frame *if_) {
	bool success = false;

	// 스택은 아래로 성장하므로, USER_STACK에서 PGSIZE만큼 아래로 내린 지점에서 페이지를 생성한다.
	void *stack_bottom = (void *)(((uint8_t *)USER_STACK) - PGSIZE);

	/* TODO: Map the stack on stack_bottom and claim the page immediately.
	 * TODO: If success, set the rsp accordingly.
	 * TODO: You should mark the page is stack. */
	/* TODO: stack_bottom에 스택을 매핑하고 페이지를 즉시 요청하세요.
	 * TODO: 성공하면, rsp를 그에 맞게 설정하세요.
	 * TODO: 페이지가 스택임을 표시해야 합니다. */
	/* TODO: Your code goes here */

	// 1) stack_bottom에 페이지를 하나 할당받는다.
	if (vm_alloc_page(VM_ANON | VM_MARKER_0, stack_bottom, 1)) {
	// VM_MARKER_0: 스택이 저장된 메모리 페이지임을 식별하기 위해 추가
	// writable: argument_stack()에서 값을 넣어야 하니 True
	
		// 2) 할당 받은 페이지에 바로 물리 프레임을 매핑한다.
		success = vm_claim_page(stack_bottom);
		if (success) {
			// 3) rsp를 변경한다. (argument_stack에서 이 위치부터 인자를 push한다.)
			if_->rsp = USER_STACK;
			thread_current()->stack_bottom = stack_bottom;

		}
	}
	return success;
}
```
