# Memory Management
먼저 supplemental page table을 다루고 그 이후에 물리 메모리 페이지 프레임을 다뤄야한다.

page는 가상 메모리에서의 페이지를 의미하는 구조체로 page에 대해서 우리가 알아야 하는 모든 필요 정보를 알고 있어야한다.
페이지는 uninit, anon, file 세가지 종류 중 하나이다.
이 각 종류에 맞는 함수를 사용하는 방법 -> 클래스 상속 (함수 포인터)

os가 관리하기 위한 테이블 : 어떻게 구현할지는 설계 철학 등이 필요함 (답 X)
mmap? mman

Kernel panic in run: PANIC at ../../lib/kernel/list.c:242 in list_remove(): assertion `is_interior (elem)' failed.

swap slot은 디스크 공간에서 스왑 영역에 존재하는 페이지 크기들의 집합이다.

spt : 이를 통해서 page fault를 처리할 수 있어야한다. page fault 발생하면 프로세스가 찾으려는 page를 찾아서 물리 메모리에 적재시켜 demand loading을 해줘야한다.
- page fault 발생시 : 어떤 데이터가 실제로 그 page에 있어야하는지 알아내기 위해서 spt에서 page fault가 발생한 가상 페이지를 찾는다
- 프로세스 종료시 : 어떤 자원들이 free되면 되는지 알기 위해서 spt를 탐색한다.
- page fault handler가 가장 중요하게 사용한다. 페이지 폴트 발생하면 접근하려던 그 페이지를 파일이든 swap slot이든 메모리로 가져와야한다.


frame table : 프레임을 효과적으로 퇴거하기 위해 필요한 자료구조
frame entry를 가지고 있다 이러한 frame들은 어떤 page에 의해서 쓰여지고 있는지, 즉 점유중인 page를 가르키는 포인터를 가지고 있다.

swap table : swap slot들이 어떻게 사용되고 있는지 추적한다.


page_fault 함수는 vm_try_handle_fault 함수를 호출한다.
vm_try_handle_fault : 페이지 폴트가 발생한 페이지를 spt에서 찾는다
-> fault 난 struct page를 spt에서 찾는다 (spt_fnd_page)

anonymous page : struct page는 할당되어있는데 물리 프레임은 없는 상태 -> 즉 로드되지 않은 상태

VM_UNINT: 모든 struct page는 이 종류로 생성된다. vm_alloc_page_with_initailizer라는 함수로 struct page가 생성된다.

vm_alloc_page_with_initializer는 struct page를 생성하고 spt에 할당한다. 근데 들어올 수 있는 page는 VM_ANON이랑 VM_FILE 뿐이며, VM_UNINIT은 임의로 생성할 수 있는 것이 아닌 시스템 상 임시로만 존재하는 종류이다. 특정 주소에 접근하기 전까지는 실제로 페이지 할당을 하지는 않고 매핑이 존재한다는 것만 남겨두고 pml4상으로 valid한 주소가 아니어서 나중에 이 주소로 접근하면 page fault가 발생하게 된다. 따라서 struct page내의 swap in이 호출되고 uninit_initialize가 발동된다. 그때서야 strcut page는 실제 용도로 활용될 종류로 변환되고 pml4를 통해서 실제 할당 및 매핑과 함께 반환된다. VM_UNINIT종류의 페이지는 임시적인 종류의 페이지여서 연결된 프레임이 존재할 수 없다.

 uninit_new : 주어진 struct page에 필요한 초기화 정보를 담는 역할 (얘를 통해서 VM_UNINIT 페이지가 생긴다)
uninit_initialize: 주어진 struct page에 담겨진 정보를 바탕으로 구조체와 연동된 페이지를 초기화한다. (얘들 통해서 VM_UNINIT 페이지의 종류가 정해진다)
-> 나눠놓은 이유 : struct page를 할당해서 임시 매핑을 만드는 시점이랑페이지를 실제로 할당할 시점을 따로 잡아놓으면 이점이 있어서

해시테이블의 키 : page->va
값 : struct page
